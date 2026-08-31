# GXKB

GXKB es una herramienta Python portátil y autocontenida que normaliza exportaciones XML y XPZ de GeneXus en una base de conocimiento legible y procesable por máquinas. También adapta selecciones GXL opcionales de GeneXus 9.

## Inicio rápido

```powershell
cd tools\kb-extractor
py -3 -m venv .venv
\.venv\Scripts\python -m pip install -e ".[test]"
\.venv\Scripts\python -m gxkb path\to\export.xml -o normalized-kb
\.venv\Scripts\python -m pytest
```

Use `python -m gxkb` o la API directamente:

```python
from gxkb.normalizer import normalize, validate_output

output = normalize("export.xpz", "normalized-kb", preserve_raw=False)
validate_output(output)
```

Se conservan los puntos de entrada de compatibilidad `gxkb.normalizer.normalize` y `validate_output`.

## Requisitos

- Python 3.10 o posterior
- Biblioteca estándar durante la ejecución
- `pytest>=8` únicamente para el extra de pruebas

Las entradas deben ser `.xml` o `.xpz`. La selección de XML dentro de XPZ es determinista; pase `--xml-member` para elegir un miembro explícitamente. Para exportaciones GX9, pase un `.gxl` opcional con `--gxl`; filtra objetos y no se importa como contenido de la KB.

## Salida

La herramienta escribe registros JSONL canónicos, proyecciones legibles por objeto, JSONL del grafo, un índice de objetos, un manifiesto y el estado incremental. Consulte [docs/output-layers.md](docs/output-layers.md), [docs/object-types.md](docs/object-types.md), [docs/input-flow.md](docs/input-flow.md) y [docs/architecture.md](docs/architecture.md).

Las importaciones son incrementales y acumulativas de forma predeterminada. Los objetos sin cambios pueden omitirse, las entradas parciales no eliminan objetos ausentes y `--reprocess-all` fuerza el procesamiento. Use `--snapshot` únicamente cuando la entrada esté completa para su ámbito de KB/versión; retira los objetos ausentes mientras conserva el historial.

## Uso seguro para compartir

El modo normal conserva la entrada de origen en `raw/` para auditoría y reprocesamiento. Antes de compartir la salida, use `--share-safe`:

```powershell
python -m gxkb private-export.xpz -o shared-kb --share-safe
```

Esto implica no conservar datos sin procesar y aplicar redacción al origen y la procedencia, incluida la procedencia histórica conservada. La redacción cubre rutas absolutas de Windows, UNC y POSIX compatibles, así como determinados valores similares a identidades, pero no es un detector general de secretos. Inspeccione el resultado y no considere la salida segura para compartir como prueba de que no existen secretos arbitrarios.

## Verificación

```powershell
cd tools\kb-extractor
py -3 -m pytest
py -3 -m gxkb tests\fixtures\biller_procedure_sample.xml -o $env:TEMP\gxkb-smoke --without-raw --redact-source --quiet
py -3 -c "from gxkb.normalizer import validate_output; validate_output(r'$env:TEMP\gxkb-smoke')"
```

El fixture es un ejemplo XML portátil y seguro para compartir. No agregue salidas generadas, exportaciones sin procesar, fixtures privados, cachés ni archivos `.atl` a este directorio.
