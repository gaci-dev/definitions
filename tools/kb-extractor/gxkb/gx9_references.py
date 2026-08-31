"""Conservative lexical reference extraction for GeneXus 9 source."""

from __future__ import annotations

import re
from bisect import bisect_right
from dataclasses import dataclass
from typing import Any


IDENT = r"[A-Za-z_][A-Za-z0-9_.$-]*"
_TOKEN = re.compile(IDENT)
_FOR_EACH = re.compile(r"\bFOR\s+EACH\s+(?P<header>.*?)(?=\bWHERE\b|\bDEFINED\s+BY\b|\Z)", re.I | re.S)
_CALL = re.compile(r"\bCALL\s*\(\s*(?P<target>" + IDENT + r")\s*\)|(?P<method>" + IDENT + r")\s*\.\s*Call\s*\(", re.I)
_CONDITION = re.compile(r"\b(?:WHERE|DEFINED\s+BY)\b(?P<body>.*?)(?=\b(?:FOR\s+EACH|WHERE|DEFINED\s+BY|END\s+FOR|CALL)\b|$)", re.I | re.S)


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    line: int
    column: int
    end_line: int
    end_column: int

    def as_dict(self) -> dict[str, int]:
        return {"start": self.start, "end": self.end, "line": self.line, "column": self.column,
                "end_line": self.end_line, "end_column": self.end_column}


def mask_source(source: str) -> str:
    """Mask comments and literals, retaining newlines and character offsets."""
    result = list(source)
    i = 0
    quote: str | None = None
    while i < len(source):
        if quote:
            if source[i] == quote:
                if i + 1 < len(source) and source[i + 1] == quote:
                    result[i] = result[i + 1] = " "
                    i += 2
                    continue
                quote = None
            if source[i] not in "\r\n":
                result[i] = " "
            i += 1
            continue
        if source[i] in "'\"":
            quote = source[i]
            result[i] = " "
            i += 1
            continue
        if source.startswith("//", i):
            while i < len(source) and source[i] not in "\r\n":
                result[i] = " "
                i += 1
            continue
        if source.startswith("/*", i):
            result[i] = result[i + 1] = " "
            i += 2
            while i < len(source) and not source.startswith("*/", i):
                if source[i] not in "\r\n":
                    result[i] = " "
                i += 1
            if i < len(source):
                result[i] = result[i + 1] = " "
                i += 2
            continue
        i += 1
    return "".join(result)


def _span(source: str, start: int, end: int, line_starts: list[int] | None = None) -> Span:
    line_starts = line_starts or [0] + [index + 1 for index, char in enumerate(source) if char == "\n"]
    line_index = bisect_right(line_starts, start) - 1
    end_line_index = bisect_right(line_starts, end) - 1
    line = line_index + 1
    end_line = end_line_index + 1
    column = start - line_starts[line_index] + 1
    end_column = end - line_starts[end_line_index] + 1
    return Span(start, end, line, column, end_line, end_column)


def _source_parts(part: Any) -> list[str]:
    sources = ["".join(node.itertext()) for node in part.iter() if node.tag.rsplit("}", 1)[-1] == "Source"]
    return sources or ["".join(part.itertext())]


def _names(text: str) -> list[str]:
    return [match.group(0) for match in _TOKEN.finditer(text)]


def extract(source: str, known_attributes: set[str], header_attributes: set[str]) -> list[dict[str, Any]]:
    """Return only FOR EACH, strong calls, and catalog-backed attributes."""
    masked = mask_source(source)
    line_starts = [0] + [index + 1 for index, char in enumerate(source) if char == "\n"]
    found: list[dict[str, Any]] = []
    allowed = {name.casefold() for name in known_attributes | header_attributes}
    for match in _FOR_EACH.finditer(masked):
        header = _names(match.group("header"))
        if not header:
            continue
        target = header[0]
        span = _span(source, match.start(), match.end(), line_starts)
        found.append({"reference_kind": "for_each", "target_kind": "object", "target_name": target,
                      "relation": "gx9_for_each", "span": span.as_dict(), "evidence": source[match.start():match.end()].strip()})
        new_attributes = {name for name in header[1:] if name.casefold() in {item.casefold() for item in known_attributes}}
        header_attributes.update(new_attributes)
        allowed.update(name.casefold() for name in new_attributes)

    for match in _CALL.finditer(masked):
        target = match.group("target") or match.group("method")
        start, end = match.span("target" if match.group("target") else "method")
        span = _span(source, start, end, line_starts)
        found.append({"reference_kind": "call", "target_kind": "object", "target_name": target,
                      "relation": "gx9_call", "span": span.as_dict(), "evidence": source[match.start():match.end()].strip()})

    mention_spans: set[tuple[int, int]] = set()
    keywords = {"and", "or", "not", "in", "is", "null", "true", "false", "defined", "by", "where"}
    for condition in _CONDITION.finditer(masked):
        for token in _TOKEN.finditer(condition.group("body")):
            absolute_start = condition.start("body") + token.start()
            if (token.group(0).casefold() not in allowed and token.group(0).casefold() in keywords) or source[max(0, absolute_start - 4):absolute_start].rstrip().endswith("&"):
                continue
            key = token.span()
            if key in mention_spans:
                continue
            mention_spans.add(key)
            body_offset = condition.start("body")
            span = _span(source, body_offset + token.start(), body_offset + token.end(), line_starts)
            found.append({"reference_kind": "attribute", "target_kind": "attribute", "target_name": token.group(0),
                          "relation": "gx9_attribute_mention", "span": span.as_dict(), "evidence": source[body_offset + token.start():body_offset + token.end()]})
    return sorted(found, key=lambda item: (item["span"]["start"], item["relation"], item["target_name"]))


def catalog(objects: list[Any], guid_counts: dict[str, int], structure_attributes: Any) -> dict[str, Any]:
    """Build object aliases and attribute owners from the adapted KB tree."""
    object_names: dict[str, list[str]] = {}
    attributes: dict[str, set[str]] = {}
    for obj in objects:
        guid = obj.attrib.get("guid")
        object_id = (f"object:{guid}" if guid and guid_counts.get(guid, 0) == 1 else
                     _stable_object_id(guid or "", obj.attrib.get("fullyQualifiedName", ""), obj.attrib.get("type", "")))
        for name in {obj.attrib.get("fullyQualifiedName"), obj.attrib.get("name"), obj.attrib.get("legacy_name") } - {None, ""}:
            object_names.setdefault(name, []).append(object_id)
        attrs = structure_attributes(obj)
        for name in attrs:
            attributes.setdefault(name.casefold(), set()).add(object_id)
    return {"objects": object_names, "attributes": attributes}


def _stable_object_id(guid: str, fqn: str, kind: str) -> str:
    import hashlib
    return "object:" + hashlib.sha256("\x1f".join((guid, fqn, kind)).encode()).hexdigest()[:20]
