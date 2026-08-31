"""Share-safe redaction and provenance sanitization primitives.

This module deliberately contains no output-writing or normalizer imports.  The
normalizer owns when and where sanitization is applied; this module owns the
recursive value and XML-element transformations used by those boundaries.
"""

from __future__ import annotations

import copy
import re
from typing import Any
from xml.etree import ElementTree as ET


REDACTED_ATTRIBUTE_NAMES = {"user", "username", "uncpath", "path"}
WINDOWS_PATH = re.compile(r"(?i)(?<![\w])(?:[a-z]:[\\/]|\\\\)[^\r\n\"'<>&]*")
DOMAIN_USER = re.compile(r"\b[A-Za-z0-9_.-]+\\[A-Za-z0-9_.-]+\b")
POSIX_PATH = re.compile(
    r"(?<![\w])/(?:[A-Za-z0-9._~-]+(?:[ \t]+[A-Za-z0-9._~-]+)*/)+"
    r"[A-Za-z0-9._~-]+(?:[ \t]+[A-Za-z0-9._~-]+)*(?=$|[\s\"'<>&,;:!?()\[\]])"
)
INTERNAL_PATH_KEYS = {"normalized_path", "normalized_file", "output_path", "raw_path"}
INTERNAL_PATH_ROOTS = ("objects/", "raw/", "canonical/", "graph/")


def redact_value(value: Any, attribute_name: str | None = None) -> Any:
    if isinstance(value, dict):
        return {key: redact_value(item, str(key)) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if not isinstance(value, str):
        return value
    if attribute_name and attribute_name.lower() in REDACTED_ATTRIBUTE_NAMES:
        return "[REDACTED]"
    value = WINDOWS_PATH.sub("[REDACTED_PATH]", value)
    value = POSIX_PATH.sub("[REDACTED_PATH]", value)
    return DOMAIN_USER.sub("[REDACTED_USER]", value)


def is_absolute_path(value: str) -> bool:
    return bool(re.match(r"(?i)^(?:[a-z]:[\\/]|\\\\|/)", value))


def redact_state_value(value: Any, key: str | None = None) -> Any:
    """Redact provenance while retaining references inside the output tree."""
    if isinstance(value, dict):
        return {name: redact_state_value(item, str(name)) for name, item in value.items()}
    if isinstance(value, list):
        return [redact_state_value(item) for item in value]
    if not isinstance(value, str):
        return value
    key_name = (key or "").lower()
    if key_name == "source_filename":
        return "[REDACTED_INPUT]"
    if key_name in INTERNAL_PATH_KEYS or key_name == "path":
        return redact_value(value) if is_absolute_path(value) else value
    if key_name == "source_input_path":
        return redact_value(value)
    return redact_value(value, key)


def redact_output_value(value: Any, key: str | None = None) -> Any:
    """Redact output content without destroying generated relative paths."""
    if isinstance(value, dict):
        return {name: redact_output_value(item, str(name)) for name, item in value.items()}
    if isinstance(value, list):
        return [redact_output_value(item) for item in value]
    if not isinstance(value, str):
        return value
    key_name = (key or "").lower()
    if key_name in INTERNAL_PATH_KEYS:
        return value if not is_absolute_path(value) else redact_value(value)
    if key_name == "path" and value.startswith(INTERNAL_PATH_ROOTS):
        return value
    return redact_value(value, key)


def redacted_element(element: ET.Element) -> ET.Element:
    result = copy.deepcopy(element)
    # deepcopy keeps descendants, so sanitize each node from its matching source.
    for source, target in zip(element.iter(), result.iter()):
        target.attrib.clear()
        target.attrib.update({key: redact_value(value, key) for key, value in source.attrib.items()})
        if target.text:
            target.text = redact_value(target.text)
        if target.tail:
            target.tail = redact_value(target.tail)
    return result
