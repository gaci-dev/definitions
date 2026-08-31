# Capas de salida

`canonical/records.jsonl` es la fuente de verdad. Cada otra salida se deriva para un consumidor específico.

| Capa | Contenido |
|---|---|
| `canonical/` | Registros JSONL versionados de objetos, partes, referencias y dependencias |
| `objects/` | Markdown legible para personas, origen GeneXus, proyecciones JSON y partes serializadas |
| `graph/` | Nodos y aristas JSONL de objetos, partes y dependencias resueltas de forma unívoca |
| `raw/` | Entrada XML/XPZ original o historial XML sanitizado, según la política de conservación |
| Raíz de salida | `manifest.json`, `kb-state.json` y `objects-index.jsonl` |

Los registros canónicos usan `schema_version: 1` e identificadores estables. `canonical/manifest.json` informa los conteos de registros. La validación comprueba los campos obligatorios, la pertenencia, las rutas de proyección, los destinos de dependencias y la coherencia del grafo antes de confirmar la salida preparada.

Los directorios de objetos pueden contener `metadata.json`, `object.md`, `code.gx`, `rules.gx`, `events.gx`, `variables/`, `structure.json`, `form.gx`, `layout.gx`, `api.json`, `table.json`, `platforms.json`, `key.json`, `indexes.json`, `members.json`, `external-members.json`, `help.md`, `documentation.md`, `dependencies.json` y `parts/*.txt`, según las partes exportadas.

## Comportamiento incremental y seguro para compartir

La salida es acumulativa. Los objetos ausentes de una importación parcial permanecen activos; los objetos sin cambios pueden omitirse mediante hashes deterministas; `--reprocess-all` fuerza el procesamiento. `--snapshot` retira los objetos ausentes dentro del ámbito de KB/versión y preserva el estado histórico. Las dependencias y las proyecciones del grafo se recalculan para el conjunto acumulado.

`--share-safe` es el límite explícito para compartir. Implica redacción y no conservar datos sin procesar, sanitiza la procedencia conservada y mantiene únicamente las rutas internas relativas necesarias para el estado incremental. Redacta rutas absolutas de Windows, UNC y POSIX compatibles, pero no es un detector completo de secretos. Revise las salidas antes de compartirlas.

Las referencias no resueltas o ambiguas permanecen en `dependencies.json` y en los registros canónicos, con evidencia y motivos. No crean destinos del grafo ni entradas de referencias entrantes.
