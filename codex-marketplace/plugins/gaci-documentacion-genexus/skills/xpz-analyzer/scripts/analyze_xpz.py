#!/usr/bin/env python3
"""Inventaria un XPZ de GeneXus sin importar ni ejecutar su contenido."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET


MAX_FILES = 5000
MAX_MEMBER_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
XML_SUFFIXES = {".xml", ".xsd"}

TYPE_NAMES = {
    "1db606f2-af09-4cf9-a3b5-b481519d28f6": "Transaction",
    "84a12160-f59b-4ad7-a683-ea4481ac23e9": "Procedure",
    "2a9e9aba-d2de-4801-ae7f-5e3819222daf": "DataProvider",
    "ffd44be7-3bb4-4d01-9e7e-d1c1a3c095af": "DataSelector",
    "19abc6ff-2cd2-0000-0006-6d172bc2333b": "DataView",
    "447527b5-9210-4523-898b-5dccb17be60a": "StructuredDataType",
    "00972a17-9975-449e-aab1-d26165d51393": "Domain",
    "b5f00807-9da8-4cf9-b408-7554f2b6a8ee": "BusinessProcessDiagram",
    "9fb193d9-64a4-4d30-b129-ff7c76830f7e": "Image",
    "88313f43-5eb2-0000-0028-e8d9f5bf9588": "Language",
    "c9584656-94b6-4ccd-890f-332d11fc2c25": "WebPanelFamily",
    "198e8ea4-1d49-4c9c-8a9a-417024baa9d1": "WorkPanel",
}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def safe_member(info: zipfile.ZipInfo) -> PurePosixPath:
    normalized = info.filename.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"Ruta insegura en el XPZ: {info.filename}")
    if info.flag_bits & 0x1:
        raise ValueError(f"No se admiten entradas cifradas: {info.filename}")
    if info.file_size > MAX_MEMBER_BYTES:
        raise ValueError(f"Entrada demasiado grande: {info.filename}")
    return path


def child_text(element: ET.Element, child: str) -> str | None:
    for node in element:
        if local_name(node.tag) == child and node.text:
            return node.text.strip()
    return None


def parse_xml(data: bytes, member: str) -> dict:
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        return {"member": member, "xml_error": str(exc), "objects": []}

    version: dict[str, str] = {}
    for node in root.iter():
        if local_name(node.tag) == "KMW":
            for key in ("MajorVersion", "MinorVersion", "Build"):
                value = child_text(node, key)
                if value is not None:
                    version[key] = value
            break

    objects = []
    for node in root.iter():
        if local_name(node.tag) != "Object":
            continue
        type_guid = node.get("type", "")
        parts = []
        for part in node:
            if local_name(part.tag) != "Part":
                continue
            sources = [s.text or "" for s in part.iter() if local_name(s.tag) == "Source"]
            parts.append(
                {
                    "type_guid": part.get("type"),
                    "source_count": len(sources),
                    "source_characters": sum(len(s) for s in sources),
                    "source_lines": sum(s.count("\n") + (1 if s else 0) for s in sources),
                }
            )
        objects.append(
            {
                "name": node.get("name"),
                "fully_qualified_name": node.get("fullyQualifiedName"),
                "description": node.get("description"),
                "parent": node.get("parent"),
                "type_guid": type_guid or None,
                "type_name": TYPE_NAMES.get(type_guid, "Unknown"),
                "last_update": node.get("lastUpdate"),
                "parts": parts,
            }
        )

    return {"member": member, "root": local_name(root.tag), "kmw": version, "objects": objects}


def main() -> None:
    parser = argparse.ArgumentParser(description="Analiza un XPZ de GeneXus en modo de solo lectura")
    parser.add_argument("xpz", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="Inventario JSON de salida")
    parser.add_argument("--extract-xml", type=Path, help="Extrae solamente XML/XSD a esta carpeta")
    args = parser.parse_args()

    xpz = args.xpz.expanduser().resolve()
    if not xpz.is_file():
        raise SystemExit(f"No existe el XPZ: {xpz}")
    if not zipfile.is_zipfile(xpz):
        raise SystemExit("El archivo no es un contenedor ZIP valido")

    documents = []
    file_entries = []
    with zipfile.ZipFile(xpz) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_FILES:
            raise SystemExit(f"El XPZ excede el limite de {MAX_FILES} entradas")
        total = sum(info.file_size for info in infos)
        if total > MAX_TOTAL_BYTES:
            raise SystemExit("El XPZ excede el limite total descomprimido de 256 MiB")

        extract_root = args.extract_xml.expanduser().resolve() if args.extract_xml else None
        if extract_root:
            extract_root.mkdir(parents=True, exist_ok=True)

        for info in infos:
            path = safe_member(info)
            if info.is_dir():
                continue
            suffix = Path(path.name).suffix.lower()
            file_entries.append({"name": str(path), "size": info.file_size, "xml": suffix in XML_SUFFIXES})
            if suffix not in XML_SUFFIXES:
                continue
            data = archive.read(info)
            documents.append(parse_xml(data, str(path)))
            if extract_root:
                target = (extract_root / Path(*path.parts)).resolve()
                if extract_root != target and extract_root not in target.parents:
                    raise SystemExit(f"Destino de extraccion inseguro: {path}")
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as source, target.open("wb") as destination:
                    shutil.copyfileobj(source, destination)

    objects = [obj for doc in documents for obj in doc.get("objects", [])]
    counts = Counter(obj["type_name"] for obj in objects)
    report = {
        "format": "gaci-genexus-xpz-inventory-v1",
        "archive": {"name": xpz.name, "files": len(file_entries), "uncompressed_bytes": sum(x["size"] for x in file_entries)},
        "object_count": len(objects),
        "counts_by_type": dict(sorted(counts.items())),
        "files": file_entries,
        "documents": documents,
        "warnings": [
            "Los nombres de tipo se basan en GUID observados en las muestras provistas y pueden variar por version.",
            "El inventario omite usuarios, GUID de KB, checksums y contenido fuente completo.",
        ],
    }

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
