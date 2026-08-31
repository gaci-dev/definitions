from __future__ import annotations

import json
import hashlib
import os
import re
import shutil
import tempfile
import zipfile
import copy
import time
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from collections.abc import Callable
from xml.etree import ElementTree as ET

from .errors import GXKBError
from .redaction import (
    redact_output_value as _redact_output_value,
    redact_state_value as _redact_state_value,
    redact_value as _redact_value,
    redacted_element as _redacted_element,
)
from .contracts import (
    CANONICAL_SCHEMA_VERSION,
    OUTPUT_SCHEMA_VERSION,
    _contained_output_path,
    _inferred_dependency_id,
    _legacy_output_path,
    _read_jsonl,
    _stable_id,
    validate_output,
)
from .projections import build_canonical_and_graph
from .gx9 import (
    adapt as _adapt_gx9,
    is_gx9_export,
    legacy_structure_projection,
    legacy_variables_projection,
    selection_names,
)
from .gx9_references import extract as _extract_gx9_references, catalog as _catalog_gx9_references

OBJECT_KINDS = {
    "84a12160-f59b-4ad7-a683-ea4481ac23e9": "procedure",
    "1db606f2-af09-4cf9-a3b5-b481519d28f6": "transaction",
    "447527b5-9210-4523-898b-5dccb17be60a": "sdt",
    "c9584656-94b6-4ccd-890f-332d11fc2c25": "webpanel",
    # Types observed in the Biller export. The names are intentionally
    # descriptive; unknown future GeneXus types remain ``unknown``.
    "00972a17-9975-449e-aab1-d26165d51393": "domain",
    "c163e562-42c6-4158-ad83-5b21a14cf30e": "external_object",
    "2a9e9aba-d2de-4801-ae7f-5e3819222daf": "data_provider",
    "00000000-0000-0000-0000-000000000008": "folder",
    "c88fffcd-b6f8-0000-8fec-00b5497e2117": "module",
    "07135890-56fc-489b-b408-063722fa9f7d": "pattern",
    "ffd44be7-3bb4-4d01-9e7e-d1c1a3c095af": "data_selector",
    "857ca50e-7905-0000-0007-c5d9ff2975ec": "table",
    # This GeneXus type contains platform/index metadata for a database view.
    # It is named table_view rather than table because the export also contains
    # the physical table type above and this object is named ``vw_*``.
    "19abc6ff-2cd2-0000-0006-6d172bc2333b": "table_view",
    "36e32e2d-023e-4188-95df-d13573bac2e0": "api",
    "fc1b76c4-95c5-0000-0101-44f9543121bd": "index_definition",
}

OBJECT_KIND_LABELS = {
    "procedure": "Procedure",
    "transaction": "Transaction",
    "sdt": "SDT",
    "webpanel": "WebPanel",
    "menu_bar": "Menu Bar",
    "data_view": "Data View",
    "domain": "Domain",
    "external_object": "External Object",
    "data_provider": "Data Provider",
    "folder": "Folder",
    "module": "Module",
    "pattern": "Pattern",
    "data_selector": "Data Selector",
    "table": "Table",
    "unknown": "Unknown",
    "table_view": "Table View",
    "api": "API",
    "index_definition": "Index Definition",
}

PART_KINDS = {
    "gx9:structure": "legacy_structure",
    "gx9:variables": "legacy_variables",
    "gx9:form": "legacy_form",
    "gx9:events": "legacy_events",
    "gx9:rules": "legacy_rules",
    "gx9:documentation": "legacy_documentation",
    "gx9:table": "legacy_table",
    "gx9:report": "legacy_report",
    "gx9:code": "legacy_code",
    "528d1c06-a9c2-420d-bd35-21dca83f12ff": "procedure_code",
    "264be5fb-1b28-4b25-a598-6ca900dd059f": "transaction_structure",
    "5c2aa9da-8fc4-4b6b-ae02-8db4fa48976a": "sdt_structure",
    "d24a58ad-57ba-41b7-9e6e-eaca3543c778": "form_layout",
    "c414ed00-8cc4-4f44-8820-4baf93547173": "report_layout",
    "a2bc65a1-999f-4e9b-b837-72285cc9bb16": "data_selector",
    # Both spellings have appeared in exports; keep the legacy variant for
    # compatibility while recognizing the GUID used by current Biller exports.
    "9b0a32a3-de6d-4be1-a4dd-1b85d3741534": "rules",
    "9b0a32a3-de6b-4be1-a4dd-1b85d3741534": "rules",
    "e4c4ade7-53f0-4a56-bdfd-843735b66f47": "variables",
    "c44bd5ff-f918-415b-98e6-aca44fed84fa": "events",
    "babf62c5-0111-49e9-a1c3-cc004d90900a": "object_defaults",
    "00000000-0000-0000-0002-000000000005": "external_members",
    "ed1b7b1c-2aaf-46eb-9ec5-db348f6fa3fc": "export_metadata",
    "ad3ca970-19d0-44e1-a7b7-db05556e820c": "help",
    "763f0d8b-d8ac-4db4-8dd4-de8979f2b5b9": "auxiliary_source",
    "4c28dfb9-f83b-46f0-9cf3-f7e090b525d5": "defaults",
    "00000000-0000-0000-0002-000000000004": "key",
    "19abc6ff-2cd2-1000-0006-6d172bc2333b": "platforms",
    "1d8aeb5a-6e98-45a7-92d2-d8de7384e432": "data_provider_source",
    "7706bd3b-212a-1000-0006-8aaeb59068b9": "indexes",
    "9f577ec2-27f4-4cf4-8ad5-f3f50c9d69b5": "api_source",
    "a51ced48-7bee-0001-ab12-04e9e32123d1": "pattern_data",
    "a5c0e770-560d-0001-0001-7fe71c260de3": "indexes",
    "a5e6a251-2df0-44d8-adab-1da237574326": "module_metadata",
    "fe47b55c-ea2a-1000-0101-5b38901e24f7": "members",
}
INVALID_FILENAME = re.compile(r"[^\w .-]+", re.UNICODE)


@dataclass
class InputDocument:
    original: Path
    xml_path: Path
    source_kind: str
    warnings: list[str]
    temporary_dir: tempfile.TemporaryDirectory[str] | None = None


ProgressCallback = Callable[[dict[str, Any]], None]


class _ProgressReporter:
    """Emit stable progress events without adding work to every object."""

    def __init__(self, callback: ProgressCallback | None) -> None:
        self.callback = callback
        self.started = time.monotonic()
        self.last_emit = 0.0
        self.last_percent = -5

    def emit(self, stage: str, message: str, **counts: Any) -> None:
        if self.callback is None:
            return
        event = {"stage": stage, "message": message, "elapsed": round(time.monotonic() - self.started, 3), **counts}
        self.callback(event)

    def object(self, current: int, total: int, **counts: Any) -> None:
        if self.callback is None:
            return
        percent = int(current * 100 / total) if total else 100
        now = time.monotonic()
        if current != total and percent < self.last_percent + 25 and now - self.last_emit < 1.0:
            return
        self.last_emit = now
        self.last_percent = percent
        self.emit("object_processing", "Processing objects", current=current, total=total, percent=percent, **counts)


def _safe_name(value: str, fallback: str) -> str:
    cleaned = INVALID_FILENAME.sub("_", value).strip(" .")
    return cleaned or fallback


def _object_path_parts(qualified: str, guid: str | None, collision: bool, collision_identity: str | None = None, parent: str | None = None) -> tuple[str, str, str]:
    bits = qualified.rsplit(".", 1)
    module = _safe_name(bits[0], "root") if len(bits) == 2 else "root"
    if "." not in qualified:
        module = _safe_name(parent or "root", "root")
    name = _safe_name(bits[-1], "object")
    directory_name = name
    if collision:
        suffix_source = guid or collision_identity or qualified
        suffix = _safe_name((suffix_source if guid else hashlib.sha256(suffix_source.encode("utf-8")).hexdigest())[:12], "object")
        directory_name = f"{name}--{suffix}"
    return module, name, directory_name


def _text(element: ET.Element | None) -> str:
    return "" if element is None else "".join(element.itertext()).strip()


def _json_write(path: Path, value: Any) -> None:
    _atomic_write(path, json.dumps(_json_safe_value(value), ensure_ascii=False, indent=2) + "\n")


def _jsonl_write(path: Path, values: Iterable[dict[str, Any]]) -> None:
    content = []
    for value in values:
        content.append(json.dumps(_json_safe_value(value), ensure_ascii=False, sort_keys=True) + "\n")
    _atomic_write(path, "".join(content))


def _json_safe_value(value: Any) -> Any:
    """Make structured output acceptable to case-insensitive JSON consumers.

    XML attributes are case-sensitive, while PowerShell treats JSON property
    names case-insensitively.  When both spellings occur in one object, keep
    the lower-case contract spelling and retain every original spelling/value
    in an explicit, unambiguous list.
    """
    if isinstance(value, list):
        return [_json_safe_value(item) for item in value]
    if not isinstance(value, dict):
        return value

    grouped: dict[str, list[tuple[str, Any]]] = {}
    for key, item in value.items():
        grouped.setdefault(str(key).casefold(), []).append((str(key), item))

    result: dict[str, Any] = {}
    raw_attributes: list[dict[str, Any]] = []
    for entries in grouped.values():
        if len(entries) == 1:
            key, item = entries[0]
            result[key] = _json_safe_value(item)
            continue
        preferred = next((entry for entry in entries if entry[0] == entry[0].lower()), entries[0])
        result[preferred[0]] = _json_safe_value(preferred[1])
        raw_attributes.extend({"name": key, "value": _json_safe_value(item)} for key, item in entries)

    if raw_attributes:
        existing = result.get("raw_attributes")
        if existing is None:
            result["raw_attributes"] = raw_attributes
        elif isinstance(existing, list):
            result["raw_attributes"] = existing + raw_attributes
        else:
            result["raw_attributes"] = [existing, *raw_attributes]
    return result


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _managed_output_names() -> tuple[str, ...]:
    return ("raw", "objects", "canonical", "graph", "kb-state.json", "manifest.json", "objects-index.jsonl")


