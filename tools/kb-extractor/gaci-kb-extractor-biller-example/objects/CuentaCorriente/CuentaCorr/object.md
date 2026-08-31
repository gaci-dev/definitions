# CuentaCorriente.CuentaCorr

**Type:** Transaction
**Type GUID:** `1db606f2-af09-4cf9-a3b5-b481519d28f6`
**Object GUID:** `6e56899a-b5b2-4642-b374-cb237eb7e0f5`
**Module:** `CuentaCorriente`
**Name:** `CuentaCorr`
**Normalized path:** `objects/CuentaCorriente/CuentaCorr`

## Description

Cuenta Corriente

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

Levels: **1** · Attributes: **63**
- **Level `CuentaCorr`**
  - `CuentaCorrId` (primary key)
  - `CuentaCorrEmpresa`
  - `CuentaCorrCarrera`
  - `CuentaCorrCL_CarreraId`
  - `CuentaCorrCL_observaciones`
  - `CuentaCorrCliente`
  - `CuentaCorrClienteNombre`
  - `CuentaCorrClienteTipo`
  - `CuentaCorrClienteNroDoc`
  - `CuentaCorrEstAdministrativo`
  - `CuentaCorrEstAcademico`
  - `CuentaCorrFacturaTipo`
  - `CuentaCorrFacturaSerie`
  - `CuentaCorrFacturaSucursal`
  - `CuentaCorrFacturaNumero`
  - `CuentaCorrFacturaFecha`
  - `CuentaCorrFacturaVto`
  - `CuentaCorrFacturaMoneda`
  - `CuentaCorrFacturaTotal`
  - `CuentaCorrFacturaNroSAP` (isNullable=True)
  - `CuentaCorrMedioCobroId` (isNullable=True)
  - `CuentaCorrMedioCobroCod` (isNullable=True)
  - `CuentaCorrMedioCobroNumero` (isNullable=True)
  - `CuentaCorrMedioCobroMoneda`
  - `CuentaCorrMedioCobroMonedaDescripcion`
  - `CuentaCorrMedioCobroTotal`
  - `CuentaCorrMedioCobroFecha`
  - `CuentaCorrMedioCobroVto`
  - `CuentaCorrAsigNumero` (isNullable=True)
  - `CuentaCorrAsigFecha`
  - `CuentaCorrDiasPago` (isNullable=True)
  - `CuentaCorrInternoTipo`
  - `CuentaCorrInternoNumero`
  - `CuentaCorrMod` (isNullable=True)
  - `CuentaCorrTrn` (isNullable=True)
  - `CuentaCorrRel` (isNullable=True)
  - `CuentaCorrContabilizado` (isNullable=True)
  - `CuentaCorrEstado` (isNullable=True)
  - `CuentaCorrRegistroProcesado`
  - `CuentaCorrFacturaVtoPro`
  - `CuentaCorrTotalSaldo`
  - `CuentaCorrModalidadId` (isNullable=True)
  - `CuentaCorrAnulado` (isNullable=True)
  - `CuentaCorrSaldado` (isNullable=True)
  - `CuentaCorrMaterialId` (isNullable=True)
  - `CuentaCorrCcostoId` (isNullable=True)
  - `CuentaCorrCCostoDescripcion` (isNullable=True)
  - `CuentaCorrFacDetPlanitem` (isNullable=True)
  - `CuentaCorrFacDetPlanid` (isNullable=True)
  - `CuentaCorrFacturaDebitoAutomatico` (isNullable=True)
  - `CuentaCorrMedioCobrodescripcion` (isNullable=True)
  - `CuentaCorrFacturaVto2` (isNullable=True)
  - `CuentaCorrTexto` (isNullable=True)
  - `CuentaCorrProcesadoPMC` (isNullable=True)
  - `CuentaCorrAnticipo` (isNullable=True)
  - `CuentaCorrClienteEmail`
  - `CuentaCorrCBU`
  - `CuentaCorrMaterialConcepto`
  - `CuentaCorrUsuario` (isNullable=True)
  - `CuentaCorrFechaHoraAud` (isNullable=True)
  - `CuentaCorrPaisId`
  - `CuentaCorrPaisTxt`
  - `CuentaCorrClienteCodigoUniversitas`
