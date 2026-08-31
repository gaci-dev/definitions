# Tipos de objetos de GeneXus

`object_kind` es una clasificación semántica conservadora. No reemplaza los atributos exportados, el GUID, las partes ni el contenido de origen desconocido. Los prefijos serializados de GX9 se normalizan para las rutas navegables, mientras `legacy_name` conserva la forma original.

| Tipo | Significado | Proyecciones comunes |
|---|---|---|
| `procedure` / `report` | Objeto ejecutable | `code.gx`, `rules.gx`, `events.gx`, `variables/` |
| `transaction` | Modelo de datos transaccional | `structure.json`, `form.gx`, `variables/` |
| `sdt` | Tipo de datos estructurado | `structure.json`, `object.md` |
| `webpanel` / `screen` | Panel de interacción con el usuario | `form.gx`, `layout.gx`, `events.gx`, `variables/` |
| `menu_bar`, `data_view`, `domain`, `module`, `pattern` | Objetos de organización o metadatos | `metadata.json`, `documentation.md`, `parts/` |
| `data_provider`, `data_selector` | Composición o selección de datos estructurados | `data-provider-source.gx`, `rules.gx`, `variables/` |
| `table` / `table_view` | Metadatos de tabla o vista física | `table.json`, `platforms.json`, `key.json`, `indexes.json` |
| `api` | Contrato de API exportado | `api.json`, `api.gx`, `documentation.md` |
| `index_definition` | Definición de índice y miembros | `members.json`, `indexes.json` |
| `external_object` | Contrato de objeto externo | `external-members.json`, `documentation.md` |
| `folder` | Contenedor organizativo | `metadata.json`, `object.md` |
| `unknown` | Tipo no asignado | `metadata.json`, `object.md`, `parts/*.txt` |

Los archivos de proyección solo se emiten cuando existen sus partes de origen. Las partes repetidas reciben sufijos numéricos y no se sobrescriben. El contenido desconocido permanece disponible mediante los registros canónicos y las partes serializadas; `unknown` no significa que se hayan perdido datos.
