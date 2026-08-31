---
name: documentacion-tecnica-gaci
description: Crea o actualiza documentacion tecnica y genera el PDF y DOCX corporativos de Gaci mediante tools/generador-documentacion del repositorio definitions. Usar ante pedidos de documentar sistemas, APIs, integraciones, despliegues, configuraciones, arquitecturas o procedimientos tecnicos.
---

# Documentacion tecnica Gaci

Usa siempre el generador corporativo de `definitions`; no reemplaces su salida con documentos creados por otros medios.

## Flujo

1. Identifica el alcance, los lectores y las fuentes autorizadas. Si el alcance puede inferirse con seguridad, avanza y declara la inferencia; pregunta solo cuando una eleccion cambiaria materialmente el documento.
2. Revisa codigo, configuracion y documentacion pertinente. Basa las afirmaciones en evidencia observable y separa hechos de inferencias. Para codigo u objetos GeneXus, usa la skill `nexa` y sus referencias especificas. Para un `.xpz`, usa primero la skill `xpz-analyzer` y luego `nexa` para interpretar semanticamente los objetos detectados.
3. Usa por defecto la copia corporativa versionada en `assets/generador-documentacion`. Solo usa otro checkout de `definitions` cuando el usuario lo pida o configure explicitamente.
4. Lee `assets/generador-documentacion/README.md` y `assets/generador-documentacion/ejemplo.json` antes de redactar. Lee [references/json-schema.md](references/json-schema.md) cuando necesites la forma de un bloque.
5. Crea un JSON por documento en una carpeta de trabajo. Conserva tambien ese JSON como fuente editable y usa un `output.basename` descriptivo.
6. Ejecuta [scripts/run_generator.py](scripts/run_generator.py) indicando el JSON y la carpeta final. El script debe producir un PDF y un DOCX editable.
7. Inspecciona visualmente todas las paginas del PDF. Corrige texto cortado, paginas pobres, tablas ilegibles, desbordes y jerarquia confusa modificando el JSON, y vuelve a generar.
8. Entrega el JSON fuente, el PDF y el DOCX. Resume las fuentes consultadas, los supuestos y cualquier vacio de informacion.

## Reglas de contenido

- Escribe en el idioma pedido; si no se especifica, usa el idioma del usuario.
- No inventes endpoints, puertos, variables, dependencias ni comportamientos. Marca como pendiente lo que no pueda verificarse.
- Usa datos ficticios con estructura real en ejemplos.
- No copies tokens, claves, contrasenas, archivos `.env`, direcciones privadas de clientes, datos personales, clinicos ni productivos.
- No uses el documento generado para exponer secretos encontrados durante la investigacion.
- No cambies `generar_documentacion.py`, sus recursos visuales ni la identidad corporativa salvo que el usuario lo pida expresamente.
- No importes un XPZ en una Knowledge Base para analizarlo salvo pedido y autorizacion explicitos; el analisis documental debe comenzar en modo de solo lectura.
- Si el generador falla por una dependencia ausente, informa el requisito concreto. Instala dependencias solamente cuando la solicitud autorice preparar o configurar el entorno.

## Ejecucion

```text
python scripts/run_generator.py documento.json --output-dir RUTA_SALIDA
```

`--definitions-repo` permite probar deliberadamente otra version del generador. Usa `--no-logo` solo a pedido del usuario.
