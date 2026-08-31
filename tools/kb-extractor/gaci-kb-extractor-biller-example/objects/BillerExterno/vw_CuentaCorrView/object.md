# BillerExterno.vw_CuentaCorrView

**Type:** Transaction
**Type GUID:** `1db606f2-af09-4cf9-a3b5-b481519d28f6`
**Object GUID:** `049abb72-b21d-41c4-875e-3b7b5190e21a`
**Module:** `BillerExterno`
**Name:** `vw_CuentaCorrView`
**Normalized path:** `objects/BillerExterno/vw_CuentaCorrView`

## Description

vw_Cuenta Corr

## Content

- [events.gx](./events.gx)
- [form.gx](./form.gx)
- [help.md](./help.md)
- [rules.gx](./rules.gx)
- [structure.json](./structure.json)
- [variables/variables.json](.[REDACTED_PATH])
- [variables/variables.md](.[REDACTED_PATH])

## Parts

| # | Part kind | File | Type GUID | Count |
|---:|---|---|---|---:|
| 1 | `transaction_structure` | [structure.json](./structure.json) | `264be5fb-1b28-4b25-a598-6ca900dd059f` | 1 |
| 2 | `form_layout` | [form.gx](./form.gx) | `d24a58ad-57ba-41b7-9e6e-eaca3543c778` | 1 |
| 3 | `defaults` | [defaults.json](./defaults.json) | `4c28dfb9-f83b-46f0-9cf3-f7e090b525d5` | 1 |
| 4 | `rules` | [rules.gx](./rules.gx) | `9b0a32a3-de6d-4be1-a4dd-1b85d3741534` | 1 |
| 5 | `events` | [events.gx](./events.gx) | `c44bd5ff-f918-415b-98e6-aca44fed84fa` | 1 |
| 6 | `variables` | [variables/variables.json](.[REDACTED_PATH]) | `e4c4ade7-53f0-4a56-bdfd-843735b66f47` | 1 |
| 7 | `help` | [help.md](./help.md) | `ad3ca970-19d0-44e1-a7b7-db05556e820c` | 1 |
| 8 | `object_defaults` | [object-defaults.json](./object-defaults.json) | `babf62c5-0111-49e9-a1c3-cc004d90900a` | 1 |

## Transaction structure

Levels: **1** · Attributes: **46**
- **Level `vw_CuentaCorrView`**
  - `vw_CC_Id` (primary key)
  - `vw_CC_Empresa`
  - `vw_CC_Estado`
  - `vw_CC_Cliente`
  - `vw_CC_ClieNombre`
  - `vw_CC_ClieNroDoc`
  - `vw_CC_ClieCBU`
  - `vw_CC_ClieEmail`
  - `vw_CC_EstAdmId`
  - `vw_CC_EstAdmDesc`
  - `vw_CC_EstAcaId`
  - `vw_CC_EstAcaDesc`
  - `vw_CC_FacTipo`
  - `vw_CC_FacSerie`
  - `vw_CC_FacSuc`
  - `vw_CC_FacNro`
  - `vw_CC_FacFecha`
  - `vw_CC_FacVto`
  - `vw_CC_FacMoneda`
  - `vw_CC_FacTotal`
  - `vw_CC_FacNroSAP`
  - `vw_CC_McCod`
  - `vw_CC_McNro`
  - `vw_CC_McMoneda`
  - `vw_CC_McTotal`
  - `vw_CC_McFecha`
  - `vw_CC_McVto`
  - `vw_CC_AsigNro`
  - `vw_CC_AsigFecha`
  - `vw_CC_DiasPago`
  - `vw_CC_IntTipo`
  - `vw_CC_IntNro`
  - `vw_CC_Carrera`
  - `vw_CC_CLCarreraId`
  - `vw_CC_CLObs`
  - `vw_CC_MaterialId`
  - `vw_CC_CCostoId`
  - `vw_CC_CCostoDesc`
  - `vw_CC_FacDetPlanItem`
  - `vw_CC_FacDetPlanId`
  - `vw_CC_FacDebAuto`
  - `vw_CC_Texto`
  - `vw_CC_Anulado`
  - `vw_CC_ModalidadId`
  - `vw_CC_Usuario`
  - `vw_CC_FechaHoraAud`
