# Navegación GXKB — gaci-gxkb-navigation

## Propósito
Navegar datos GXKB generados y responder con evidencia sobre procedimientos, reportes, transacciones, reglas, eventos, variables, estructura y dependencias de GeneXus.

## Cuándo usar
Cargar al recibir un directorio de salida de `kb_extractor`/GXKB o al consultar procedimientos, reportes, transacciones, reglas, eventos, variables, estructura, dependencias o análisis de KB generada de GeneXus.

## Reglas obligatorias
- Localizar primero la raíz de salida buscando `objects-index.jsonl`, `manifest.json` o `canonical/records.jsonl`; no asumir que el directorio actual es la KB.
- Tratar `canonical/records.jsonl` como autoridad estructural. `objects/`, `graph/` e índices son proyecciones.
- No inferir que un dato está ausente por una proyección faltante. Revisar primero los registros canónicos y todos los `parts/*.txt` coincidentes.
- Distinguir hechos confirmados, evidencia generada e interpretación. No ejecutar ni inventar comportamiento de GeneXus.
- Inspeccionar cada parte repetida (`-002`, `-003`, etc.) antes de concluir.

## Decisiones

| Consulta | Leer primero |
|---|---|
| Encontrar un objeto | `objects-index.jsonl` → `objects/<module>/<name>/metadata.json`, `object.md` |
| Comportamiento de procedimiento/reporte | `code.gx` → `rules.gx` → `events.gx` → `variables/` |
| Estructura de transacción | `structure.json` → `form.gx` → `rules.gx`/`events.gx` → `variables/` |
| Dependencias/referencias | `dependencies.json` del objeto → `incoming-references.json` → registros canónicos → graph |
| Detalle faltante o ambiguo | registros canónicos y `parts/*.txt` coincidentes |

## Procedimiento
1. Identificar el objeto por nombre exacto, módulo, GUID u `object_kind`.
2. Leer las proyecciones preferidas anteriores y registrar sus rutas.
3. Contrastar las afirmaciones importantes con los registros canónicos y las partes fuente.
4. Seguir las dependencias y referencias inversas resueltas; informar explícitamente los elementos no resueltos o ambiguos.
5. Para el comportamiento de negocio, combinar la documentación con el código ejecutable, reglas, eventos, variables y dependencias.

## Salida esperada
Responder concisamente con conclusión, rutas de evidencia, extractos de código/reglas o nombres de campos relevantes, hallazgos de dependencias/referencias y una nota explícita de incertidumbre cuando la cobertura sea parcial o haya elementos sin resolver.

## Ejemplo
Para navegar la muestra share-safe reducida de Biller, usar `tools/kb-extractor/gaci-kb-extractor-biller-example` como raíz de salida. La muestra contiene 47 objetos, 197 partes, 90 dependencias y ninguna referencia; 87 dependencias permanecen sin resolver porque sus destinos fueron excluidos, sin incorporar entradas raw.

```powershell
$output = "tools/kb-extractor/gaci-kb-extractor-biller-example"
py -3 -m gxkb --help
```

La salida corresponde a la KB `Biller` y conserva su identidad y las tres importaciones acumulativas. La validación de `canonical/records.jsonl`, `canonical/manifest.json`, `manifest.json` y `graph/` pasó correctamente.

Ante una consulta sobre `CuentaCorriente.CuentaCorr`, seguir este orden:

1. Encontrar `CuentaCorriente.CuentaCorr` en `objects-index.jsonl` y confirmar que es una `transaction` retenida.
2. Leer `tools/kb-extractor/gaci-kb-extractor-biller-example/objects/CuentaCorriente/CuentaCorr/metadata.json` y `object.md`.
3. Revisar `structure.json`, `form.gx`, `rules.gx`, `events.gx` y `variables/`; la estructura contiene 63 atributos.
4. Contrastar `dependencies.json` con los registros canónicos y revisar las partes repetidas.
5. Revisar `incoming-references.json` y separar hechos confirmados, evidencia y aspectos no resueltos.

Ejemplo de salida:

> `CuentaCorriente.CuentaCorr` es una transacción retenida en la muestra reducida, con 63 atributos. Sus reglas asignan valores iniciales y bloquean la edición de varios atributos cuando la operación está en modo inserción.
>
> **Evidencia:** `tools/kb-extractor/gaci-kb-extractor-biller-example/objects/CuentaCorriente/CuentaCorr/metadata.json` identifica el objeto como `transaction`; `tools/kb-extractor/gaci-kb-extractor-biller-example/objects/CuentaCorriente/CuentaCorr/object.md` informa 63 atributos; `tools/kb-extractor/gaci-kb-extractor-biller-example/objects/CuentaCorriente/CuentaCorr/rules.gx:10-21` contiene las asignaciones condicionadas por `TrnMode.Insert`; `tools/kb-extractor/gaci-kb-extractor-biller-example/objects/CuentaCorriente/CuentaCorr/dependencies.json` conserva la evidencia de sus dependencias.
>
> **Incertidumbre:** `dependencies.json` conserva una referencia no resuelta a `WWPTransactionContext.Attribute`, y `incoming-references.json` está vacío. No se debe afirmar quién invoca la transacción sin evidencia adicional.

## Referencias
- `references/kb-navigation.md` — mapa detallado de navegación y particularidades de GX9.