def _remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def _commit_staged_output(staged: Path, destination: Path) -> None:
    """Replace managed output as one rollback-protected commit.

    User-owned files are never touched; all work that can fail happens before
    this function, in the staging tree.
    """
    backup = Path(tempfile.mkdtemp(prefix="gxkb-backup-", dir=str(destination.parent)))
    destination.mkdir(parents=True, exist_ok=True)
    moved_old: list[str] = []
    moved_new: list[str] = []
    try:
        for name in _managed_output_names():
            current = destination / name
            if current.exists():
                os.replace(current, backup / name)
                moved_old.append(name)
        for name in _managed_output_names():
            candidate = staged / name
            if candidate.exists():
                os.replace(candidate, destination / name)
                moved_new.append(name)
    except Exception as commit_error:
        rollback_errors: list[tuple[str, Exception]] = []
        for name in reversed(moved_new):
            try:
                _remove_path(destination / name)
            except Exception as exc:
                rollback_errors.append((f"remove new '{name}'", exc))
        for name in reversed(moved_old):
            try:
                os.replace(backup / name, destination / name)
            except Exception as exc:
                rollback_errors.append((f"restore old '{name}'", exc))
        if rollback_errors:
            details = "; ".join(f"{operation}: {error}" for operation, error in rollback_errors)
            raise GXKBError(
                f"Output commit failed: {commit_error}. Rollback incomplete; "
                f"backup preserved at {backup}. Recovery required ({details})."
            ) from commit_error
        try:
            shutil.rmtree(backup)
        except Exception as cleanup_error:
            raise GXKBError(
                f"Output commit failed: {commit_error}. Rollback restored the previous output, "
                f"but backup cleanup failed; backup preserved at {backup}."
            ) from cleanup_error
        raise GXKBError(
            f"Output commit failed: {commit_error}. Rollback completed; previous output restored "
            f"and backup removed at {backup}."
        ) from commit_error
    try:
        shutil.rmtree(backup)
    except Exception as cleanup_error:
        raise GXKBError(
            f"Output commit succeeded, but backup cleanup failed; backup preserved at {backup}. "
            f"Remove it after confirming the output is valid ({cleanup_error})."
        ) from cleanup_error


def _stage_output(destination: Path) -> tuple[tempfile.TemporaryDirectory[str], Path]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = tempfile.TemporaryDirectory(prefix="gxkb-stage-", dir=str(destination.parent))
    staged = Path(temporary.name) / "output"
    if destination.exists():
        shutil.copytree(destination, staged)
    else:
        staged.mkdir()
    return temporary, staged


def _validate_new_kb_destination(destination: Path) -> None:
    if destination.exists() and any(destination.iterdir()):
        raise GXKBError("--new-kb solo puede inicializar un directorio vacío")


def _redact_existing_output(destination: Path) -> None:
    """Sanitize retained objects/ledgers when a later run enables redaction."""
    for root_name in ("objects", "canonical", "graph"):
        root = destination / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            if path.suffix in {".json", ".jsonl"}:
                if path.suffix == ".jsonl":
                    value = "\n".join(
                        json.dumps(_redact_output_value(json.loads(line)), ensure_ascii=False, sort_keys=True)
                        for line in text.splitlines() if line.strip()
                    ) + ("\n" if text.endswith("\n") else "")
                else:
                    value = json.dumps(_redact_output_value(json.loads(text)), ensure_ascii=False, indent=2) + "\n"
            else:
                value = _redact_value(text)
            _atomic_write(path, value)
    for path in (destination / "manifest.json", destination / "canonical" / "manifest.json", destination / "objects-index.jsonl"):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".jsonl":
            value = "\n".join(
                json.dumps(_redact_output_value(json.loads(line)), ensure_ascii=False, sort_keys=True)
                for line in text.splitlines() if line.strip()
            ) + ("\n" if text.endswith("\n") else "")
        else:
            value = json.dumps(_redact_output_value(json.loads(text)), ensure_ascii=False, indent=2) + "\n"
        _atomic_write(path, value)


def _redact_raw_history(destination: Path) -> None:
    """Sanitize retained XML raws and remove retained XPZ binaries."""
    raw = destination / "raw"
    if not raw.exists():
        return
    for path in raw.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".xpz":
            path.unlink()
            continue
        if path.suffix.lower() != ".xml":
            continue
        try:
            root = ET.parse(path).getroot()
            content = ET.tostring(_redacted_element(root), encoding="unicode") + "\n"
        except ET.ParseError:
            content = '<redacted-raw status="omitted" reason="invalid-xml"/>\n'
        _atomic_write(path, content)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _normalized_xml(element: ET.Element) -> str:
    """Serialize an element deterministically for incremental fingerprints."""
    def render(node: ET.Element) -> str:
        tag = node.tag
        attrs = "".join(f' {key}={value!r}' for key, value in sorted(node.attrib.items()))
        text = (node.text or "").strip()
        children = "".join(render(child) for child in list(node))
        tail = ""  # tails are formatting outside the object and are ignored
        return f"<{tag}{attrs}>{text}{children}</{tag}>"
    return render(element)


def _object_hash(element: ET.Element) -> str:
    return hashlib.sha256(_normalized_xml(element).encode("utf-8")).hexdigest()


def _canonical_contract_is_current(root: Path, records: list[dict[str, Any]]) -> bool:
    if not records or any(record.get("schema_version") != CANONICAL_SCHEMA_VERSION for record in records):
        return False
    try:
        canonical_manifest = json.loads((root / "canonical" / "manifest.json").read_text(encoding="utf-8"))
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    if canonical_manifest.get("schema_version") != CANONICAL_SCHEMA_VERSION or manifest.get("schema_version") != OUTPUT_SCHEMA_VERSION:
        return False
    try:
        validate_output(root)
    except (GXKBError, FileNotFoundError, json.JSONDecodeError):
        return False
    return (
        canonical_manifest.get("schema_version") == CANONICAL_SCHEMA_VERSION
        and manifest.get("schema_version") == OUTPUT_SCHEMA_VERSION
        and canonical_manifest.get("record_counts") == {
            "objects": sum(record.get("record_type") == "object" for record in records),
            "parts": sum(record.get("record_type") == "part" for record in records),
            "references": sum(record.get("record_type") == "reference" for record in records),
            "dependencies": sum(record.get("record_type") == "dependency" for record in records),
        }
    )


