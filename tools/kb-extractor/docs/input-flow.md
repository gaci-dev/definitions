# Flujo de entrada

1. Valida la extensión `.xml` o `.xpz` y el archivo de entrada.
2. Conserva la entrada en `raw/` de forma predeterminada. Para XPZ, enumera los miembros XML de forma determinista y selecciona el miembro solicitado o el primero.
3. Si se proporciona `--gxl`, lo lee como archivo de selección/índice GX9. Nunca se trata como contenido primario de la KB.
4. Decodifica la codificación XML declarada, incluido Latin-1, y la analiza con el analizador XML de la biblioteca estándar.
5. Reconoce los elementos `Object`, `Part`, `Reference`, `Source` y `Version` sin rechazar elementos desconocidos. El contenido `GXObject` de GX9 se adapta conservando `legacy_name`.
6. Emite registros canónicos, proyecciones legibles por objeto, proyecciones del grafo y estado.
7. Registra las advertencias de selección, los metadatos del origen, los conteos y los enlaces de salida en `manifest.json`.

El XML malformado, la entrada ZIP no válida, las extensiones no compatibles y los miembros XPZ solicitados que faltan generan `GXKBError` con un mensaje accionable. CDATA se trata como texto y no se ejecuta.
