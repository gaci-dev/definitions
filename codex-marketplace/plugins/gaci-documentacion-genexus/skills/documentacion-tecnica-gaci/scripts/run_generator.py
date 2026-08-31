#!/usr/bin/env python3
"""Ejecuta el generador corporativo de Gaci desde un checkout de definitions."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


GENERATOR_RELATIVE = Path("tools/generador-documentacion/generar_documentacion.py")
BUNDLED_GENERATOR = Path(__file__).resolve().parents[1] / "assets" / "generador-documentacion" / "generar_documentacion.py"


def resolve_generator(explicit: Path | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(explicit)
    configured = os.environ.get("GACI_DEFINITIONS_REPO")
    if configured:
        candidates.append(Path(configured))
    for candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if (resolved / GENERATOR_RELATIVE).is_file():
            return resolved / GENERATOR_RELATIVE

    if BUNDLED_GENERATOR.is_file():
        return BUNDLED_GENERATOR

    for candidate in (Path.cwd(), *Path.cwd().parents):
        resolved = candidate.resolve()
        if (resolved / GENERATOR_RELATIVE).is_file():
            return resolved / GENERATOR_RELATIVE

    raise SystemExit(
        "No se encontro el generador corporativo incluido. Reinstale el plugin o "
        "pase --definitions-repo con la ruta de un checkout valido."
    )


def expected_outputs(spec_path: Path, output_dir: Path, basename_override: str | None) -> tuple[Path, Path]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    basename = basename_override or spec.get("output", {}).get("basename", "documentacion")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", str(basename)).strip("._") or "documentacion"
    return output_dir / f"{safe}.pdf", output_dir / f"{safe}_editable.docx"


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta el generador corporativo de documentacion Gaci")
    parser.add_argument("input", type=Path, help="JSON compatible con el generador")
    parser.add_argument("--definitions-repo", type=Path, help="Ruta al checkout del repositorio definitions")
    parser.add_argument("--output-dir", type=Path, help="Carpeta de salida; por defecto, junto al JSON")
    parser.add_argument("--basename", help="Nombre base de salida")
    parser.add_argument("--no-logo", action="store_true", help="Genera sin el logo corporativo")
    args = parser.parse_args()

    input_path = args.input.expanduser().resolve()
    if not input_path.is_file():
        raise SystemExit(f"No existe el JSON de entrada: {input_path}")
    json.loads(input_path.read_text(encoding="utf-8"))

    generator = resolve_generator(args.definitions_repo)
    output_dir = (args.output_dir or input_path.parent).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [sys.executable, str(generator), str(input_path), "--output-dir", str(output_dir)]
    if args.basename:
        command.extend(("--basename", args.basename))
    if args.no_logo:
        command.append("--no-logo")

    completed = subprocess.run(command, check=False)
    if completed.returncode:
        raise SystemExit(completed.returncode)

    pdf, docx = expected_outputs(input_path, output_dir, args.basename)
    missing = [str(path) for path in (pdf, docx) if not path.is_file()]
    if missing:
        raise SystemExit("El generador termino sin crear: " + ", ".join(missing))

    print(pdf)
    print(docx)


if __name__ == "__main__":
    main()
