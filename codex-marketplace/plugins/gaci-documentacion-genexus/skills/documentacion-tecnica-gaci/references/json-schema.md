# Formato JSON del generador

Esta referencia resume el formato observado en `definitions/tools/generador-documentacion`. La version del repositorio local es la autoridad: consulta siempre su `README.md` y `ejemplo.json` antes de generar.

## Raiz

- `document` (obligatorio): `title`, `subtitle`, `product`, `objective`, `scope` y `result` son obligatorios. Tambien admite `version`, `strategy` y `footer`.
- `output.basename`: nombre base de los archivos.
- `style`: `logo`, `primaryColor`, `secondaryColor`, `accentColor`. La ruta del logo es relativa al JSON.
- `summary`: `title`, `intro`, `metrics`, `classificationTitle`, `classification`.
- `pages`: lista de paginas.

Cada pagina requiere `title` y admite `intro` y `blocks`.

## Bloques

### paragraph

```json
{"type":"paragraph","title":"Descripcion","text":"Texto."}
```

### metrics

```json
{"type":"metrics","title":"Indicadores","items":[{"value":"3","label":"componentes"}]}
```

### flow

`connector` describe la conexion entre el elemento actual y el siguiente.

```json
{"type":"flow","items":[{"title":"Cliente","body":"Interfaz","connector":"HTTPS"},{"title":"API","body":"Servicio"}]}
```

### table

Cada fila debe tener exactamente tantas celdas como columnas.

```json
{"type":"table","title":"Puertos","columns":[{"label":"Origen","width":1},{"label":"Destino","width":1}],"rows":[["Cliente","API"]]}
```

### steps

`titleWidth` es opcional y ajusta el ancho de la columna izquierda.

```json
{"type":"steps","title":"Procedimiento","titleWidth":150,"items":[{"title":"1. VALIDAR","body":"Comprobar dependencias."}]}
```

### code

```json
{"type":"code","title":"Ejemplo ficticio","lines":["API_URL=https://example.invalid","API_KEY=token-ficticio"]}
```

### note

```json
{"type":"note","title":"Atencion","text":"No incluir secretos reales."}
```

## Restricciones verificadas por el generador

- Solo acepta los tipos de bloque enumerados arriba.
- Requiere las claves basicas de `document` y el titulo de cada pagina.
- Valida que `pages` sea una lista.
- Valida la cantidad de celdas de las tablas.
- Los colores deben ser hexadecimales de seis digitos.
