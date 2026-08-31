"""Canonical and graph projection builders.

This module owns the derived projections that are rebuilt from the accumulated
canonical object, part, and reference records.  It deliberately has no
dependency on the normalizer; filesystem/orchestration helpers are injected by
the caller to keep the boundary acyclic and behavior-preserving.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Callable


def build_canonical_and_graph(
    records_by_object: dict[str, list[dict[str, Any]]],
    indexes: dict[str, dict[str, Any]],
    object_paths: dict[str, str],
    destination: Path,
    version_guid: str,
    canonical_schema_version: int,
    stable_id: Callable[..., str],
    inferred_dependency_id: Callable[[dict[str, Any]], str],
    json_write: Callable[[Path, Any], None],
    jsonl_write: Callable[[Path, list[dict[str, Any]]], None],
) -> dict[str, Any]:
    """Resolve accumulated dependencies and materialize canonical/graph data."""
    all_object_records = [record for group in records_by_object.values() for record in group]
    canonical_objects = [record for record in all_object_records if record.get("record_type") in {"object", "part", "reference"}]
    object_records = [record for record in canonical_objects if record.get("record_type") == "object"]
    part_records = [record for record in canonical_objects if record.get("record_type") == "part"]
    references = [record for record in canonical_objects if record.get("record_type") == "reference"]
    variable_dependencies = [record for record in all_object_records if record.get("record_type") == "dependency" and record.get("relation") != "explicit_reference"]
    object_records_by_id = {record["id"]: record for record in object_records}
    object_hash_by_id = {record["id"]: record.get("object_hash") for record in object_records}
    for item in object_records:
        indexes.setdefault(item["id"], {"id": item["id"], "guid": item.get("guid"), "name": item.get("name"), "module": item.get("module"), "fully_qualified_name": item.get("fully_qualified_name"), "type": item.get("attributes", {}).get("type"), "object_kind": item.get("object_kind", "unknown"), "part_kind_counts": item.get("semantic_counts", {}).get("parts_by_kind", {}), "path": item.get("normalized_path", "")})
    part_files = {record["id"]: record["normalized_file"] for record in part_records}
    object_nodes = [{"id": record["id"], "kind": "object", "object_kind": record.get("object_kind", "unknown"), "label": record.get("fully_qualified_name", record.get("name", "")), "guid": record.get("guid"), "normalized_path": record.get("normalized_path", "")} for record in object_records]
    object_by_guid: dict[str, list[str]] = {}
    name_matches: dict[str, list[str]] = {}
    for item in object_nodes:
        if item.get("guid"):
            object_by_guid.setdefault(item["guid"], []).append(item["id"])
        object_record = object_records_by_id[item["id"]]
        for name in {item["label"], item["label"].rsplit(".", 1)[-1], object_record.get("attributes", {}).get("name")} - {None}:
            name_matches.setdefault(name, []).append(item["id"])
    dependencies_by_object = {item["id"]: {"explicit_references": [], "inferred_dependencies": [], "unresolved_references": [], "references": []} for item in object_records}

    def resolve(dependency: dict[str, Any]) -> None:
        target_guid, target_name = dependency.get("target_guid"), dependency.get("target_name")
        if dependency.get("target_object_ids") is not None:
            matches = list(dependency.get("target_object_ids") or [])
        else:
            matches = object_by_guid.get(target_guid, []) if target_guid else name_matches.get(target_name, []) if target_name else []
        if len(matches) == 1:
            dependency.update({"to_object_id": matches[0], "resolved": True})
            return
        dependency["resolved"] = False
        dependency["unresolved_reason"] = "ambiguous_target_guid" if len(matches) > 1 and target_guid else (f"ambiguous target name '{target_name}' matches {len(matches)} objects" if len(matches) > 1 else (f"no object matches target GUID '{target_guid}'" if target_guid else f"no object matches target name '{target_name}'"))

    for reference in references:
        attrs = reference.get("attributes", {})
        dependency = {"id": stable_id("dependency", reference["id"], "explicit_reference"), "from_object_id": reference["object_id"], "target_guid": attrs.get("guid") or attrs.get("targetGuid") or attrs.get("target_guid"), "target_name": attrs.get("target_name") or attrs.get("targetName") or attrs.get("name") or attrs.get("fullyQualifiedName") or reference.get("text"), "relation": "explicit_reference", "source_part": part_files.get(reference["part_id"], reference["part_id"]), "source_location": reference["source_location"], "evidence": {"raw": reference.get("raw"), "attributes": attrs}, "raw": reference.get("raw"), "reference_id": reference["id"]}
        resolve(dependency)
        dependencies_by_object[reference["object_id"]]["explicit_references"].append(dependency)
        dependencies_by_object[reference["object_id"]]["references"].append(reference)
        if not dependency["resolved"]:
            dependencies_by_object[reference["object_id"]]["unresolved_references"].append(dependency)
    canonical_dependencies: list[dict[str, Any]] = []
    for dependency in variable_dependencies:
        dependency = copy.deepcopy(dependency)
        resolve(dependency)
        dependencies_by_object[dependency["from_object_id"]]["inferred_dependencies"].append(dependency)
        if not dependency["resolved"]:
            dependencies_by_object[dependency["from_object_id"]]["unresolved_references"].append(dependency)
        canonical_dependencies.append(dependency)
    for dependencies in dependencies_by_object.values():
        canonical_dependencies.extend(dependencies["explicit_references"])
    for dependency in canonical_dependencies:
        dependency["record_type"] = "dependency"
        dependency.setdefault("object_id", dependency["from_object_id"])
        dependency["source_location"] = f'{dependency.get("source_location", "")}#dependency'
        dependency["object_hash"] = object_hash_by_id.get(dependency["from_object_id"], dependency.get("object_hash"))
        dependency.pop("target_object_ids", None)
        dependency["version_guid"] = dependency.get("version_guid", version_guid)
    canonical_objects.extend(canonical_dependencies)
    canonical_dir, graph_dir = destination / "canonical", destination / "graph"
    canonical_dir.mkdir(exist_ok=True)
    graph_dir.mkdir(exist_ok=True)
    jsonl_write(canonical_dir / "records.jsonl", [dict(record, schema_version=record.get("schema_version", canonical_schema_version)) for record in canonical_objects])
    part_nodes = [{"id": record["id"], "kind": "part", "part_kind": record.get("part_kind", record.get("kind", "unknown")) or "unknown", "label": f"{record['type']} part {record['index']}", "object_id": record["object_id"]} for record in part_records]
    resolved_ids = {dependency.get("reference_id") for groups in dependencies_by_object.values() for dependency in groups["explicit_references"] if dependency.get("resolved")}
    reference_nodes = [{"id": record["id"], "kind": "reference", "label": record.get("text") or record.get("attributes", {}).get("name", "reference"), "object_id": record["object_id"]} for record in references if record["id"] in resolved_ids]
    nodes = object_nodes + part_nodes + reference_nodes
    edges = [{"id": stable_id("edge", part["object_id"], "contains", part["id"]), "from": part["object_id"], "to": part["id"], "kind": "contains"} for part in part_nodes]
    for groups in dependencies_by_object.values():
        for group in ("explicit_references", "inferred_dependencies"):
            for dependency in groups[group]:
                if dependency.get("resolved"):
                    edge = {"id": stable_id("edge", dependency["from_object_id"], dependency["relation"], dependency["to_object_id"], dependency.get("source_location")), "from": dependency["from_object_id"], "to": dependency["to_object_id"], "kind": "references" if dependency["relation"] == "explicit_reference" else dependency["relation"], "dependency": dependency}
                    if dependency.get("reference_id"):
                        edge["reference_id"] = dependency["reference_id"]
                    edges.append(edge)
    jsonl_write(graph_dir / "nodes.jsonl", nodes)
    jsonl_write(graph_dir / "edges.jsonl", edges)
    for item in indexes.values():
        item["path"] = object_paths.get(item["id"], item.get("path", ""))
        if item["id"] in dependencies_by_object:
            json_write(destination / item["path"] / "dependencies.json", dependencies_by_object[item["id"]])
    incoming: dict[str, list[dict[str, Any]]] = {record["id"]: [] for record in object_records}
    for dependency in canonical_dependencies:
        if dependency.get("resolved") and dependency.get("relation", "").startswith("gx9_"):
            incoming[dependency["to_object_id"]].append({
                "from_object_id": dependency["from_object_id"], "relation": dependency["relation"],
                "reference_kind": dependency.get("reference_kind"), "target_kind": dependency.get("target_kind"),
                "target_name": dependency.get("target_name"), "source_location": dependency.get("source_location"),
                "span": (dependency.get("evidence") or {}).get("span"), "evidence": (dependency.get("evidence") or {}).get("source"),
            })
    for item in indexes.values():
        if item["id"] in incoming:
            json_write(destination / item["path"] / "incoming-references.json", sorted(incoming[item["id"]], key=lambda value: (value["from_object_id"], value["relation"], value.get("source_location", ""))))
    return {"canonical_objects": canonical_objects, "object_records": object_records, "part_records": part_records, "references": references, "canonical_dependencies": canonical_dependencies, "dependencies_by_object": dependencies_by_object}
