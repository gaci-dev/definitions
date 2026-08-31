"""Canonical output contract constants and validation.

This module owns the schema versions, stable contract identifiers, path
containment checks, and validation of canonical records and their projections.
It deliberately does not import the normalizer, so the normalizer can expose
these compatibility symbols without creating a circular dependency.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from .errors import GXKBError
from .redaction import is_absolute_path as _is_absolute_path


CANONICAL_SCHEMA_VERSION = 1
OUTPUT_SCHEMA_VERSION = 2


def _stable_id(prefix: str, *values: object) -> str:
    value = "\x1f".join(str(item) for item in values)
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]
    return f"{prefix}:{digest}"


def _inferred_dependency_id(dependency: dict[str, Any]) -> str:
    evidence = dependency.get("evidence") or {}
    span = evidence.get("span") or {}
    if not dependency.get("target_kind") and not span:
        return _stable_id(
            "dependency", dependency.get("from_object_id", ""), dependency.get("part_type", ""),
            dependency.get("relation", ""), dependency.get("target_name", ""),
            dependency.get("target_guid", "") or "", evidence.get("variable", ""),
            dependency.get("identity_occurrence", 0),
        )
    return _stable_id(
        "dependency", dependency.get("from_object_id", ""), dependency.get("part_type", ""),
        dependency.get("relation", ""), dependency.get("target_name", ""),
        dependency.get("target_guid", "") or "", dependency.get("target_kind", ""),
        evidence.get("variable", ""), span.get("start", ""),
        dependency.get("identity_occurrence", 0),
    )


def _contained_output_path(root: Path, value: object, label: str) -> Path:
    """Resolve a generated reference only when it stays inside the output."""
    if not isinstance(value, str) or not value or _is_absolute_path(value):
        raise GXKBError(f"Canonical {label} must be a relative path")
    root_resolved = root.resolve()
    candidate = (root / value).resolve()
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise GXKBError(f"Canonical {label} must stay inside the output directory")
    return candidate


def _legacy_output_path(root: Path, value: object, label: str) -> Path:
    """Validate a legacy output reference before touching the filesystem."""
    if not isinstance(value, str) or not value:
        raise GXKBError(f"Legacy migration {label} must be a non-empty relative path")
    if _is_absolute_path(value) or ".." in Path(value.replace("\\", "/")).parts:
        raise GXKBError(f"Legacy migration rejected {label} '{value}': absolute and traversal paths are not allowed")
    return _contained_output_path(root, value, f"legacy {label}")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_output(output_dir: str | Path) -> None:
    """Validate the additive canonical contract and its derived indexes."""
    root = Path(output_dir)
    records = _read_jsonl(root / "canonical" / "records.jsonl")
    ids = [record.get("id") for record in records]
    if any(record.get("schema_version") != CANONICAL_SCHEMA_VERSION for record in records):
        raise GXKBError("Legacy canonical output requires migration; rerun normalize to upgrade it")
    if any(not record.get("record_type") or not record.get("id") for record in records):
        raise GXKBError("Canonical records require record_type and id")
    if len(ids) != len(set(ids)):
        raise GXKBError("Canonical record IDs must be unique")
    objects = [r for r in records if r["record_type"] == "object"]
    parts = [r for r in records if r["record_type"] == "part"]
    references = [r for r in records if r["record_type"] == "reference"]
    dependencies = [r for r in records if r["record_type"] == "dependency"]
    object_ids = {r["id"] for r in objects}
    part_ids = {r["id"] for r in parts}
    if any(part.get("object_id") not in object_ids for part in parts):
        raise GXKBError("Canonical parts must reference an object")
    if any(ref.get("object_id") not in object_ids or ref.get("part_id") not in part_ids for ref in references):
        raise GXKBError("Canonical references must reference an object and part")
    if any(dep.get("from_object_id") not in object_ids for dep in dependencies):
        raise GXKBError("Canonical dependencies must reference an object")
    if any(dep.get("relation") != "explicit_reference" and dep.get("id") != _inferred_dependency_id(dep) for dep in dependencies):
        raise GXKBError("Inferred dependency IDs must use stable semantic identity")
    if any(dep.get("resolved") and dep.get("to_object_id") not in object_ids for dep in dependencies):
        raise GXKBError("Resolved canonical dependencies must reference an object target")
    for record in objects:
        object_dir = _contained_output_path(root, record.get("normalized_path"), "normalized_path")
        if not (object_dir / "metadata.json").exists():
            qualified = record.get("fully_qualified_name") or record.get("name") or record.get("id")
            raise GXKBError(
                f"Canonical object '{qualified}' with normalized path '{record.get('normalized_path')}' "
                "must reference an existing metadata projection"
            )
    for record in parts:
        normalized_file_path = _contained_output_path(root, record.get("normalized_file"), "normalized_file")
        if not normalized_file_path.exists():
            raise GXKBError("Canonical parts must reference an existing projection path")
        projection_file = record.get("projection_file")
        if projection_file:
            _contained_output_path(root, projection_file, "projection_file")
            object_dir = normalized_file_path.parent.parent
            projection_path = (object_dir / projection_file).resolve()
            if object_dir not in projection_path.parents and projection_path != object_dir:
                raise GXKBError("Canonical projection_file must stay inside its object directory")
        if projection_file and not projection_path.exists():
            raise GXKBError("Canonical parts must reference an existing recorded projection path")
    canonical_manifest = json.loads((root / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    expected_counts = {"objects": len(objects), "parts": len(parts), "references": len(references), "dependencies": len(dependencies)}
    if canonical_manifest.get("record_counts") != expected_counts:
        raise GXKBError("Canonical manifest record counts do not match records.jsonl")
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if canonical_manifest.get("schema_version") != CANONICAL_SCHEMA_VERSION or manifest.get("schema_version") != OUTPUT_SCHEMA_VERSION:
        raise GXKBError("Legacy output requires migration; rerun normalize to upgrade it")
    if manifest.get("object_count") != len(objects):
        raise GXKBError("Manifest object_count does not match canonical records")
    if manifest.get("dependency_count") != len(dependencies):
        raise GXKBError("Manifest dependency_count does not match canonical records")
    nodes = _read_jsonl(root / "graph" / "nodes.jsonl")
    edges = _read_jsonl(root / "graph" / "edges.jsonl")
    if len(nodes) != len({node.get("id") for node in nodes}):
        raise GXKBError("Graph node IDs must be unique")
    node_ids = {node.get("id") for node in nodes}
    if any(not node.get("id") or not node.get("kind") for node in nodes):
        raise GXKBError("Graph nodes require id and kind")
    expected_node_ids = object_ids | part_ids | {r["id"] for r in references if any(dep.get("reference_id") == r["id"] and dep.get("resolved") for dep in dependencies)}
    if node_ids != expected_node_ids:
        raise GXKBError("Graph nodes must cover canonical objects, parts, and resolved references")
    nodes_by_id = {node["id"]: node for node in nodes}
    if any(nodes_by_id[object_id].get("kind") != "object" for object_id in object_ids):
        raise GXKBError("Graph object nodes must have kind object")
    part_nodes = {node["id"]: node for node in nodes if node.get("kind") == "part"}
    if set(part_nodes) != part_ids or any(nodes_by_id[part["id"]].get("kind") != "part" or nodes_by_id[part["id"]].get("object_id") != part.get("object_id") for part in parts):
        raise GXKBError("Graph part nodes must preserve canonical ownership")
    reference_ids = {r["id"] for r in references if any(dep.get("reference_id") == r["id"] and dep.get("resolved") for dep in dependencies)}
    reference_object_ids = {reference["id"]: reference["object_id"] for reference in references}
    if any(nodes_by_id[reference_id].get("kind") != "reference" or nodes_by_id[reference_id].get("object_id") != reference_object_ids[reference_id] for reference_id in reference_ids):
        raise GXKBError("Graph reference nodes must preserve canonical ownership")
    if any(edge.get("from") not in node_ids or edge.get("to") not in node_ids for edge in edges):
        raise GXKBError("Graph edges must reference existing node targets")
    contains = [edge for edge in edges if edge.get("kind") == "contains"]
    expected_contains = {(part["object_id"], part["id"]) for part in parts}
    if {(edge.get("from"), edge.get("to")) for edge in contains} != expected_contains or len(contains) != len(expected_contains):
        raise GXKBError("Graph contains edges must match canonical part ownership")
    resolved_references = {dep.get("reference_id") for dep in dependencies if dep.get("resolved") and dep.get("reference_id")}
    graph_reference_ids = {node["id"] for node in nodes if node.get("kind") == "reference"}
    if resolved_references != graph_reference_ids:
        raise GXKBError("Resolved references must match graph reference nodes")
    expected_dependency_edges = Counter((dependency["from_object_id"], dependency["to_object_id"], "references" if dependency["relation"] == "explicit_reference" else dependency["relation"], dependency.get("reference_id")) for dependency in dependencies if dependency.get("resolved"))
    actual_dependency_edges = Counter((edge.get("from"), edge.get("to"), edge.get("kind"), edge.get("reference_id")) for edge in edges if edge.get("kind") != "contains")
    if actual_dependency_edges != expected_dependency_edges:
        raise GXKBError("Graph dependency edges must match resolved canonical dependencies")
