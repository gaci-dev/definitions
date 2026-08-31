# Arquitectura

GXKB considera `canonical/records.jsonl` como la autoridad estructural. `objects/`, `graph/` y los índices de compatibilidad son proyecciones derivadas.

```text
XML / XPZ -> input preparation -> identity and hashes -> cumulative merge
                              |-> canonical JSONL records
                              |-> readable object files
                              |-> graph nodes and edges
                              `-> manifest and state links
```

## Límites

| Capa | Propósito | Mutabilidad |
|---|---|---|
| `raw/` | Copia de entrada para auditoría y reprocesamiento | Conservada de forma predeterminada; omitida o sanitizada según la política |
| `objects/` | Navegación de objetos legible para personas | Derivada |
| `canonical/` | Representación de intercambio general orientada al origen | Autoridad derivada |
| `graph/` | Proyección para consumidores del grafo | Derivada |
| `kb-state.json` | Registro de identidad, versión, hash e ingesta | Estado persistente |

La implementación usa únicamente la biblioteca estándar de Python durante la ejecución. El XML se analiza con `xml.etree.ElementTree`; el texto de origen nunca se ejecuta.

La interfaz pública de compatibilidad está formada por `gxkb.normalizer.normalize` y `gxkb.normalizer.validate_output`. Los módulos de soporte aíslan la redacción, los contratos, las proyecciones y la adaptación GX9 sin cambiar esos puntos de entrada.

Las dependencias y los datos del grafo se recalculan para el conjunto acumulado de objetos. Las importaciones parciales conservan los objetos ausentes. `snapshot=True` retira los objetos ausentes de ese ámbito de KB/versión mientras preserva el historial; los objetos reintroducidos vuelven a estar activos.

`BasedOn` de GX9 y las referencias léxicas al origen son conservadoras: solo los destinos resueltos de forma unívoca producen aristas del grafo y resúmenes de referencias entrantes. Los comentarios y literales de cadena se enmascaran, se conservan los rangos y la evidencia no resuelta o ambigua permanece en forma canónica sin fabricar topología.
