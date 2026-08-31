"""Compatibility adapter for GeneXus 9 XML exports and GXL selections."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from typing import Any, Callable


LEGACY_OBJECT_KINDS = {
    "Transaction": "transaction",
    "DataView": "data_view",
    "Report": "report",
    "Folder": "folder",
    "Table": "table",
    "Group": "group",
    "Procedure": "procedure",
    "WorkPanel": "webpanel",
    "Menubar": "menu_bar",
}

LEGACY_PART_TYPES = {
    "Structure": "gx9:structure",
    "Variable": "gx9:variables",
    "Form": "gx9:form",
    "Events": "gx9:events",
    "Rules": "gx9:rules",
    "Documentation": "gx9:documentation",
    "Table": "gx9:table",
    "Report": "gx9:report",
    "FormInfo": "gx9:report",
}

LEGACY_NAME_PREFIXES = {
    "Report": "R",
    "Transaction": "T",
}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def is_gx9_export(root: ET.Element) -> bool:
    return any(local_name(node.tag) == "GXObject" for node in root.iter())


def selection_names(path: Path) -> tuple[set[str], list[str]]:
    """Read GXL names; the file is a selection/index, never KB content."""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"Invalid GXL XML: {path}: {exc}") from exc
    names = {
        ((node.attrib.get("ObjName") or "") if local_name(node.tag) != "ObjName" else "".join(node.itertext())).strip()
        for node in root.iter()
        if local_name(node.tag) == "ObjName" or "ObjName" in node.attrib
    }
    names.discard("")
    return names, []


def _normalized_name(kind_name: str, serialized_name: str) -> str:
    prefix = LEGACY_NAME_PREFIXES.get(kind_name)
    if prefix and serialized_name.startswith(prefix) and len(serialized_name) > len(prefix):
        return serialized_name[len(prefix):]
    return serialized_name


def _code_parts(class_node: ET.Element) -> list[ET.Element]:
    """Materialize nested GX9 CodeBlock sources without discarding their parent."""
    parts: list[ET.Element] = []
    for code_block in class_node.iter():
        if local_name(code_block.tag) != "CodeBlock":
            continue
        source = next((node for node in code_block if local_name(node.tag) == "Source"), None)
        if source is None:
            continue
        part = ET.Element("Part", {"type": "gx9:code", "legacy_container": "CodeBlock"})
        part.append(deepcopy(code_block))
        parts.append(part)
    return parts


def _text(node: ET.Element | None) -> str:
    return "" if node is None else "".join(node.itertext()).strip()


def _attrs(node: ET.Element, redact: Callable[[str, str], str] | None) -> dict[str, Any]:
    return {key: redact(value, key) if redact else value for key, value in node.attrib.items()}


def _legacy_attribute(name: str, redact: Callable[[str, str], str] | None) -> dict[str, Any]:
    is_key = name.endswith("*")
    clean_name = name[:-1].strip() if is_key else name.strip()
    item: dict[str, Any] = {"name": redact(clean_name, "name") if redact else clean_name}
    if is_key:
        item["key"] = True
    return item


def _legacy_structure_text(text: str, redact: Callable[[str, str], str] | None) -> tuple[list[dict[str, Any]], list[str]]:
    """Conservatively parse the parenthesized GX9 structure notation.

    The grammar varied between GX9 exporters. Groups become levels when their
    boundaries are balanced; every token remains represented either as an
    attribute or in ``unknown_fragments``.
    """
    levels: list[dict[str, Any]] = []
    unknown: list[str] = []
    token = re.compile(r"[A-Za-z_][\w.$-]*(?:\*)?")

    def parse_group(value: str, name: str | None = None) -> None:
        items: list[dict[str, Any]] = []
        level: dict[str, Any] | None = None
        if name is None:
            level = {"name": None, "attributes": {}, "properties": {}, "items": items}
            levels.append(level)
        else:
            level = {"name": name, "attributes": {}, "properties": {}, "items": items}
            levels.append(level)
        pos = 0
        while pos < len(value):
            while pos < len(value) and (value[pos].isspace() or value[pos] in ",;"):
                pos += 1
            match = token.match(value, pos)
            if match:
                candidate = match.group(0)
                pos = match.end()
                while pos < len(value) and value[pos].isspace():
                    pos += 1
                if pos < len(value) and value[pos] == "(":
                    end = _matching_parenthesis(value, pos)
                    if end is None:
                        unknown.append(value[pos:].strip())
                        items.append(_legacy_attribute(candidate, redact))
                        break
                    parse_group(value[pos + 1:end], candidate)
                    pos = end + 1
                else:
                    items.append(_legacy_attribute(candidate, redact))
                continue
            if pos < len(value) and value[pos] == "(":
                end = _matching_parenthesis(value, pos)
                if end is None:
                    unknown.append(value[pos:].strip())
                    break
                parse_group(value[pos + 1:end])
                pos = end + 1
                continue
            end = min((index for index in (value.find(",", pos), value.find(";", pos), value.find("(", pos)) if index >= 0), default=len(value))
            fragment = value[pos:end].strip()
            if fragment:
                unknown.append(fragment)
            pos = end
        if not items and name is None and level in levels:
            levels.remove(level)

    def _matching_parenthesis(value: str, start: int) -> int | None:
        depth = 0
        for index in range(start, len(value)):
            if value[index] == "(":
                depth += 1
            elif value[index] == ")":
                depth -= 1
                if depth == 0:
                    return index
        return None

    parse_group(text)
    return levels, unknown


def legacy_structure_projection(part: ET.Element, redact: Callable[[str, str], str] | None = None, raw: Callable[[ET.Element], str] | None = None) -> dict[str, Any]:
    """Project GX9 Structure syntax without discarding its serialized form."""
    levels: list[dict[str, Any]] = []
    unknown_fragments: list[str] = []
    explicit_levels = [node for node in part.iter() if local_name(node.tag) == "Level"]
    for level in explicit_levels:
        items = []
        for node in level.iter():
            if local_name(node.tag) not in {"Attribute", "Item"} or node is level:
                continue
            item = _attrs(node, redact)
            name = _text(node)
            if name:
                item["name"] = redact(name, "name") if redact else name
            if name.endswith("*"):
                item["name"] = (redact(name[:-1].strip(), "name") if redact else name[:-1].strip())
                item["key"] = True
            items.append(item)
        levels.append({"name": _attrs(level, redact).get("Name"), "attributes": _attrs(level, redact), "properties": {}, "items": items})
    if not explicit_levels:
        source = next((node for node in part.iter() if local_name(node.tag) == "Source"), None)
        text = _text(source) if source is not None else _text(part)
        levels, unknown_fragments = _legacy_structure_text(text, redact)
        level_names = [_text(node) for node in part.iter() if local_name(node.tag) == "LevelInfo" and _text(node)]
        for index, level in enumerate(levels):
            if index < len(level_names) and not level.get("name"):
                level["name"] = level_names[index]
    return {
        "kind": "legacy_structure",
        "levels": levels,
        "attribute_count": sum(len(level["items"]) for level in levels),
        "level_count": len(levels),
        "unknown_fragments": unknown_fragments,
        "raw_xml": raw(part) if raw else ET.tostring(part, encoding="unicode"),
    }


def legacy_variables_projection(part: ET.Element, redact: Callable[[str, str], str] | None = None, raw: Callable[[ET.Element], str] | None = None) -> dict[str, Any]:
    variables: list[dict[str, Any]] = []
    for variable in (node for node in part.iter() if local_name(node.tag) == "Variable"):
        attributes = _attrs(variable, redact)
        fields: dict[str, str] = {}
        for child in variable.iter():
            child_name = local_name(child.tag)
            if child_name and _text(child) and not list(child):
                fields[child_name] = _text(child)
        fields_lower = {key.lower(): value for key, value in fields.items()}
        name = attributes.get("Name") or attributes.get("name") or fields_lower.get("name")
        based_on = attributes.get("BasedOn") or attributes.get("basedon") or fields_lower.get("basedon") or fields_lower.get("based_on")
        variable_type = attributes.get("Type") or attributes.get("type") or fields_lower.get("type") or fields_lower.get("datatype") or fields_lower.get("vartype")
        variables.append({
            "name": redact(name, "name") if redact and name else name,
            "based_on": redact(based_on, "based_on") if redact and based_on else based_on,
            "type": redact(variable_type, "type") if redact and variable_type else variable_type,
            "attributes": attributes,
            "metadata": {key: redact(value, key) if redact else value for key, value in fields.items() if key.lower() not in {"name", "basedon", "based_on", "type", "datatype", "vartype"}},
            "raw": raw(variable) if raw else ET.tostring(variable, encoding="unicode"),
        })
    return {"kind": "legacy_variables", "variables": variables, "variable_count": len(variables), "raw_xml": raw(part) if raw else ET.tostring(part, encoding="unicode")}


def adapt(root: ET.Element, selected_names: set[str] | None = None) -> tuple[ET.Element, list[str]]:
    """Return a modern-shaped tree while retaining every legacy container."""
    warnings: list[str] = []
    if not is_gx9_export(root):
        return root, warnings

    adapted = deepcopy(root)
    objects = []
    for gx_object in adapted.iter():
        if local_name(gx_object.tag) != "GXObject":
            continue
        class_node = next((child for child in gx_object if local_name(child.tag) not in {"Info"}), None)
        if class_node is None:
            warnings.append("GX9 GXObject without a legacy class was preserved as unknown")
            continue
        info = next((child for child in class_node if local_name(child.tag) == "Info"), None)
        value = lambda name: (next((child for child in (info if info is not None else []) if local_name(child.tag) == name), None))
        name = "" if value("Name") is None else "".join(value("Name").itertext()).strip()
        description = "" if value("Description") is None else "".join(value("Description").itertext()).strip()
        folder = "" if value("Folder") is None else "".join(value("Folder").itertext()).strip()
        kind_name = local_name(class_node.tag)
        normalized_name = _normalized_name(kind_name, name)
        attrs = {
            "name": normalized_name or f"gx9-object-{len(objects) + 1}",
            "fullyQualifiedName": ".".join(part for part in (folder, normalized_name) if part) or f"gx9-object-{len(objects) + 1}",
            "parent": folder,
            "type": f"gx9:{kind_name.lower()}",
            "object_kind": LEGACY_OBJECT_KINDS.get(kind_name, "unknown"),
            "legacy_class": kind_name,
        }
        if name:
            attrs["legacy_name"] = name
        if description:
            attrs["description"] = description
        # GX9 has no modern GUID in the observed format. The normalizer's
        # stable fallback identity is therefore based on these source fields.
        gx_object.tag = "Object"
        gx_object.attrib.clear()
        gx_object.attrib.update(attrs)
        for child in list(class_node):
            if local_name(child.tag) == "Info":
                class_node.remove(child)
        for container in list(class_node):
            container_name = local_name(container.tag)
            part_type = LEGACY_PART_TYPES.get(container_name)
            if not part_type:
                continue
            part_attributes = {"type": part_type, "legacy_container": container_name}
            if any(local_name(node.tag) == "CodeBlock" for node in container.iter()):
                part_attributes["preserve_raw"] = "true"
            part = ET.Element("Part", part_attributes)
            part.append(deepcopy(container))
            gx_object.append(part)
        for code_part in _code_parts(class_node):
            gx_object.append(code_part)
        objects.append(gx_object)

    if selected_names is not None:
        aliases = {
            alias
            for obj in objects
            for alias in (obj.attrib.get("name", ""), obj.attrib.get("legacy_name", ""))
            if alias
        }
        missing = sorted(selected_names - aliases)
        if missing:
            warnings.append("GXL selection names not found in GX9 export: " + ", ".join(missing))
        for parent in adapted.iter():
            for child in list(parent):
                if child in objects and not ({child.attrib.get("name", ""), child.attrib.get("legacy_name", "")} & selected_names):
                    parent.remove(child)
        if not objects:
            warnings.append("GXL selection did not match any GX9 object")
    return adapted, warnings
