# Formato XPZ y referencias provistas

## Contenedor

Los XPZ examinados son contenedores ZIP. El ejemplo provisto contiene un XML cuya raiz es `ExportFile`, con metadatos de version, origen y una coleccion `Objects/Object`. Un XPZ distinto puede variar; el analizador debe informar, no corregir silenciosamente.

Un `Object` puede incluir:

- atributos como `name`, `fullyQualifiedName`, `type`, `parent`, `description` y fechas;
- una o mas `Part`, identificadas tambien por GUID;
- `Source` en CDATA o XML serializado;
- propiedades, referencias y dependencias.

Los campos `user`, identificadores de Knowledge Base, GUID y checksum no son necesarios para documentacion funcional y se omiten del informe predeterminado.

## GUID de tipos observados en las muestras

Esta tabla es orientativa y no sustituye la identificacion de la version ni las referencias Nexa.

| GUID | Categoria observada |
| --- | --- |
| `1db606f2-af09-4cf9-a3b5-b481519d28f6` | Transaction |
| `84a12160-f59b-4ad7-a683-ea4481ac23e9` | Procedure |
| `2a9e9aba-d2de-4801-ae7f-5e3819222daf` | Data Provider |
| `ffd44be7-3bb4-4d01-9e7e-d1c1a3c095af` | Data Selector |
| `19abc6ff-2cd2-0000-0006-6d172bc2333b` | Data View |
| `447527b5-9210-4523-898b-5dccb17be60a` | Structured Data Type |
| `00972a17-9975-449e-aab1-d26165d51393` | Domain |
| `b5f00807-9da8-4cf9-b408-7554f2b6a8ee` | Business Process Diagram |
| `9fb193d9-64a4-4d30-b129-ff7c76830f7e` | Image |
| `88313f43-5eb2-0000-0028-e8d9f5bf9588` | Language |
| `c9584656-94b6-4ccd-890f-332d11fc2c25` | Web panel/master page family in sample |
| `198e8ea4-1d49-4c9c-8a9a-417024baa9d1` | Work panel in sample |

## XSD

Los XSD aportados estan en `assets/schemas/legacy` y `assets/schemas/default`. Cubren atributos, dominios, transacciones, procedimientos, SDT, data providers, data selectors, data views, diagramas, imagenes, lenguajes y paneles. Algunas variantes se duplican con diferencias historicas.

Usalos para comprender estructuras de XML ya identificadas. No elijas automaticamente un XSD solo por el nombre del archivo interno ni declares valido un XPZ completo con el esquema de un unico tipo de objeto.

## Interpretacion profunda

Despues del inventario, enruta cada categoria a la referencia Nexa correspondiente:

- Transaction: `object-transaction.md`
- Procedure: `object-procedure.md`
- Data Provider: `object-data-provider.md`
- Data Selector: `object-data-selector.md`
- Data View: `object-data-view.md`
- Structured Data Type: `object-structured-data-type.md`
- Domain: `object-domain.md`
- Business Process Diagram: `object-business-process.md`
- Panel/Web Panel: `object-panel.md`

Para tipos desconocidos, conserva GUID, nombre y evidencia estructural; no derives el tipo por analogia.
