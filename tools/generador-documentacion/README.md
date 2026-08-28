# Generador genérico de documentación

Genera un PDF final y un DOCX editable con el formato corporativo de Gaci. El contenido se define completamente en un archivo JSON; el motor no está asociado a ningún producto.

No es necesario usar inteligencia artificial. El documento puede prepararse manualmente o con ayuda de IA; en ambos casos, el generador produce los archivos de manera determinística a partir del mismo JSON.

## Cómo funciona

La herramienta separa el contenido de su presentación:

```text
JSON con el contenido
        ↓
generar_documentacion.py
        ↓
PDF final + DOCX editable
```

El JSON es la fuente del documento. Contiene títulos, textos, tablas, flujos y ejemplos. El script de Python aplica el diseño corporativo, calcula la paginación y genera los archivos finales.

Para crear un documento nuevo normalmente solo se modifica el JSON. No es necesario cambiar `generar_documentacion.py`.

## Requisitos

- Python 3.
- Pycairo.

Instalación de la dependencia:

```bash
python3 -m pip install pycairo
```

## Crear un documento manualmente

1. Copiar [`ejemplo.json`](./ejemplo.json) y asignarle un nombre relacionado con el documento:

    ```text
    documentacion-api-farmacia.json
    ```

2. Editar la portada, el resumen, las páginas y sus bloques.

3. Ejecutar el generador:

```bash
python3 generar_documentacion.py ejemplo.json
```

También puede ejecutarse indicando rutas completas:

```bash
python3 /ruta/definitions/tools/generador-documentacion/generar_documentacion.py \
  /ruta/documentacion-api-farmacia.json \
  --output-dir /ruta/salida
```

Opciones:

```text
--output-dir DIRECTORIO   Cambia el directorio de salida.
--basename NOMBRE         Cambia el nombre base de los archivos.
--no-logo                 Genera documentos sin logotipo.
```

La salida contiene:

- `NOMBRE.pdf`: documento final.
- `NOMBRE_editable.docx`: versión editable.

## Estructura del JSON

La raíz admite:

- `document`: portada, objetivo, alcance, estrategia y resultado.
- `output.basename`: nombre predeterminado de los archivos.
- `style`: logo y colores opcionales.
- `summary`: introducción, métricas y clasificación de la portada.
- `pages`: páginas de contenido.

Ejemplo mínimo:

```json
{
  "document": {
    "title": "Título del documento",
    "subtitle": "Descripción breve",
    "product": "Nombre del producto",
    "version": "v1.0",
    "objective": "Qué explica el documento",
    "scope": "Qué incluye y qué deja afuera",
    "strategy": "Cómo funciona la solución",
    "result": "Qué obtiene el lector",
    "footer": "Texto del pie de página"
  },
  "output": {
    "basename": "Nombre_Del_Archivo"
  },
  "summary": {
    "title": "Resumen",
    "intro": "Descripción general",
    "metrics": [
      {
        "value": "2",
        "label": "conexiones obligatorias"
      }
    ],
    "classification": "Circuito principal: Cliente → API → Base de datos."
  },
  "pages": []
}
```

Ejemplo de una página con bloques:

```json
{
  "title": "Configuración",
  "intro": "Configuración necesaria para operar el sistema.",
  "blocks": [
    {
      "type": "paragraph",
      "title": "Descripción",
      "text": "El cliente consume una API REST."
    },
    {
      "type": "code",
      "title": "Ejemplo",
      "lines": [
        "API_URL=http://192.0.2.10:3000",
        "API_KEY=token-ficticio"
      ]
    }
  ]
}
```

Cada página contiene un título, una introducción opcional y una lista `blocks`. Los bloques soportados son:

| Tipo | Uso |
| --- | --- |
| `paragraph` | Título opcional y texto libre. |
| `metrics` | Indicadores numéricos destacados. |
| `flow` | Componentes conectados mediante flechas. |
| `table` | Tabla con anchos relativos por columna. |
| `steps` | Secuencia numerada o lista de acciones. |
| `code` | Configuración, comandos o ejemplos técnicos. |
| `note` | Advertencia o aclaración destacada. |

El archivo [`ejemplo.json`](./ejemplo.json) muestra todos los conceptos principales y puede copiarse como punto de partida.

## Crear un documento con IA

La IA es útil cuando la información está repartida entre código fuente, archivos de configuración y distintos repositorios. Puede investigar el sistema y preparar un primer borrador del JSON.

Ejemplo de pedido:

> Revisá estos repositorios y prepará un JSON compatible con el generador de documentación de `definitions`. Documentá componentes, conexiones, variables obligatorias y opcionales. Usá ejemplos ficticios y no incluyas secretos reales.

Flujo recomendado:

1. La IA revisa el código y la configuración que se le autorice consultar.
2. Identifica componentes, conexiones, variables y dependencias.
3. Genera el JSON compatible con esta herramienta.
4. Una persona revisa el contenido, el alcance y los ejemplos.
5. Se ejecuta el generador.
6. Se revisan visualmente el PDF y el DOCX.
7. Los ajustes de contenido se realizan en el JSON y se vuelve a generar.

La IA no es necesaria para producir el PDF o el DOCX. Su función es ayudar a investigar, redactar y estructurar el contenido.

## Cuándo conviene cada modalidad

- **Manual:** documentos cortos, información ya conocida o cambios pequeños sobre un JSON existente.
- **Con IA:** documentación inicial, sistemas con varios componentes o información distribuida entre repositorios.
- **Combinada:** IA para el primer borrador y revisión manual antes de generar. Es la modalidad recomendada para documentación técnica.

## Personalización visual

`style` permite indicar:

```json
{
  "style": {
    "logo": "assets/otro-logo.png",
    "primaryColor": "#0785BF",
    "secondaryColor": "#1CA6B0",
    "accentColor": "#A1CF1F"
  }
}
```

La ruta del logo es relativa al JSON de entrada. Si no se especifica, se utiliza el logo corporativo incluido con la herramienta.

## Seguridad

Los ejemplos deben usar datos ficticios con la estructura real.

No incluir:

- Tokens o API keys reales.
- Usuarios o contraseñas.
- Direcciones privadas de clientes.
- Contenido de archivos `.env` reales.
- Datos clínicos o información personal.

Estas reglas aplican tanto al trabajo manual como al asistido por IA. Antes de generar el documento debe revisarse el JSON y confirmarse que no contiene información sensible.