def _migrate_legacy_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Upgrade legacy canonical records without losing objects absent from input."""
    migrated = [copy.deepcopy(record) for record in records]
    object_id_map: dict[str, str] = {}
    objects = [record for record in migrated if record.get("record_type") == "object"]
    for index, record in enumerate(objects):
        old_id = record.get("id") or f"legacy-object-{index}"
        attributes = record.get("attributes") or {}
        qualified = record.get("fully_qualified_name") or attributes.get("fullyQualifiedName") or record.get("name")
        if not qualified:
            raise GXKBError("Legacy migration cannot derive an object identity; restore the canonical output or provide fully_qualified_name/name")
        object_id = record.get("id") or (f"object:{record.get('guid')}" if record.get("guid") else _stable_id(
            "object", qualified, attributes.get("type", record.get("type", "")), record.get("name", ""), attributes.get("parent", "")
        ))
        if object_id in object_id_map.values():
            raise GXKBError(f"Legacy migration found ambiguous object identity for {qualified}; restore the canonical output before retrying")
        object_id_map[old_id] = object_id
        record["id"] = object_id
        record["schema_version"] = CANONICAL_SCHEMA_VERSION
        record["fully_qualified_name"] = qualified
        record["attributes"] = attributes

    part_id_map: dict[str, str] = {}
    part_occurrences: dict[tuple[str, str, str], int] = {}
    for index, record in enumerate(record for record in migrated if record.get("record_type") == "part"):
        old_object_id = record.get("object_id")
        object_id = object_id_map.get(old_object_id, old_object_id)
        if object_id not in object_id_map.values():
            raise GXKBError("Legacy migration cannot derive part ownership; restore the canonical output before retrying")
        part_type = record.get("type", "unknown")
        source = record.get("source_xml") or record.get("content")
        if not source:
            raise GXKBError(f"Legacy migration cannot derive part identity for {part_type}; restore the canonical output before retrying")
        key = (object_id, part_type, source)
        occurrence = part_occurrences.get(key, 0)
        part_occurrences[key] = occurrence + 1
        old_part_id = record.get("id") or f"legacy-part-{index}"
        part_id = record.get("id") or _stable_id("part", object_id, part_type, source, occurrence)
        part_id_map[old_part_id] = part_id
        record.update({"id": part_id, "object_id": object_id, "schema_version": CANONICAL_SCHEMA_VERSION})

    for record in migrated:
        if record.get("record_type") == "object":
            old_part_ids = record.get("part_ids", [])
            if any(part_id not in part_id_map for part_id in old_part_ids):
                raise GXKBError("Legacy migration found stale object.part_ids; restore the canonical output before retrying")
            record["part_ids"] = [part_id_map[part_id] for part_id in old_part_ids]
        elif record.get("record_type") == "reference":
            old_object_id, old_part_id = record.get("object_id"), record.get("part_id")
            if old_object_id not in object_id_map and old_object_id not in object_id_map.values() or old_part_id not in part_id_map and old_part_id not in part_id_map.values():
                raise GXKBError("Legacy migration cannot derive reference ownership; restore the canonical output before retrying")
            record.update({"object_id": object_id_map.get(old_object_id, old_object_id), "part_id": part_id_map.get(old_part_id, old_part_id), "schema_version": CANONICAL_SCHEMA_VERSION})
        elif record.get("record_type") == "dependency":
            old_object_id = record.get("from_object_id") or record.get("object_id")
            object_id = object_id_map.get(old_object_id, old_object_id)
            if object_id not in object_id_map.values():
                raise GXKBError("Legacy migration cannot derive dependency ownership; restore the canonical output before retrying")
            record["from_object_id"] = object_id
            record["object_id"] = object_id
            if record.get("reference_id"):
                record["reference_id"] = next((item["id"] for item in migrated if item.get("record_type") == "reference" and item.get("id") == record["reference_id"]), record["reference_id"])
            if not record.get("id"):
                record["id"] = (_inferred_dependency_id(record) if record.get("relation") != "explicit_reference" else _stable_id(
                    "dependency", record.get("from_object_id", ""), record.get("source_part", ""), record.get("relation", ""), record.get("source_location", ""), record.get("target_name", "")
                ))
            record["schema_version"] = CANONICAL_SCHEMA_VERSION
    reference_occurrences: dict[tuple[str, str], int] = {}
    reference_id_map: dict[str, str] = {}
    for index, record in enumerate(record for record in migrated if record.get("record_type") == "reference"):
        part_id = record.get("part_id")
        if part_id not in part_id_map.values():
            raise GXKBError("Legacy migration cannot derive reference ownership; restore the canonical output before retrying")
        raw = record.get("raw") or record.get("text") or json.dumps(record.get("attributes", {}), sort_keys=True)
        key = (part_id, raw)
        occurrence = reference_occurrences.get(key, 0)
        reference_occurrences[key] = occurrence + 1
        old_reference_id = record.get("id") or f"legacy-reference-{index}"
        reference_id = record.get("id") or _stable_id("reference", part_id, raw, occurrence)
        reference_id_map[old_reference_id] = reference_id
        record["id"] = reference_id
        record["schema_version"] = CANONICAL_SCHEMA_VERSION
    for record in migrated:
        if record.get("record_type") == "dependency" and record.get("reference_id"):
            reference_id = reference_id_map.get(record["reference_id"])
            if reference_id is None:
                raise GXKBError("Legacy migration found a dependency with a stale reference_id; restore the canonical output before retrying")
            record["reference_id"] = reference_id
    return migrated


def _unique_raw_copy(source: Path, raw: Path) -> str:
    """Keep the legacy filename when possible, suffixing collisions by content hash."""
    raw.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
    candidate = raw / source.name
    if candidate.exists() and hashlib.sha256(candidate.read_bytes()).hexdigest() != hashlib.sha256(source.read_bytes()).hexdigest():
        candidate = raw / f"{source.stem}-{digest}{source.suffix}"
    if not candidate.exists():
        shutil.copy2(source, candidate)
    return str(candidate.relative_to(raw.parent)).replace("\\", "/")


def _element_path(root: ET.Element, target: ET.Element) -> str:
    """Return a stable, human-readable location without depending on line data."""
    path: list[str] = []

    def visit(element: ET.Element, current: list[str]) -> bool:
        tag = element.tag.rsplit("}", 1)[-1]
        next_path = current + [f"{tag}[1]"] if not current else current
        if element is target:
            path.extend(next_path)
            return True
        positions: dict[str, int] = {}
        for child in list(element):
            child_tag = child.tag.rsplit("}", 1)[-1]
            positions[child_tag] = positions.get(child_tag, 0) + 1
            child_path = next_path + [f"{child_tag}[{positions[child_tag]}]"]
            if visit(child, child_path):
                return True
        return False

    visit(root, [])
    return "/".join(path)


def _element_paths(root: ET.Element) -> dict[int, str]:
    """Build stable paths for every element in one document traversal."""
    paths: dict[int, str] = {}

    def visit(element: ET.Element, current: list[str]) -> bool:
        tag = element.tag.rsplit("}", 1)[-1]
        next_path = current + [f"{tag}[1]"] if not current else current
        paths[id(element)] = "/".join(next_path)
        positions: dict[str, int] = {}
        for child in list(element):
            child_tag = child.tag.rsplit("}", 1)[-1]
            positions[child_tag] = positions.get(child_tag, 0) + 1
            child_path = next_path + [f"{child_tag}[{positions[child_tag]}]"]
            visit(child, child_path)
        return True

    visit(root, [])
    return paths


def _xml_candidates(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        return sorted(
            name for name in archive.namelist() if not name.endswith("/") and name.lower().endswith(".xml")
        )


def _prepare_input(path: Path, raw_dir: Path, xml_member: str | None) -> InputDocument:
    if not path.is_file():
        raise GXKBError(f"No existe el archivo de entrada: {path}")
    suffix = path.suffix.lower()
    if suffix == ".xml":
        destination = raw_dir / path.name
        if destination.exists() and destination.read_bytes() != path.read_bytes():
            destination = raw_dir / f"{path.stem}-{hashlib.sha256(path.read_bytes()).hexdigest()[:12]}{path.suffix}"
        if not destination.exists() or destination.read_bytes() != path.read_bytes():
            shutil.copy2(path, destination)
        return InputDocument(path, destination, "xml", [])
    if suffix != ".xpz":
        raise GXKBError("La entrada debe tener extensión .xml o .xpz; GXL is only a selection file")
    try:
        members = _xml_candidates(path)
    except zipfile.BadZipFile as exc:
        raise GXKBError(f"El XPZ no es un ZIP válido: {path}") from exc
    if not members:
        raise GXKBError("El XPZ no contiene archivos XML")
    warnings: list[str] = []
    selected = xml_member.replace("\\", "/") if xml_member else members[0]
    if selected not in members:
        raise GXKBError(f"El XML indicado no está en el XPZ: {xml_member}")
    if len(members) > 1 and xml_member is None:
        warnings.append(f"XPZ con {len(members)} XML; se eligió determinísticamente el primero: {selected}")
    archive_copy = raw_dir / path.name
    if archive_copy.exists() and archive_copy.read_bytes() != path.read_bytes():
        archive_copy = raw_dir / f"{path.stem}-{hashlib.sha256(path.read_bytes()).hexdigest()[:12]}{path.suffix}"
    if not archive_copy.exists() or archive_copy.read_bytes() != path.read_bytes():
        shutil.copy2(path, archive_copy)
    temporary = tempfile.TemporaryDirectory(prefix="gxkb-")
    extracted = Path(temporary.name) / Path(selected).name
    with zipfile.ZipFile(path) as archive, archive.open(selected) as source, extracted.open("wb") as target:
        shutil.copyfileobj(source, target)
    raw_xml = raw_dir / f"selected-{extracted.name}"
    if raw_xml.exists() and raw_xml.read_bytes() != extracted.read_bytes():
        raw_xml = raw_dir / f"selected-{hashlib.sha256(extracted.read_bytes()).hexdigest()[:12]}-{extracted.name}"
    if not raw_xml.exists() or raw_xml.read_bytes() != extracted.read_bytes():
        shutil.copy2(extracted, raw_xml)
    return InputDocument(path, raw_xml, "xpz", warnings, temporary)


def _parse(path: Path) -> ET.Element:
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise GXKBError(f"XML malformado en {path}: {exc}") from exc


def _element_snapshot(element: ET.Element, redact_source: bool = False) -> dict[str, Any]:
    attributes = {_key: _redact_value(value, _key) for _key, value in element.attrib.items()} if redact_source else dict(element.attrib)
    return {"tag": element.tag, "attributes": attributes, "text": _redact_value(_text(element)) if redact_source else _text(element)}


def _references(object_element: ET.Element, redact_source: bool = False) -> list[dict[str, Any]]:
    return [_element_snapshot(reference, redact_source) for reference in object_element.iter() if reference.tag.rsplit("}", 1)[-1] == "Reference"]


def _object_parts(object_element: ET.Element) -> list[ET.Element]:
    parts: list[ET.Element] = []

    def visit(node: ET.Element) -> None:
        for child in list(node):
            tag = child.tag.rsplit("}", 1)[-1]
            if tag == "Object":
                continue
            if tag == "Part":
                parts.append(child)
            else:
                visit(child)

    visit(object_element)
    return parts


def _part_content(part: ET.Element, redact_source: bool = False) -> str:
    if part.attrib.get("preserve_raw") == "true":
        value = ET.tostring(_redacted_element(part) if redact_source else part, encoding="unicode")
        return _redact_value(value) if redact_source else value
    source = next((child for child in part.iter() if child.tag.rsplit("}", 1)[-1] == "Source"), None)
    if source is not None:
        value = _text(source)
    else:
        value = ET.tostring(part, encoding="unicode")
    return _redact_value(value) if redact_source else value


def _gx9_raw(node: ET.Element, redact_source: bool) -> str:
    return ET.tostring(_redacted_element(node) if redact_source else node, encoding="unicode")


def _property_map(element: ET.Element, redact_source: bool = False) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for prop in element.iter():
        if prop.tag.rsplit("}", 1)[-1] != "Property":
            continue
        name = _text(next((child for child in prop if child.tag.rsplit("}", 1)[-1] == "Name"), None))
        value = _text(next((child for child in prop if child.tag.rsplit("}", 1)[-1] == "Value"), None))
        if not name:
            continue
        value = _redact_value(value) if redact_source else value
        if name in values:
            values[name] = values[name] if isinstance(values[name], list) else [values[name]]
            values[name].append(value)
        else:
            values[name] = value
    return values


def _bool_value(value: str | None) -> bool | None:
    if value is None:
        return None
    if value.lower() in {"true", "1", "yes"}:
        return True
    if value.lower() in {"false", "0", "no"}:
        return False
    return None


def _variable_value(variable: ET.Element, names: set[str], properties: dict[str, Any]) -> Any:
    for key, value in variable.attrib.items():
        if key.lower() in names and value:
            return value
    for key, value in properties.items():
        if key.lower() in names and value not in (None, ""):
            return value
    return None


def _variables_projection(part: ET.Element, redact_source: bool = False) -> dict[str, Any]:
    """Return a lossless-enough structured view of a Variables part.

    GeneXus exports vary between attribute-based and Property-based variables;
    retain both forms and the serialized XML whenever a semantic field is not
    confidently available.
    """
    variables: list[dict[str, Any]] = []
    for variable in (node for node in part.iter() if node.tag.rsplit("}", 1)[-1] == "Variable"):
        properties = _property_map(variable, redact_source)
        attributes = ({key: _redact_value(value, key) for key, value in variable.attrib.items()} if redact_source else dict(variable.attrib))
        name = attributes.get("Name") or attributes.get("name") or properties.get("Name")
        variable_type = _variable_value(variable, {"type", "vartype", "data_type"}, properties)
        based_on = _variable_value(variable, {"basedon", "based_on", "based-on", "basedonobject"}, properties)
        nullable_raw = _variable_value(variable, {"isnullable", "nullable"}, properties)
        nullable = _bool_value(str(nullable_raw)) if nullable_raw is not None else None
        custom_type = properties.get("ATTCUSTOMTYPE")
        uses_sdt = None
        if isinstance(custom_type, str) and custom_type.lower().startswith("sdt:"):
            uses_sdt = custom_type[4:].split(",", 1)[0].strip() or None
        item: dict[str, Any] = {
            "name": name,
            "type": variable_type or custom_type,
            "based_on": based_on,
            "nullable": nullable,
            "properties": properties,
            "attributes": attributes,
            "raw": ET.tostring(_redacted_element(variable) if redact_source else variable, encoding="unicode"),
        }
        if uses_sdt:
            item["uses_sdt"] = uses_sdt
        variables.append(item)
    part_attributes = ({key: _redact_value(value, key) for key, value in part.attrib.items()} if redact_source else dict(part.attrib))
    return {
        "kind": "variables",
        "part_attributes": part_attributes,
        "properties": _property_map(part, redact_source),
        "variables": variables,
        "raw": ET.tostring(_redacted_element(part) if redact_source else part, encoding="unicode"),
    }


def _variable_dependencies(object_id: str, part_id: str, part: ET.Element, source_location: str, redact_source: bool = False, legacy: bool = False) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    occurrences: dict[tuple[str, str, str, str], int] = {}
    for variable in (node for node in part.iter() if node.tag.rsplit("}", 1)[-1] == "Variable"):
        properties = _property_map(variable, redact_source)
        based_on = _variable_value(variable, {"basedon", "based_on", "based-on", "basedonobject"}, properties)
        if legacy and not based_on:
            based_on = _text(next((child for child in variable.iter() if child.tag.rsplit("}", 1)[-1].lower() in {"basedon", "based_on"}), None)) or None
        custom_type = properties.get("ATTCUSTOMTYPE")
        target_name = based_on
        relation = "gx9_based_on" if legacy else "based_on"
        if not target_name and isinstance(custom_type, str) and custom_type.lower().startswith("sdt:"):
            target_name = custom_type[4:].split(",", 1)[0].strip() or None
            relation = "uses_sdt"
        if not target_name:
            continue
        target_guid = None
        for key, value in variable.attrib.items():
            if key.lower() in {"guid", "targetguid", "target_guid"}:
                target_guid = value
                break
        raw = ET.tostring(_redacted_element(variable) if redact_source else variable, encoding="unicode")
        variable_name = variable.attrib.get("Name") or variable.attrib.get("name") or _text(next((child for child in variable.iter() if child.tag.rsplit("}", 1)[-1].lower() == "name"), None)) or ""
        identity = (relation, target_name, target_guid or "", variable_name)
        occurrence = occurrences.get(identity, 0)
        occurrences[identity] = occurrence + 1
        result.append({
            "id": _inferred_dependency_id({
                "from_object_id": object_id, "part_type": part.attrib.get("type", ""), "relation": relation,
                "target_name": target_name, "target_guid": target_guid, "evidence": {"variable": variable_name},
                "identity_occurrence": occurrence,
            }),
            "from_object_id": object_id,
            "target_guid": target_guid,
            "target_name": _redact_value(target_name) if redact_source else target_name,
            "relation": relation,
            "source_part": f"parts/{part_id}",
            "part_type": part.attrib.get("type", ""),
            "source_location": source_location,
            "evidence": {"variable": _redact_value(variable_name) if redact_source else variable_name, "raw": raw},
            "identity_occurrence": occurrence,
            "resolved": False,
        })
    return result


def _gx9_structure_attributes(element: ET.Element) -> set[str]:
    result: set[str] = set()
    for part in _object_parts(element):
        for node in part.iter():
            if node.tag.rsplit("}", 1)[-1] == "Attribute" and _text(node):
                result.add(_text(node).rstrip("*").strip())
    return result


def _gx9_source_dependencies(object_id: str, part_id: str, part: ET.Element, source_location: str, catalog: dict[str, Any], redact_source: bool = False) -> list[dict[str, Any]]:
    known = set(catalog.get("attributes", {}))
    header_attributes: set[str] = set()
    result: list[dict[str, Any]] = []
    occurrence: dict[tuple[str, str, int], int] = {}
    for source in ["".join(node.itertext()) for node in part.iter() if node.tag.rsplit("}", 1)[-1] == "Source"] or [_text(part)]:
        for item in _extract_gx9_references(source, known, header_attributes):
            key = (item["relation"], item["target_name"], item["span"]["start"])
            count = occurrence.get(key, 0)
            occurrence[key] = count + 1
            target_name = item["target_name"]
            if item["target_kind"] == "attribute":
                matches = sorted(catalog.get("attributes", {}).get(target_name.casefold(), set()))
            else:
                matches = sorted(catalog.get("objects", {}).get(target_name, []))
                if not matches:
                    matches = sorted(catalog.get("objects", {}).get(target_name.split(".")[-1], []))
            evidence_source = item["evidence"]
            result.append({
                "id": _inferred_dependency_id({"from_object_id": object_id, "part_type": part.attrib.get("type", ""), "relation": item["relation"], "target_name": target_name, "target_kind": item["target_kind"], "evidence": {"span": item["span"]}, "identity_occurrence": count}),
                "record_type": "dependency", "from_object_id": object_id, "object_id": object_id,
                "target_name": _redact_value(target_name) if redact_source else target_name,
                "target_kind": item["target_kind"], "reference_kind": item["reference_kind"], "relation": item["relation"],
                "source_part": f"parts/{part_id}", "part_type": part.attrib.get("type", ""),
                "source_location": f"{source_location}#gx9:{item['span']['line']}:{item['span']['column']}",
                "evidence": {"source": _redact_value(evidence_source) if redact_source else evidence_source, "span": item["span"]},
                "target_object_ids": matches, "identity_occurrence": count, "resolved": False,
            })
    return result


def _semantic_structure(part: ET.Element, kind: str, redact_source: bool = False) -> dict[str, Any] | None:
    if kind == "transaction_structure":
        levels = []
        for level in (node for node in part.iter() if node.tag.rsplit("}", 1)[-1] == "Level"):
            attrs = {key: _redact_value(value, key) for key, value in level.attrib.items()} if redact_source else dict(level.attrib)
            attributes = []
            for attribute in level:
                if attribute.tag.rsplit("}", 1)[-1] != "Attribute":
                    continue
                item = {key: _redact_value(value, key) for key, value in attribute.attrib.items()} if redact_source else dict(attribute.attrib)
                item["name"] = _redact_value(_text(attribute)) if redact_source else _text(attribute)
                key = _bool_value(item.get("key"))
                if key is not None:
                    item["key"] = key
                nullable = _bool_value(item.get("isNullable"))
                if nullable is not None:
                    item["isNullable"] = nullable
                item["properties"] = _property_map(attribute, redact_source)
                attributes.append(item)
            levels.append({"name": attrs.get("Name"), "attributes": attrs, "properties": _property_map(level, redact_source), "items": attributes})
        return {"kind": kind, "levels": levels, "attribute_count": sum(len(level["items"]) for level in levels)}
    if kind == "sdt_structure":
        levels = []
        for level in (node for node in part.iter() if node.tag.rsplit("}", 1)[-1] == "Level"):
            level_attrs = {key: _redact_value(value, key) for key, value in level.attrib.items()} if redact_source else dict(level.attrib)
            info = next((node for node in level if node.tag.rsplit("}", 1)[-1] == "LevelInfo"), None)
            level_info = {"attributes": ({key: _redact_value(value, key) for key, value in info.attrib.items()} if redact_source else dict(info.attrib)) if info is not None else {}, "properties": _property_map(info, redact_source) if info is not None else {}}
            items = []
            for node in level.iter():
                if node.tag.rsplit("}", 1)[-1] != "Item":
                    continue
                item = {key: _redact_value(value, key) for key, value in node.attrib.items()} if redact_source else dict(node.attrib)
                item["properties"] = _property_map(node, redact_source)
                items.append(item)
            levels.append({"name": level_attrs.get("Name"), "attributes": level_attrs, "level_info": level_info, "items": items})
        return {"kind": kind, "levels": levels, "item_count": sum(len(level["items"]) for level in levels)}
        return None


def _generic_part_projection(part: ET.Element, kind: str, redact_source: bool = False) -> dict[str, Any]:
    """Project known containers without assigning GeneXus meaning to fields.

    The canonical part and ``parts/*.txt`` remain the source of truth.  This
    projection only exposes XML names that are stable and explicitly requested
    by the format (Properties, Members, Indexes, etc.).
    """
    def attrs(node: ET.Element) -> dict[str, Any]:
        return ({key: _redact_value(value, key) for key, value in node.attrib.items()}
                if redact_source else dict(node.attrib))

    def node_projection(node: ET.Element) -> dict[str, Any]:
        result: dict[str, Any] = {
            "tag": node.tag,
            "attributes": attrs(node),
            "text": _redact_value(_text(node)) if redact_source else _text(node),
            "raw_xml": ET.tostring(_redacted_element(node) if redact_source else node, encoding="unicode"),
        }
        properties = _property_map(node, redact_source)
        if properties:
            result["properties"] = properties
        for child_name, field_name in (("Name", "name"), ("Value", "value"), ("InnerHtml", "inner_html")):
            child = next((child for child in node if child.tag.rsplit("}", 1)[-1] == child_name), None)
            if child is not None:
                result[field_name] = _redact_value(_text(child)) if redact_source else _text(child)
        return result

    result: dict[str, Any] = {
        "kind": kind,
        "part_attributes": attrs(part),
        "properties": _property_map(part, redact_source),
        "raw_xml": ET.tostring(_redacted_element(part) if redact_source else part, encoding="unicode"),
    }
    tags = {
        "Property": "properties_nodes", "InnerHtml": "inner_html", "Member": "members", "Members": "members",
        "Index": "indexes", "Indexes": "indexes", "PlatformProperties": "platform_properties", "Platform": "platforms", "Platforms": "platforms",
        "Key": "keys", "ExternalProperty": "external_properties", "ExternalProperties": "external_properties", "ExternalMethod": "external_methods", "ExternalMethods": "external_methods",
        "ExternalEvent": "external_events", "ExternalEvents": "external_events", "HelpItem": "help_items", "Content": "content",
        "Data": "data", "Object": "objects",
    }
    for tag, field in tags.items():
        values = [node_projection(node) for node in part.iter() if node is not part and node.tag.rsplit("}", 1)[-1] == tag]
        if values:
            result[field] = values
    return result


def _generic_projection_markdown(projection: dict[str, Any], title: str) -> str:
    """Readable conservative projection for parts whose fields are not typed."""
    lines = [f"# {title}", "", "Proyección legible; el XML completo y el raw de la part permanecen conservados.", ""]
    for key, value in projection.items():
        if key in {"raw_xml", "part_attributes", "properties"}:
            continue
        if isinstance(value, list):
            lines.append(f"## {key}")
            lines.append("")
            for item in value:
                if isinstance(item, dict):
                    label = item.get("name") or item.get("value") or item.get("text") or item.get("tag")
                    lines.append(f"- **{_markdown_cell(label)}**")
                else:
                    lines.append(f"- {_markdown_cell(item)}")
            lines.append("")
        elif value not in (None, ""):
            lines.append(f"- **{key}:** {_markdown_cell(value)}")
    return "\n".join(lines).rstrip() + "\n"


PART_PROJECTION_FILES: dict[str, tuple[str, str]] = {
    "object_defaults": ("object-defaults", "json"),
    "external_members": ("external-members", "json"),
    "export_metadata": ("export-metadata", "json"),
    "help": ("help", "md"),
    "auxiliary_source": ("auxiliary-source", "gx"),
    "defaults": ("defaults", "json"),
    "key": ("key", "json"),
    "platforms": ("platforms", "json"),
    "data_provider_source": ("data-provider-source", "gx"),
    "indexes": ("indexes", "json"),
    "api_source": ("api", "gx"),
    "pattern_data": ("pattern-data", "json"),
    "module_metadata": ("module-metadata", "json"),
    "members": ("members", "json"),
}


def _layout_projection(part: ET.Element, redact_source: bool = False) -> str:
    lines = ["# GeneXus layout/form projection", "", "This file is a readable projection of a layout part.", ""]
    source = next((child for child in part.iter() if child.tag.rsplit("}", 1)[-1] == "Source"), None)
    projection_root = part
    if source is not None and _text(source).lstrip().startswith("<"):
        try:
            projection_root = ET.fromstring(_text(source))
        except ET.ParseError:
            pass
    for node in projection_root.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"Part", "Source", "Properties", "Property", "Name", "Value"}:
            continue
        attrs = " ".join(f"{key}={_redact_value(value, key) if redact_source else value!r}" for key, value in sorted(node.attrib.items()))
        lines.append(f"- `{tag}`" + (f" ({attrs})" if attrs else ""))
    return "\n".join(lines) + "\n"


def _markdown_cell(value: Any) -> str:
    """Keep generated tables readable without allowing source text to break them."""
    if value is None or value == "":
        return "—"
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def _variables_markdown(projection: dict[str, Any], json_file: str) -> str:
    lines = ["# Variables", "", f"Resumen estructurado de variables. El XML completo de la part está disponible en `parts/` y en `{json_file}`.", ""]
    lines.append(f"[Abrir {json_file}](./{json_file})")
    lines.extend(["", "| Nombre | Tipo | based_on | Nullable | Propiedades relevantes |", "|---|---|---|---|---|"])
    for item in projection.get("variables", []):
        properties = item.get("properties", {})
        relevant = ", ".join(f"{key}={value}" for key, value in properties.items() if key.lower() not in {"name"})
        lines.append("| " + " | ".join(_markdown_cell(item.get(key)) for key in ("name", "type", "based_on", "nullable")) + f" | {_markdown_cell(relevant)} |")
    return "\n".join(lines) + "\n"


def _object_markdown(
    object_dir: Path,
    normalized_path: str,
    qualified: str,
    attrs: dict[str, Any],
    module: str,
    name: str,
    object_kind: str,
    part_records: list[dict[str, Any]],
    canonical_parts: list[dict[str, Any]],
) -> str:
    """Build a navigable human/agent summary; JSON remains in its own files."""
    kind_label = OBJECT_KIND_LABELS.get(object_kind, object_kind.replace("_", " ").title())
    lines = [f"# {qualified}", "", f"**Type:** {kind_label}", f"**Type GUID:** `{attrs.get('type', '—')}`"]
    lines.extend([
        f"**Object GUID:** `{attrs.get('guid', '—')}`",
        f"**Module:** `{_markdown_cell(module)}`",
        f"**Name:** `{_markdown_cell(name)}`",
        f"**Normalized path:** `{_markdown_cell(normalized_path)}`",
    ])
    description = attrs.get("description")
    if description:
        lines.extend(["", "## Description", "", str(description)])

    available = [
        path.name for path in sorted(object_dir.iterdir())
        if path.is_file() and path.name in {
            "code.gx", "rules.gx", "events.gx", "variables.md", "variables.json", "structure.json",
            "form.gx", "layout.gx", "documentation.md", "dependencies.json",
            "table.json", "platforms.json", "key.json", "indexes.json", "members.json",
            "external-members.json", "api.gx", "api.json", "help.md", "data-provider-source.gx",
        }
    ]
    available.extend(
        path.name for path in sorted(object_dir.iterdir())
        if path.is_file() and re.match(r"^(code|rules|events|variables|structure|form|layout)-\d{3}\.(gx|md|json)$", path.name)
    )
    variables_dir = object_dir / "variables"
    if variables_dir.is_dir():
        available.extend(
            str(path.relative_to(object_dir)).replace("\\", "/")
            for path in sorted(variables_dir.iterdir())
            if path.is_file() and re.match(r"^variables(?:-\d{3})?\.(md|json)$", path.name)
        )
    if available:
        lines.extend(["", "## Content", ""])
        lines.extend(f"- [{name}](./{name})" for name in available)

    counts: dict[str, int] = {}
    for part in part_records:
        kind = part.get("part_kind") or "unknown"
        counts[kind] = counts.get(kind, 0) + 1
    lines.extend(["", "## Parts", "", "| # | Part kind | File | Type GUID | Count |", "|---:|---|---|---|---:|"])
    for part in part_records:
        kind = part.get("part_kind") or "unknown"
        file_name = part.get("projection_file") or part["file"]
        lines.append(
            f"| {part['index']} | `{_markdown_cell(kind)}` | [{file_name}](./{file_name}) | "
            f"`{_markdown_cell(part.get('type'))}` | {counts[kind]} |"
        )

    semantic_by_kind = {
        part.get("part_kind"): part.get("semantic")
        for part in canonical_parts
        if part.get("semantic")
    }
    if object_kind == "transaction" and ("transaction_structure" in semantic_by_kind or "legacy_structure" in semantic_by_kind):
        structure = semantic_by_kind.get("legacy_structure") or semantic_by_kind["transaction_structure"]
        lines.extend(["", "## Transaction structure", ""])
        lines.append(f"Levels: **{len(structure.get('levels', []))}** · Attributes: **{structure.get('attribute_count', 0)}**")
        for level in structure.get("levels", []):
            lines.append(f"- **Level `{_markdown_cell(level.get('name'))}`**")
            for item in level.get("items", []):
                flags = []
                if item.get("key") is True:
                    flags.append("primary key")
                if "isNullable" in item:
                    flags.append(f"isNullable={item['isNullable']}")
                suffix = f" ({', '.join(flags)})" if flags else ""
                lines.append(f"  - `{_markdown_cell(item.get('name'))}`{suffix}")
    if object_kind == "sdt" and "sdt_structure" in semantic_by_kind:
        structure = semantic_by_kind["sdt_structure"]
        lines.extend(["", "## SDT structure", ""])
        lines.append(f"Levels: **{len(structure.get('levels', []))}** · Items: **{structure.get('item_count', 0)}**")
        for level in structure.get("levels", []):
            lines.append(f"- **Level `{_markdown_cell(level.get('name'))}`**: {len(level.get('items', []))} item(s)")
            for item in level.get("items", []):
                lines.append(f"  - `{_markdown_cell(item.get('name'))}`")
    if object_kind in {"table_view", "table"}:
        links = [name for name in ("table.json", "platforms.json", "key.json", "indexes.json") if (object_dir / name).exists()]
        if links:
            lines.extend(["", "## Database metadata", "", "Salidas estructuradas conservadoras: " + ", ".join(f"[{item}](./{item})" for item in links) + "."])
    if object_kind == "api":
        api_links = [path.name for path in object_dir.iterdir() if path.is_file() and path.name.startswith("api") and path.suffix in {".gx", ".json"}]
        if api_links:
            lines.extend(["", "## API", "", "Source y metadata: " + ", ".join(f"[{item}](./{item})" for item in sorted(api_links)) + "."])
    if object_kind == "index_definition" and (object_dir / "members.json").exists():
        lines.extend(["", "## Members", "", "[members.json](./members.json)"])
    external_files = [path.name for path in object_dir.iterdir() if path.is_file() and path.name.startswith("external-members")]
    if external_files:
        lines.extend(["", "## External members", "", ", ".join(f"[{item}](./{item})" for item in sorted(external_files))])
    return "\n".join(lines) + "\n"


def _write_object(root_dir: Path, xml_root: ET.Element, element: ET.Element, index: int, redact_source: bool = False, collision: bool = False, object_id_override: str | None = None, gx9_catalog: dict[str, Any] | None = None, element_paths: dict[int, str] | None = None) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    if element_paths is None:
        element_paths = _element_paths(xml_root)
    attrs = dict(element.attrib)
    if redact_source:
        attrs = {key: _redact_value(value, key) for key, value in attrs.items()}
    qualified = attrs.get("fullyQualifiedName", attrs.get("name", f"object-{index}"))
    object_id = object_id_override or (f"object:{attrs['guid']}" if attrs.get("guid") else _stable_id("object", qualified, attrs.get("type", ""), attrs.get("name", ""), attrs.get("parent", "")))
    module, name, directory_name = _object_path_parts(
        qualified, attrs.get("guid"), collision=collision, collision_identity=object_id, parent=attrs.get("parent")
    )
    object_dir = root_dir / "objects" / module / directory_name
    object_dir.mkdir(parents=True, exist_ok=True)
    parts_dir = object_dir / "parts"
    parts_dir.mkdir(exist_ok=True)
    parts = _object_parts(element)
    object_kind = attrs.get("object_kind") or OBJECT_KINDS.get(attrs.get("type", "").lower(), "unknown")
    typed: dict[str, list[str]] = {}
    part_records: list[dict[str, Any]] = []
    canonical_parts: list[dict[str, Any]] = []
    canonical_references: list[dict[str, Any]] = []
    variable_dependencies: list[dict[str, Any]] = []
    seen_parts: dict[str, int] = {}
    for part_index, part in enumerate(parts, 1):
        part_type = part.attrib.get("type", "unknown")
        content = _part_content(part, redact_source)
        part_fingerprint = _normalized_xml(part)
        occurrence = seen_parts.get(part_fingerprint, 0)
        seen_parts[part_fingerprint] = occurrence + 1
        part_name = f"{part_index:03d}-{_safe_name(part_type, 'unknown')}.txt"
        (parts_dir / part_name).write_text(content + ("\n" if content and not content.endswith("\n") else ""), encoding="utf-8")
        kind = PART_KINDS.get(part_type.lower())
        semantic = (_semantic_structure(part, kind, redact_source) if kind in {"transaction_structure", "sdt_structure"}
                    else legacy_structure_projection(part, (lambda value, key: _redact_value(value, key)) if redact_source else None, lambda node: _gx9_raw(node, redact_source))
                    if kind == "legacy_structure" and object_kind == "transaction"
                    else legacy_variables_projection(part, (lambda value, key: _redact_value(value, key)) if redact_source else None, lambda node: _gx9_raw(node, redact_source))
                    if kind == "legacy_variables"
                    else _generic_part_projection(part, kind, redact_source) if kind else None)
        if kind:
            typed.setdefault(kind, []).append(content)
        part_records.append({"index": part_index, "type": part_type, "file": f"parts/{part_name}", "kind": kind, "part_kind": kind})
        part_id = _stable_id("part", object_id, part_type, part_fingerprint, occurrence)
        canonical_parts.append({
            "record_type": "part",
            "id": part_id,
            "object_id": object_id,
            "index": part_index,
            "type": part_type,
            "kind": kind,
            "part_kind": kind,
            "content": content,
            "semantic": semantic,
            "source_xml": ET.tostring(_redacted_element(part), encoding="unicode") if redact_source else ET.tostring(part, encoding="unicode"),
            "source_location": element_paths.get(id(part), ""),
            "normalized_file": f"objects/{module}/{directory_name}/parts/{part_name}",
        })
        if kind in {"variables", "legacy_variables"}:
            variable_dependencies.extend(_variable_dependencies(
                object_id, part_id, part, element_paths.get(id(part), ""), redact_source,
                legacy=kind == "legacy_variables",
            ))
        if gx9_catalog is not None and kind in {"legacy_code", "legacy_rules", "legacy_events", "legacy_report", "gx9:code", "gx9:rules", "gx9:events"}:
            variable_dependencies.extend(_gx9_source_dependencies(
                object_id, part_id, part, element_paths.get(id(part), ""), gx9_catalog, redact_source,
            ))
        seen_references: dict[str, int] = {}
        for reference_index, reference in enumerate(
            node for node in part.iter() if node.tag.rsplit("}", 1)[-1] == "Reference"
        ):
            reference_fingerprint = _normalized_xml(reference)
            reference_occurrence = seen_references.get(reference_fingerprint, 0)
            seen_references[reference_fingerprint] = reference_occurrence + 1
            reference_id = _stable_id("reference", part_id, reference_fingerprint, reference_occurrence)
            canonical_references.append({
                "record_type": "reference",
                "id": reference_id,
                "object_id": object_id,
                "part_id": part_id,
                "index": reference_index,
                "attributes": {key: _redact_value(value, key) for key, value in reference.attrib.items()} if redact_source else dict(reference.attrib),
                "text": _redact_value(_text(reference)) if redact_source else _text(reference),
                "raw": ET.tostring(_redacted_element(reference) if redact_source else reference, encoding="unicode"),
                "source_location": element_paths.get(id(reference), ""),
            })
    part_kind_counts: dict[str, int] = {}
    for part in part_records:
        part_kind = part["part_kind"] or "unknown"
        part_kind_counts[part_kind] = part_kind_counts.get(part_kind, 0) + 1
    normalized_path = str(object_dir.relative_to(root_dir)).replace("\\", "/")
    metadata = {"attributes": attrs, "guid": attrs.get("guid"), "object_kind": object_kind, "fully_qualified_name": qualified, "module": module, "name": name, "normalized_path": normalized_path, "parts": part_records, "semantic_counts": {"parts": len(parts), "parts_by_kind": part_kind_counts}}
    if typed.get("structure"):
        (object_dir / "structure.md").write_text("\n\n".join(typed["structure"]) + "\n", encoding="utf-8")
    projection_counts: dict[str, int] = {}
    for part_record, part in zip(part_records, parts):
        part_kind = part_record["part_kind"]
        if part_kind:
            projection_counts[part_kind] = projection_counts.get(part_kind, 0) + 1
            occurrence = projection_counts[part_kind]

        def projection_name(base: str, extension: str) -> str:
            suffix = "" if occurrence == 1 else f"-{occurrence:03d}"
            return f"{base}{suffix}.{extension}"

        projection_file: str | None = None
        if part_kind == "procedure_code":
            projection_file = projection_name("code", "gx")
            (object_dir / projection_file).write_text(_part_content(part, redact_source) + "\n", encoding="utf-8")
        elif part_kind == "legacy_code":
            projection_file = projection_name("code", "gx")
            (object_dir / projection_file).write_text(_part_content(part, redact_source) + "\n", encoding="utf-8")
        elif part_kind in {"transaction_structure", "sdt_structure", "legacy_structure"}:
            semantic = (_semantic_structure(part, part_kind, redact_source)
                        if part_kind in {"transaction_structure", "sdt_structure"}
                        else legacy_structure_projection(part, (lambda value, key: _redact_value(value, key)) if redact_source else None, lambda node: _gx9_raw(node, redact_source)))
            projection_file = projection_name("structure", "json")
            _json_write(object_dir / projection_file, semantic)
        elif part_kind in {"form_layout", "report_layout"}:
            filename = "form.gx" if part_kind == "form_layout" else "layout.gx"
            base, extension = filename.rsplit(".", 1)
            projection_file = projection_name(base, extension)
            (object_dir / projection_file).write_text(_layout_projection(part, redact_source), encoding="utf-8")
        elif part_kind in {"rules", "events"}:
            projection_file = projection_name(part_kind, "gx")
            (object_dir / projection_file).write_text(_part_content(part, redact_source) + "\n", encoding="utf-8")
        elif part_kind == "variables":
            projection = _variables_projection(part, redact_source)
            projection_file = f"variables/{projection_name('variables', 'json')}"
            _json_write(object_dir / projection_file, projection)
            md_file = projection_name("variables", "md")
            md_file = f"variables/{md_file}"
            (object_dir / md_file).write_text(_variables_markdown(projection, projection_file), encoding="utf-8")
        elif part_kind == "legacy_variables":
            projection = legacy_variables_projection(part, (lambda value, key: _redact_value(value, key)) if redact_source else None, lambda node: _gx9_raw(node, redact_source))
            projection_file = f"variables/{projection_name('variables', 'json')}"
            _json_write(object_dir / projection_file, projection)
            md_file = projection_name("variables", "md")
            md_file = f"variables/{md_file}"
            (object_dir / md_file).write_text(_variables_markdown(projection, projection_file), encoding="utf-8")
        elif part_kind in PART_PROJECTION_FILES:
            base, extension = PART_PROJECTION_FILES[part_kind]
            projection = _generic_part_projection(part, part_kind, redact_source)
            projection_file = projection_name(base, extension)
            if extension == "json":
                _json_write(object_dir / projection_file, projection)
            elif extension == "md":
                (object_dir / projection_file).write_text(
                    _generic_projection_markdown(projection, part_kind.replace("_", " ").title()), encoding="utf-8"
                )
            else:
                (object_dir / projection_file).write_text(_part_content(part, redact_source) + "\n", encoding="utf-8")
            # API consumers need both executable-looking source and metadata.
            if part_kind == "api_source":
                metadata_file = projection_name("api", "json")
                _json_write(object_dir / metadata_file, projection)
        if projection_file:
            part_record["projection_file"] = projection_file
            canonical_parts[part_index - 1]["projection_file"] = projection_file
    if object_kind in {"table_view", "table"}:
        _json_write(object_dir / "table.json", {
            "kind": object_kind,
            "object": {"guid": attrs.get("guid"), "name": name, "fully_qualified_name": qualified, "attributes": attrs},
            "parts": [
                {"index": item["index"], "part_kind": item.get("part_kind"), "type": item.get("type"),
                 "file": item.get("projection_file") or item.get("file"), "semantic": item.get("semantic")}
                for item in canonical_parts if item.get("part_kind") in {"platforms", "indexes", "key", "members"}
            ],
        })
    _json_write(object_dir / "metadata.json", metadata)
    docs = [_redact_value(_text(node)) if redact_source else _text(node) for node in element.iter() if node.tag.rsplit("}", 1)[-1] == "Documentation" and _text(node)]
    if docs:
        (object_dir / "documentation.md").write_text("# Documentation\n\n" + "\n\n".join(docs) + "\n", encoding="utf-8")
    (object_dir / "object.md").write_text(
        _object_markdown(object_dir, normalized_path, qualified, attrs, module, name, object_kind, part_records, canonical_parts),
        encoding="utf-8",
    )
    summary = {"index": index, "id": object_id, "guid": attrs.get("guid"), "name": name, "module": module, "fully_qualified_name": qualified, "type": attrs.get("type"), "object_kind": object_kind, "part_kind_counts": part_kind_counts, "path": str(object_dir.relative_to(root_dir)).replace("\\", "/"), "references": len(canonical_references)}
    canonical_object = {
        "record_type": "object",
        "id": object_id,
        "guid": attrs.get("guid"),
        "attributes": attrs,
        "object_kind": object_kind,
        "fully_qualified_name": qualified,
        "module": module,
        "name": name,
        "source_location": element_paths.get(id(element), ""),
        "normalized_path": summary["path"],
        "part_ids": [part["id"] for part in canonical_parts],
        "semantic_counts": {"parts": len(parts), "parts_by_kind": part_kind_counts},
    }
    return summary, [canonical_object, *canonical_parts], canonical_references, variable_dependencies


def normalize(input_path: str | Path = "", output_dir: str | Path = "normalized-kb", xml_member: str | None = None,
               preserve_raw: bool = True, redact_source: bool = False, reprocess_all: bool = False,
               new_kb: bool = False, share_safe: bool = False, snapshot: bool = False,
               gxl_selection: str | Path | None = None, progress: ProgressCallback | None = None) -> Path:
    """Incrementally merge one XML/XPZ into an output directory.

    ``kb-state.json`` is the ingestion ledger. Objects are keyed by GUID and
    fingerprints are tracked per version GUID. By default absent objects are
    intentionally retained because an export may be partial. ``snapshot=True``
    explicitly reconciles the imported KB/version and records tombstones for
    objects absent from that complete input.
    """
    if share_safe:
        preserve_raw = False
        redact_source = True
    source = Path(input_path)
    final_destination = Path(output_dir)
    reporter = _ProgressReporter(progress)
    if new_kb:
        _validate_new_kb_destination(final_destination)
    staging_context, destination = _stage_output(final_destination)
    raw = destination / "raw"
    raw.mkdir(exist_ok=True)
    document: InputDocument | None = None
    try:
        reporter.emit("input_preparation", "Preparing input", current=0, total=0, processed=0, skipped=0)
        document = _prepare_input(source, raw, xml_member)
        reporter.emit("parse_adaptation", "Parsing XML and adapting export", current=0, total=0, processed=0, skipped=0)
        root = _parse(document.xml_path)
        selected_names: set[str] | None = None
        if gxl_selection is not None:
            selection_path = Path(gxl_selection)
            if not selection_path.is_file():
                document.warnings.append(f"GXL selection file not found; no filtering applied: {selection_path}")
            else:
                try:
                    selected_names, _ = selection_names(selection_path)
                except ValueError as exc:
                    raise GXKBError(str(exc)) from exc
        gx9_input = is_gx9_export(root)
        if gx9_input:
            root, adapter_warnings = _adapt_gx9(root, selected_names)
            document.warnings.extend(adapter_warnings)
        elif gxl_selection is not None:
            document.warnings.append("GXL selection ignored because the primary input is not a GX9 export")
        element_paths = _element_paths(root)
        source_nodes = [n for n in root.iter() if n.tag.rsplit("}", 1)[-1] == "Source"]
        source_metadata = dict(source_nodes[0].attrib) if source_nodes else {}
        kb_guid = source_metadata.get("kb", "")
        version_nodes = [n for n in root.iter() if n.tag.rsplit("}", 1)[-1] == "Version"]
        versions = [dict(n.attrib) for n in version_nodes]
        version = versions[0] if versions else {}
        version_guid, version_name = version.get("guid", "unknown"), version.get("name", "")
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        safe_source_name = "[REDACTED_INPUT]" if share_safe else source.name
        state_path = destination / "kb-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"schema_version": 1, "kb": {}, "versions": {}, "objects": {}, "imports": []}
        registered_kb = state.get("kb", {}).get("guid") or ""
        registered_kb = "" if registered_kb == "unknown" else registered_kb
        # Older/hand-authored XML fixtures may omit Source. Keep compatibility;
        # identity enforcement applies whenever either side provides a GUID.
        if registered_kb and kb_guid and registered_kb != kb_guid:
            raise GXKBError(f"KB GUID incompatible: output={registered_kb}, entrada={kb_guid}; use un output nuevo (o --new-kb vacío)")
        kb_guid = kb_guid or registered_kb

        objects = [n for n in root.iter() if n.tag.rsplit("}", 1)[-1] == "Object"]
        reporter.emit("object_processing", "Processing objects", current=0, total=len(objects), processed=0, skipped=0)
        guid_counts: dict[str, int] = {}
        for obj in objects:
                if obj.attrib.get("guid"): guid_counts[obj.attrib["guid"]] = guid_counts.get(obj.attrib["guid"], 0) + 1
        gx9_catalog = (_catalog_gx9_references(objects, guid_counts, _gx9_structure_attributes) if gx9_input else None)
        old_records = _read_jsonl(destination / "canonical" / "records.jsonl")
        contract_current = _canonical_contract_is_current(destination, old_records)
        # Upgrade legacy records in place.  Partial exports must retain objects
        # absent from the current input; dropping these records would orphan
        # their already-materialized object directories and index entries.
        if old_records and not contract_current:
            old_records = _migrate_legacy_records(old_records)
        for record in old_records:
            if record.get("record_type") == "dependency" and not record.get("id"):
                record["id"] = (_inferred_dependency_id(record) if record.get("relation") != "explicit_reference" else _stable_id(
                    "dependency", record.get("from_object_id", ""), record.get("source_part", ""), record.get("relation", ""), record.get("source_location", ""), record.get("target_name", "")
                ))
        records_by_object: dict[str, list[dict[str, Any]]] = {}
        for record in old_records:
            object_id = record.get("id") if record.get("record_type") == "object" else record.get("object_id")
            if object_id:
                records_by_object.setdefault(object_id, []).append(record)
        current_ids = {
            (f"object:{obj.attrib['guid']}" if obj.attrib.get("guid") and guid_counts.get(obj.attrib["guid"], 0) == 1
             else _stable_id("object", obj.attrib.get("guid", ""), obj.attrib.get("fullyQualifiedName", ""), obj.attrib.get("type", ""))): obj
            for obj in objects
        }
        object_path_inputs: dict[str, tuple[str, str | None, str | None]] = {}
        for object_id, records in records_by_object.items():
            record = next((item for item in records if item.get("record_type") == "object"), None)
            if record and record.get("fully_qualified_name"):
                object_path_inputs[object_id] = (
                    record["fully_qualified_name"], record.get("guid"), record.get("module"),
                )
        for object_id, obj in current_ids.items():
            fqn = obj.attrib.get("fullyQualifiedName", obj.attrib.get("name", ""))
            if fqn:
                object_path_inputs[object_id] = (fqn, obj.attrib.get("guid"), obj.attrib.get("parent"))
        path_ids: dict[str, set[str]] = {}
        for object_id, (qualified, guid, parent) in object_path_inputs.items():
            path_qualified = _redact_value(qualified) if redact_source else qualified
            module, _, directory_name = _object_path_parts(path_qualified, guid, collision=False, parent=parent)
            path_ids.setdefault(f"objects/{module}/{directory_name}".casefold(), set()).add(object_id)
        collision_ids = {object_id for ids in path_ids.values() if len(ids) > 1 for object_id in ids}
        object_paths: dict[str, str] = {}
        for object_id, records in records_by_object.items():
            record = next((item for item in records if item.get("record_type") == "object"), None)
            if not record:
                continue
            module, _, directory_name = _object_path_parts(
                _redact_value(record["fully_qualified_name"]) if redact_source else record["fully_qualified_name"],
                record.get("guid"), object_id in collision_ids, collision_identity=object_id,
                parent=record.get("module"),
            )
            object_paths[object_id] = f"objects/{module}/{directory_name}"
            old_path = record.get("normalized_path")
            old_path_value = _legacy_output_path(destination, old_path, "normalized_path") if old_path else None
            new_path_value = _legacy_output_path(destination, object_paths[object_id], "target path")
            if old_path_value and old_path != object_paths[object_id] and old_path_value.exists():
                new_path_value.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_path_value), str(new_path_value))
            if old_path != object_paths[object_id]:
                metadata_path = destination / object_paths[object_id] / "metadata.json"
                if metadata_path.exists():
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                    metadata["normalized_path"] = object_paths[object_id]
                    _json_write(metadata_path, metadata)
                markdown_path = destination / object_paths[object_id] / "object.md"
                if markdown_path.exists():
                    markdown = markdown_path.read_text(encoding="utf-8")
                    if "**Normalized path:**" not in markdown:
                        markdown += f"\n**Normalized path:** `{object_paths[object_id]}`\n"
                        _atomic_write(markdown_path, markdown)
                for item in records:
                    if item.get("record_type") == "object":
                        item["normalized_path"] = object_paths[object_id]
                    elif item.get("record_type") == "part" and old_path:
                        item["normalized_file"] = item["normalized_file"].replace(old_path + "/", object_paths[object_id] + "/")
                for version_item in state.get("objects", {}).get(object_id, {}).get("versions", {}).values():
                    version_item["path"] = object_paths[object_id]
        now = _utc_now()
        state.setdefault("kb", {"guid": kb_guid})
        state["kb"] = {"guid": kb_guid}
        state.setdefault("versions", {})
        version_entry = state["versions"].setdefault(version_guid, {"guid": version_guid, "name": version_name, "import_count": 0})
        version_entry.update({"name": version_name, "last_seen": now, "import_count": version_entry.get("import_count", 0) + 1})
        indexes = {item["id"]: item for item in _read_jsonl(destination / "objects-index.jsonl") if item.get("id")}
        retired_ids: list[str] = []
        if snapshot:
            # Reconciliation is version-scoped. Older versions stay in the
            # ledger; only the current projection is reconciled. All changes
            # happen in the staging tree and therefore commit atomically.
            state.setdefault("tombstones", {})
            for object_id, entry in state.get("objects", {}).items():
                if object_id in current_ids:
                    continue
                version_state = entry.get("versions", {}).get(version_guid)
                if version_state is None or not version_state.get("active", True):
                    continue
                retired_ids.append(object_id)
                version_state.update({"active": False, "retired_at": now, "retirement": "absent_from_snapshot"})
                tombstone = {
                    "object_id": object_id,
                    "guid": entry.get("guid"),
                    "version_guid": version_guid,
                    "retired_at": now,
                    "reason": "absent_from_snapshot",
                }
                existing_tombstone = state["tombstones"].get(object_id, {})
                tombstone_versions = existing_tombstone.get("versions", {}) if isinstance(existing_tombstone, dict) else {}
                tombstone_versions[version_guid] = dict(tombstone)
                tombstone["versions"] = tombstone_versions
                state["tombstones"][object_id] = tombstone
                has_active_version = any(
                    version.get("active", True)
                    for version in entry.get("versions", {}).values()
                )
                entry["active"] = has_active_version
                if not has_active_version:
                    records_by_object.pop(object_id, None)
                    indexes.pop(object_id, None)
                    object_path = object_paths.pop(object_id, None)
                    if object_path:
                        _remove_path(destination / object_path)
            for object_id in current_ids:
                entry = state["objects"].get(object_id)
                if entry:
                    entry["active"] = True
                    version_state = entry.get("versions", {}).get(version_guid)
                    if version_state:
                        version_state["active"] = True
                        version_state.pop("retired_at", None)
                        version_state.pop("retirement", None)
                    tombstone = state["tombstones"].get(object_id)
                    if isinstance(tombstone, dict):
                        tombstone_versions = tombstone.get("versions", {})
                        tombstone_versions.pop(version_guid, None)
                        if tombstone_versions:
                            latest = dict(next(reversed(tombstone_versions.values())))
                            latest["versions"] = tombstone_versions
                            state["tombstones"][object_id] = latest
                        else:
                            state["tombstones"].pop(object_id, None)
        processed, skipped = 0, 0
        for index, obj in enumerate(objects, 1):
            guid = obj.attrib.get("guid")
            object_id = (f"object:{guid}" if guid and guid_counts.get(guid, 0) == 1 else _stable_id("object", guid or "", obj.attrib.get("fullyQualifiedName", ""), obj.attrib.get("type", "")))
            fingerprint = _object_hash(obj)
            entry = state["objects"].setdefault(object_id, {"guid": guid, "versions": {}, "import_count": 0})
            prior = entry.get("versions", {}).get(version_guid, {})
            should_skip = (
                not reprocess_all
                and prior.get("object_hash") == fingerprint
                and prior.get("redact_source", False) == redact_source
                and prior.get("preserve_raw", True) == preserve_raw
                and any(r.get("record_type") == "object" for r in records_by_object.get(object_id, []))
                and contract_current
            )
            if should_skip:
                skipped += 1
                entry.update({"last_seen": now, "import_count": entry.get("import_count", 0) + 1})
                prior.update({"last_seen": now, "import_count": prior.get("import_count", 0) + 1, "source_filename": source.name, "source_hash": source_hash})
                obj_record = next(r for r in records_by_object[object_id] if r.get("record_type") == "object")
                indexes.setdefault(object_id, {"id": object_id, "guid": guid, "name": obj_record.get("name"), "module": obj_record.get("module"), "fully_qualified_name": obj_record.get("fully_qualified_name"), "type": obj_record.get("attributes", {}).get("type"), "object_kind": obj_record.get("object_kind", "unknown"), "part_kind_counts": obj_record.get("semantic_counts", {}).get("parts_by_kind", {}), "path": obj_record.get("normalized_path", "")})
                reporter.object(index, len(objects), object=obj_record.get("fully_qualified_name", obj.attrib.get("name", object_id)), processed=processed, skipped=skipped)
                continue
            processed += 1
            old_path = next((r.get("normalized_path") for r in records_by_object.get(object_id, []) if r.get("record_type") == "object"), None)
            old_path_value = _legacy_output_path(destination, old_path, "normalized_path") if old_path else None
            if old_path_value and old_path != "" and old_path_value.exists():
                shutil.rmtree(old_path_value)
            qualified = obj.attrib.get("fullyQualifiedName", obj.attrib.get("name", f"object-{index}"))
            path_qualified = _redact_value(qualified) if redact_source else qualified
            parent = obj.attrib.get("parent")
            module, _, directory_name = _object_path_parts(
                path_qualified, guid, object_id in collision_ids, collision_identity=object_id, parent=parent
            )
            object_paths[object_id] = f"objects/{module}/{directory_name}"
            written = _write_object(destination, root, obj, index, redact_source, object_id in collision_ids, object_id, gx9_catalog, element_paths)
            summary, object_records, references, variable_dependencies = written
            for record in object_records:
                if record.get("record_type") == "object":
                    record["normalized_path"] = object_paths[object_id]
                elif record.get("record_type") == "part":
                    record["normalized_file"] = record["normalized_file"].replace(
                        "objects/" + module + "/" + directory_name + "/", object_paths[object_id] + "/"
                    )
            summary["path"] = object_paths[object_id]
            for dependency in variable_dependencies:
                dependency["record_type"] = "dependency"
                dependency["object_hash"] = fingerprint
            for record in object_records + references:
                record["object_hash"] = fingerprint
                record["version_guid"] = version_guid
            records_by_object[object_id] = object_records + references + variable_dependencies
            indexes[object_id] = summary
            entry.update({"guid": guid, "active": True, "last_seen": now, "import_count": entry.get("import_count", 0) + 1})
            entry.setdefault("versions", {})[version_guid] = {"guid": version_guid, "name": version_name, "object_hash": fingerprint, "active": True, "last_seen": now, "import_count": prior.get("import_count", 0) + 1, "path": summary["path"], "source_filename": safe_source_name, "source_hash": source_hash, "redact_source": redact_source, "preserve_raw": preserve_raw}
            reporter.object(index, len(objects), object=qualified, processed=processed, skipped=skipped)

        # A byte-for-byte identical import with the same output policy has no
        # derived work to commit.  In particular, do not rewrite timestamps,
        # manifests, ledgers, or graph/index projections just because the
        # source was presented a second time.
        if processed == 0 and skipped == len(objects) and not retired_ids:
            # _prepare_input necessarily materializes the current source in
            # staging.  It is removed before commit when raw is disabled, so
            # its presence here does not invalidate an already share-safe
            # output.
            raw_policy_matches = raw.exists() if preserve_raw else True
            manifest_path = destination / "manifest.json"
            manifest_policy_matches = False
            if manifest_path.exists():
                try:
                    manifest_policy_matches = json.loads(manifest_path.read_text(encoding="utf-8")).get("share_safe") is share_safe
                except (json.JSONDecodeError, OSError):
                    manifest_policy_matches = False
            state_already_share_safe = bool(state.get("share_safe"))
            if raw_policy_matches and manifest_policy_matches and (not share_safe or state_already_share_safe):
                # Validate before the no-op return: share-safe is an export
                # boundary, not permission to trust stale derived files.
                try:
                    validate_output(destination)
                except (GXKBError, FileNotFoundError, json.JSONDecodeError):
                    pass
                else:
                    return final_destination

        # Keep prior objects and regenerate derived dependency/graph projections globally.
        reporter.emit("dependency_resolution", "Resolving dependencies", total=len(records_by_object), processed=processed, skipped=skipped)
        reporter.emit("projections_write", "Writing canonical and graph projections", total=len(records_by_object), processed=processed, skipped=skipped)
        projection_result = build_canonical_and_graph(
            records_by_object, indexes, object_paths, destination, version_guid,
            CANONICAL_SCHEMA_VERSION, _stable_id, _inferred_dependency_id, _json_write, _jsonl_write,
        )
        canonical_objects = projection_result["canonical_objects"]
        object_records = projection_result["object_records"]
        part_records = projection_result["part_records"]
        references = projection_result["references"]
        canonical_dependencies = projection_result["canonical_dependencies"]
        dependencies_by_object = projection_result["dependencies_by_object"]
        for item in indexes.values():
            item["path"] = object_paths.get(item["id"], item.get("path", ""))
        canonical_dir, graph_dir = destination / "canonical", destination / "graph"
        for record in canonical_objects:
            record.setdefault("schema_version", CANONICAL_SCHEMA_VERSION)
        # The builder has already materialized canonical records, graph data,
        # and per-object dependency projections. Continue with the existing
        # manifest/state/commit orchestration below.
        source_info = {"source_input_path": safe_source_name if redact_source else str(source), "kind": document.source_kind, "sha256": source_hash}
        if preserve_raw and raw.exists():
            if redact_source:
                # Keep one sanitized XML provenance file per import. XPZ
                # binaries are removed; the selected XML is retained safely.
                _redact_raw_history(destination)
                source_info["raw"] = str(document.xml_path.relative_to(destination)).replace("\\", "/")
            else:
                source_info["raw"] = _unique_raw_copy(source, raw)
        elif not preserve_raw and raw.exists(): shutil.rmtree(raw)
        raw_path = source_info.get("raw") if preserve_raw else None
        raw_kind = "xml_selected" if redact_source and document.source_kind == "xpz" else document.source_kind
        for object_entry in state.get("objects", {}).values():
            for historical_version in object_entry.get("versions", {}).values():
                if share_safe:
                    historical_version["raw_path"] = None
                    historical_version["raw_redacted"] = False
                    historical_version["raw_kind"] = None
                    continue
                if redact_source and historical_version.get("raw_path"):
                    historical_version["raw_redacted"] = True
                    if historical_version.get("raw_kind") == "xpz":
                        historical_path = _legacy_output_path(destination, historical_version["raw_path"], "historical raw_path")
                        if not historical_path.exists():
                            candidates = sorted(raw.glob(f"selected-{historical_path.stem}*.xml"))
                            if candidates:
                                historical_version["raw_path"] = str(candidates[0].relative_to(destination)).replace("\\", "/")
                                historical_version["raw_kind"] = "xml_selected"
        current_object_ids = {
            f"object:{obj.attrib['guid']}" if obj.attrib.get("guid") and guid_counts.get(obj.attrib["guid"], 0) == 1
            else _stable_id("object", obj.attrib.get("guid", ""), obj.attrib.get("fullyQualifiedName", ""), obj.attrib.get("type", ""))
            for obj in objects
        }
        for object_id in current_object_ids:
            current_version = state.get("objects", {}).get(object_id, {}).get("versions", {}).get(version_guid)
            if current_version is not None:
                current_version.update({"raw_path": raw_path, "raw_redacted": bool(raw_path and redact_source), "raw_kind": raw_kind})
        object_kind_counts: dict[str, int] = {}; part_kind_counts: dict[str, int] = {}
        for item in indexes.values():
            object_kind_counts[item.get("object_kind", "unknown")] = object_kind_counts.get(item.get("object_kind", "unknown"), 0) + 1
            for kind, count in item.get("part_kind_counts", {}).items(): part_kind_counts[kind] = part_kind_counts.get(kind, 0) + count
        semantic_counts = {"objects_by_kind": object_kind_counts, "parts_by_kind": part_kind_counts}
        for record in canonical_objects:
            record.setdefault("schema_version", CANONICAL_SCHEMA_VERSION)
        safe_versions = _redact_value(versions) if redact_source else versions
        reconciliation = {"mode": "snapshot" if snapshot else "partial", "scope": "kb-version", "complete_input": snapshot, "retired_objects": sorted(retired_ids), "retired_count": len(retired_ids)}
        manifest = {"schema_version": OUTPUT_SCHEMA_VERSION, "canonical_schema_version": CANONICAL_SCHEMA_VERSION, "share_safe": share_safe, "source": source_info, "source_metadata": _redact_value(source_metadata) if redact_source else source_metadata, "kb": {"guid": kb_guid}, "versions": safe_versions, "version": _redact_value({"guid": version_guid, "name": version_name}) if redact_source else {"guid": version_guid, "name": version_name}, "object_count": len(indexes), "dependency_count": len(canonical_dependencies), "processed_objects": processed, "skipped_objects": skipped, "semantic_counts": semantic_counts, "warnings": _redact_value(document.warnings) if redact_source else document.warnings, "errors": [], "incremental": {"absent_objects_retained": not snapshot, "reconciliation": reconciliation, "reprocess_all": reprocess_all}, "outputs": {"canonical_records": "canonical/records.jsonl", "canonical_manifest": "canonical/manifest.json", "graph_nodes": "graph/nodes.jsonl", "graph_edges": "graph/edges.jsonl", "state": "kb-state.json"}}
        _json_write(canonical_dir / "manifest.json", {"schema_version": CANONICAL_SCHEMA_VERSION, "records": "records.jsonl", "record_counts": {"objects": len(object_records), "parts": len(part_records), "references": len(references), "dependencies": len(canonical_dependencies)}, "semantic_counts": semantic_counts, "kb": manifest["kb"], "versions": safe_versions, "reconciliation": reconciliation, "graph": {"nodes": "../graph/nodes.jsonl", "edges": "../graph/edges.jsonl"}})
        state.setdefault("imports", []).append({"timestamp": now, "source": source_info, "version": {"guid": version_guid, "name": version_name}, "processed_objects": processed, "skipped_objects": skipped, "reconciliation": reconciliation})
        _json_write(destination / "manifest.json", manifest)
        if redact_source:
            # A redacted import must also sanitize provenance retained from
            # earlier, unredacted imports; raw_path values remain relative.
            state = _redact_state_value(state)
            if share_safe:
                state["share_safe"] = True
                for import_entry in state.get("imports", []):
                    if isinstance(import_entry.get("source"), dict):
                        import_entry["source"]["raw"] = None
        _json_write(state_path, state)
        _atomic_write(
            destination / "objects-index.jsonl",
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in sorted(indexes.values(), key=lambda value: value.get("id", ""))),
        )
        if redact_source:
            _redact_existing_output(destination)
        reporter.emit("validation", "Validating generated output", processed=processed, skipped=skipped)
        validate_output(destination)
        reporter.emit("commit", "Committing generated output", processed=processed, skipped=skipped)
        _commit_staged_output(destination, final_destination)
        reporter.emit("complete", "Normalization completed", total=len(objects), processed=processed, skipped=skipped)
        return final_destination
    finally:
        if document is not None and document.temporary_dir is not None: document.temporary_dir.cleanup()
        staging_context.cleanup()
