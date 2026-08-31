# Variables

Resumen estructurado de variables. El XML completo de la part está disponible en `parts/` y en `variables/variables.json`.

[Abrir variables/variables.json](.[REDACTED_PATH])

| Nombre | Tipo | based_on | Nullable | Propiedades relevantes |
|---|---|---|---|---|
| IsAuthorized | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| WWPContext | sdt:WWPContext, WWPBaseObjects | — | — | ATTCUSTOMTYPE=sdt:WWPContext, WWPBaseObjects |
| HTTPRequest | ext:HttpRequest | — | — | ATTCUSTOMTYPE=ext:HttpRequest |
| TrnContext | sdt:WWPTransactionContext, WorkWithPlus_CommonObjects | — | — | ATTCUSTOMTYPE=sdt:WWPTransactionContext, WorkWithPlus_CommonObjects |
| TrnContextAtt | sdt:WWPTransactionContext.Attribute, WorkWithPlus_CommonObjects | — | — | ATTCUSTOMTYPE=sdt:WWPTransactionContext.Attribute, WorkWithPlus_CommonObjects |
| GridState | sdt:WWPGridState, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState, WorkWithPlus_Web |
| GridStateFilterValue | sdt:WWPGridState.FilterValue, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.FilterValue, WorkWithPlus_Web |
| GridStateDynamicFilter | sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web |
| OrderedBy | — | — | — | — |
| OrderedDsc | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| OrderedByAux | — | — | — | — |
| FilterFullText | — | — | — | idBasedOn=Domain:WWPFullTextFilter, WorkWithPlus_Web |
| DynamicFiltersSelector1 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, ControlType=Combo Box, ControlValues=Empresa:VW_CC_EMPRESA |
| DynamicFiltersOperator1 | — | — | — | ControlType=Combo Box, ControlValues=<:0,=:1,>:2 |
| vw_CC_Empresa1 | — | — | — | idBasedOn=Attribute:vw_CC_Empresa |
| DynamicFiltersEnabled2 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector2 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, ControlType=Combo Box, ControlValues=Empresa:VW_CC_EMPRESA |
| DynamicFiltersOperator2 | — | — | — | ControlType=Combo Box, ControlValues=<:0,=:1,>:2 |
| vw_CC_Empresa2 | — | — | — | idBasedOn=Attribute:vw_CC_Empresa |
| DynamicFiltersEnabled3 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector3 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, ControlType=Combo Box, ControlValues=Empresa:VW_CC_EMPRESA |
| DynamicFiltersOperator3 | — | — | — | ControlType=Combo Box, ControlValues=<:0,=:1,>:2 |
| vw_CC_Empresa3 | — | — | — | idBasedOn=Attribute:vw_CC_Empresa |
| DynamicFiltersRemoving | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersIgnoreFirst | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| ExcelFilename | — | — | — | idBasedOn=Domain:Url, GeneXus |
| ErrorMessage | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=512, AttMaxLen=512 |
| ColumnsSelectorXML | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| UserCustomValue | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| ColumnsSelector | sdt:WWPColumnsSelector, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPColumnsSelector, WorkWithPlus_Web |
| ColumnsSelectorAux | sdt:WWPColumnsSelector, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPColumnsSelector, WorkWithPlus_Web |
| Session | ext:WebSession | — | — | ATTCUSTOMTYPE=ext:WebSession |
| ManageFiltersData | sdt:DVB_SDTDropDownOptionsData, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTDropDownOptionsData, WorkWithPlus_Web |
| ManageFiltersXml | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| ManageFiltersExecutionStep | — | — | — | Length=1, AttMaxLen=1 |
| TFvw_CC_Id | — | — | — | idBasedOn=Attribute:vw_CC_Id, AddEmptyItem=True |
| TFvw_CC_Id_To | — | — | — | idBasedOn=Attribute:vw_CC_Id, AddEmptyItem=True |
| TFvw_CC_Empresa | — | — | — | idBasedOn=Attribute:vw_CC_Empresa, AddEmptyItem=True |
| TFvw_CC_Empresa_To | — | — | — | idBasedOn=Attribute:vw_CC_Empresa, AddEmptyItem=True |
| TFvw_CC_Cliente | — | — | — | idBasedOn=Attribute:vw_CC_Cliente, AddEmptyItem=True |
| TFvw_CC_Cliente_To | — | — | — | idBasedOn=Attribute:vw_CC_Cliente, AddEmptyItem=True |
| TFvw_CC_ClieNombre | — | — | — | idBasedOn=Attribute:vw_CC_ClieNombre, AddEmptyItem=True |
| TFvw_CC_ClieNombre_Sel | — | — | — | idBasedOn=Attribute:vw_CC_ClieNombre, AddEmptyItem=True |
| TFvw_CC_ClieNroDoc | — | — | — | idBasedOn=Attribute:vw_CC_ClieNroDoc, AddEmptyItem=True |
| TFvw_CC_ClieNroDoc_To | — | — | — | idBasedOn=Attribute:vw_CC_ClieNroDoc, AddEmptyItem=True |
| TFvw_CC_ClieCBU | — | — | — | idBasedOn=Attribute:vw_CC_ClieCBU, AddEmptyItem=True |
| TFvw_CC_ClieCBU_Sel | — | — | — | idBasedOn=Attribute:vw_CC_ClieCBU, AddEmptyItem=True |
| TFvw_CC_ClieEmail | — | — | — | idBasedOn=Attribute:vw_CC_ClieEmail, AddEmptyItem=True |
| TFvw_CC_ClieEmail_Sel | — | — | — | idBasedOn=Attribute:vw_CC_ClieEmail, AddEmptyItem=True |
| TFvw_CC_EstAdmId | — | — | — | idBasedOn=Attribute:vw_CC_EstAdmId, AddEmptyItem=True |
| TFvw_CC_EstAdmId_To | — | — | — | idBasedOn=Attribute:vw_CC_EstAdmId, AddEmptyItem=True |
| TFvw_CC_EstAdmDesc | — | — | — | idBasedOn=Attribute:vw_CC_EstAdmDesc, AddEmptyItem=True |
| TFvw_CC_EstAdmDesc_Sel | — | — | — | idBasedOn=Attribute:vw_CC_EstAdmDesc, AddEmptyItem=True |
| TFvw_CC_EstAcaId | — | — | — | idBasedOn=Attribute:vw_CC_EstAcaId, AddEmptyItem=True |
| TFvw_CC_EstAcaId_To | — | — | — | idBasedOn=Attribute:vw_CC_EstAcaId, AddEmptyItem=True |
| TFvw_CC_EstAcaDesc | — | — | — | idBasedOn=Attribute:vw_CC_EstAcaDesc, AddEmptyItem=True |
| TFvw_CC_EstAcaDesc_Sel | — | — | — | idBasedOn=Attribute:vw_CC_EstAcaDesc, AddEmptyItem=True |
| TFvw_CC_FacTipo | — | — | — | idBasedOn=Attribute:vw_CC_FacTipo, AddEmptyItem=True |
| TFvw_CC_FacTipo_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacTipo, AddEmptyItem=True |
| TFvw_CC_FacSerie | — | — | — | idBasedOn=Attribute:vw_CC_FacSerie, AddEmptyItem=True |
| TFvw_CC_FacSerie_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacSerie, AddEmptyItem=True |
| TFvw_CC_FacSuc | — | — | — | idBasedOn=Attribute:vw_CC_FacSuc, AddEmptyItem=True |
| TFvw_CC_FacSuc_To | — | — | — | idBasedOn=Attribute:vw_CC_FacSuc, AddEmptyItem=True |
| TFvw_CC_FacNro | — | — | — | idBasedOn=Attribute:vw_CC_FacNro, AddEmptyItem=True |
| TFvw_CC_FacNro_To | — | — | — | idBasedOn=Attribute:vw_CC_FacNro, AddEmptyItem=True |
| TFvw_CC_FacFecha | — | — | — | idBasedOn=Attribute:vw_CC_FacFecha, AddEmptyItem=True |
| TFvw_CC_FacFecha_To | — | — | — | idBasedOn=Attribute:vw_CC_FacFecha, AddEmptyItem=True |
| DDO_vw_CC_FacFechaAuxDate | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_FacFechaAuxDateTo | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_FacFechaAuxDateText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| TFvw_CC_FacVto | — | — | — | idBasedOn=Attribute:vw_CC_FacVto, AddEmptyItem=True |
| TFvw_CC_FacVto_To | — | — | — | idBasedOn=Attribute:vw_CC_FacVto, AddEmptyItem=True |
| DDO_vw_CC_FacVtoAuxDate | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_FacVtoAuxDateTo | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_FacVtoAuxDateText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| TFvw_CC_FacMoneda | — | — | — | idBasedOn=Attribute:vw_CC_FacMoneda, AddEmptyItem=True |
| TFvw_CC_FacMoneda_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacMoneda, AddEmptyItem=True |
| TFvw_CC_FacTotal | — | — | — | idBasedOn=Attribute:vw_CC_FacTotal, AddEmptyItem=True |
| TFvw_CC_FacTotal_To | — | — | — | idBasedOn=Attribute:vw_CC_FacTotal, AddEmptyItem=True |
| TFvw_CC_FacNroSAP | — | — | — | idBasedOn=Attribute:vw_CC_FacNroSAP, AddEmptyItem=True |
| TFvw_CC_FacNroSAP_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacNroSAP, AddEmptyItem=True |
| TFvw_CC_McCod | — | — | — | idBasedOn=Attribute:vw_CC_McCod, AddEmptyItem=True |
| TFvw_CC_McCod_Sel | — | — | — | idBasedOn=Attribute:vw_CC_McCod, AddEmptyItem=True |
| TFvw_CC_McNro | — | — | — | idBasedOn=Attribute:vw_CC_McNro, AddEmptyItem=True |
| TFvw_CC_McNro_To | — | — | — | idBasedOn=Attribute:vw_CC_McNro, AddEmptyItem=True |
| TFvw_CC_McMoneda | — | — | — | idBasedOn=Attribute:vw_CC_McMoneda, AddEmptyItem=True |
| TFvw_CC_McMoneda_Sel | — | — | — | idBasedOn=Attribute:vw_CC_McMoneda, AddEmptyItem=True |
| TFvw_CC_McTotal | — | — | — | idBasedOn=Attribute:vw_CC_McTotal, AddEmptyItem=True |
| TFvw_CC_McTotal_To | — | — | — | idBasedOn=Attribute:vw_CC_McTotal, AddEmptyItem=True |
| TFvw_CC_McFecha | — | — | — | idBasedOn=Attribute:vw_CC_McFecha, AddEmptyItem=True |
| TFvw_CC_McFecha_To | — | — | — | idBasedOn=Attribute:vw_CC_McFecha, AddEmptyItem=True |
| DDO_vw_CC_McFechaAuxDate | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_McFechaAuxDateTo | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_McFechaAuxDateText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| DDO_TitleSettingsIcons | sdt:DVB_SDTDropDownOptionsTitleSettingsIcons, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTDropDownOptionsTitleSettingsIcons, WorkWithPlus_Web |
| PageToGo | — | — | — | Length=6, AttMaxLen=6 |
| GridCurrentPage | — | — | — | Length=10, AttMaxLen=10 |
| GridPageCount | — | — | — | Length=10, AttMaxLen=10 |
| GridAppliedFilters | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| AGExportData | sdt:DVB_SDTDropDownOptionsData, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTDropDownOptionsData, WorkWithPlus_Web |
| AGExportDataItem | sdt:DVB_SDTDropDownOptionsData.Item, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTDropDownOptionsData.Item, WorkWithPlus_Web |
| CuentaCorrCarrera | — | — | — | idBasedOn=Attribute:vw_CC_Carrera, AttCollection=True |
| CuentaCorrCL_CarreraId | — | — | — | idBasedOn=Attribute:vw_CC_CLCarreraId, AttCollection=True |
| CuentaCorrMedioCobroCod | — | — | — | idBasedOn=Attribute:vw_CC_McCod, AttCollection=True |
| CuentaCorrClienteTipo | — | — | — | idBasedOn=Attribute:CuentaCorrClienteTipo, AttCollection=True |
| CuentaCorrEstado | — | — | — | idBasedOn=Attribute:CuentaCorrEstado, AttCollection=True |
| CuentaCorrFacturaFecha | — | — | — | idBasedOn=Attribute:vw_CC_FacFecha |
| CuentaCorrFacturaFecha_To | — | — | — | idBasedOn=Attribute:vw_CC_FacFecha |
| CuentaCorrFacturaVto | — | — | — | idBasedOn=Attribute:vw_CC_FacVto |
| CuentaCorrFacturaVto_To | — | — | — | idBasedOn=Attribute:vw_CC_FacVto |
| ClienteId | — | — | — | idBasedOn=Attribute:ClienteId |
| ClienteNombre | — | — | — | idBasedOn=Attribute:ClienteNombre |
| TFvw_CC_McVto | — | — | — | idBasedOn=Attribute:vw_CC_McVto, AddEmptyItem=True |
| TFvw_CC_McVto_To | — | — | — | idBasedOn=Attribute:vw_CC_McVto, AddEmptyItem=True |
| DDO_vw_CC_McVtoAuxDate | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_McVtoAuxDateTo | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_McVtoAuxDateText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| TFvw_CC_AsigNro | — | — | — | idBasedOn=Attribute:vw_CC_AsigNro, AddEmptyItem=True |
| TFvw_CC_AsigNro_To | — | — | — | idBasedOn=Attribute:vw_CC_AsigNro, AddEmptyItem=True |
| TFvw_CC_AsigFecha | — | — | — | idBasedOn=Attribute:vw_CC_AsigFecha, AddEmptyItem=True |
| TFvw_CC_AsigFecha_To | — | — | — | idBasedOn=Attribute:vw_CC_AsigFecha, AddEmptyItem=True |
| DDO_vw_CC_AsigFechaAuxDate | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_AsigFechaAuxDateTo | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_AsigFechaAuxDateText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| TFvw_CC_DiasPago | — | — | — | idBasedOn=Attribute:vw_CC_DiasPago, AddEmptyItem=True |
| TFvw_CC_DiasPago_To | — | — | — | idBasedOn=Attribute:vw_CC_DiasPago, AddEmptyItem=True |
| TFvw_CC_IntTipo | — | — | — | idBasedOn=Attribute:vw_CC_IntTipo, AddEmptyItem=True |
| TFvw_CC_IntTipo_Sel | — | — | — | idBasedOn=Attribute:vw_CC_IntTipo, AddEmptyItem=True |
| TFvw_CC_IntNro | — | — | — | idBasedOn=Attribute:vw_CC_IntNro, AddEmptyItem=True |
| TFvw_CC_IntNro_To | — | — | — | idBasedOn=Attribute:vw_CC_IntNro, AddEmptyItem=True |
| TFvw_CC_Carrera | — | — | — | idBasedOn=Attribute:vw_CC_Carrera, AddEmptyItem=True |
| TFvw_CC_Carrera_To | — | — | — | idBasedOn=Attribute:vw_CC_Carrera, AddEmptyItem=True |
| TFvw_CC_CLCarreraId | — | — | — | idBasedOn=Attribute:vw_CC_CLCarreraId, AddEmptyItem=True |
| TFvw_CC_CLCarreraId_Sel | — | — | — | idBasedOn=Attribute:vw_CC_CLCarreraId, AddEmptyItem=True |
| TFvw_CC_CLObs | — | — | — | idBasedOn=Attribute:vw_CC_CLObs, AddEmptyItem=True |
| TFvw_CC_CLObs_Sel | — | — | — | idBasedOn=Attribute:vw_CC_CLObs, AddEmptyItem=True |
| TFvw_CC_MaterialId | — | — | — | idBasedOn=Attribute:vw_CC_MaterialId, AddEmptyItem=True |
| TFvw_CC_MaterialId_Sel | — | — | — | idBasedOn=Attribute:vw_CC_MaterialId, AddEmptyItem=True |
| TFvw_CC_CCostoId | — | — | — | idBasedOn=Attribute:vw_CC_CCostoId, AddEmptyItem=True |
| TFvw_CC_CCostoId_To | — | — | — | idBasedOn=Attribute:vw_CC_CCostoId, AddEmptyItem=True |
| TFvw_CC_CCostoDesc | — | — | — | idBasedOn=Attribute:vw_CC_CCostoDesc, AddEmptyItem=True |
| TFvw_CC_CCostoDesc_Sel | — | — | — | idBasedOn=Attribute:vw_CC_CCostoDesc, AddEmptyItem=True |
| TFvw_CC_FacDetPlanItem | — | — | — | idBasedOn=Attribute:vw_CC_FacDetPlanItem, AddEmptyItem=True |
| TFvw_CC_FacDetPlanItem_To | — | — | — | idBasedOn=Attribute:vw_CC_FacDetPlanItem, AddEmptyItem=True |
| TFvw_CC_FacDetPlanId | — | — | — | idBasedOn=Attribute:vw_CC_FacDetPlanId, AddEmptyItem=True |
| TFvw_CC_FacDetPlanId_To | — | — | — | idBasedOn=Attribute:vw_CC_FacDetPlanId, AddEmptyItem=True |
| TFvw_CC_FacDebAuto | — | — | — | idBasedOn=Attribute:vw_CC_FacDebAuto, AddEmptyItem=True |
| TFvw_CC_FacDebAuto_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacDebAuto, AddEmptyItem=True |
| TFvw_CC_Texto | — | — | — | idBasedOn=Attribute:vw_CC_Texto, AddEmptyItem=True |
| TFvw_CC_Texto_Sel | — | — | — | idBasedOn=Attribute:vw_CC_Texto, AddEmptyItem=True |
| TFvw_CC_Anulado | — | — | — | idBasedOn=Attribute:vw_CC_Anulado, AddEmptyItem=True |
| TFvw_CC_Anulado_Sel | — | — | — | idBasedOn=Attribute:vw_CC_Anulado, AddEmptyItem=True |
| TFvw_CC_ModalidadId | — | — | — | idBasedOn=Attribute:vw_CC_ModalidadId, AddEmptyItem=True |
| TFvw_CC_ModalidadId_Sel | — | — | — | idBasedOn=Attribute:vw_CC_ModalidadId, AddEmptyItem=True |
| TFvw_CC_Usuario | — | — | — | idBasedOn=Attribute:vw_CC_Usuario, AddEmptyItem=True |
| TFvw_CC_Usuario_Sel | — | — | — | idBasedOn=Attribute:vw_CC_Usuario, AddEmptyItem=True |
| TFvw_CC_FechaHoraAud | — | — | — | idBasedOn=Attribute:vw_CC_FechaHoraAud, AddEmptyItem=True |
| TFvw_CC_FechaHoraAud_To | — | — | — | idBasedOn=Attribute:vw_CC_FechaHoraAud, AddEmptyItem=True |
| DDO_vw_CC_FechaHoraAudAuxDate | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_FechaHoraAudAuxDateTo | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_vw_CC_FechaHoraAudAuxDateText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| CuentaCorrCarrera_Data | sdt:DVB_SDTComboData, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTComboData, WorkWithPlus_Web |
| Combo_DataItem | sdt:DVB_SDTComboData.Item, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTComboData.Item, WorkWithPlus_Web |
| CuentaCorrCL_CarreraId_Data | sdt:DVB_SDTComboData, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTComboData, WorkWithPlus_Web |
| ComboTitles | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, AttCollection=True |
| CuentaCorrMedioCobroCod_Data | sdt:DVB_SDTComboData, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTComboData, WorkWithPlus_Web |
| CuentaCorrClienteTipo_Data | sdt:DVB_SDTComboData, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTComboData, WorkWithPlus_Web |
| CuentaCorrEstado_Data | sdt:DVB_SDTComboData, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTComboData, WorkWithPlus_Web |
| CuentaCorrFacturaFecha_RangeText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| CuentaCorrFacturaVto_RangeText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| estadoAdmin | bas:Character | — | — | ATTCUSTOMTYPE=bas:Character, Length=60, AttMaxLen=60 |
| estadoAcademico | bas:Character | — | — | ATTCUSTOMTYPE=bas:Character, Length=60, AttMaxLen=60 |
| TFvw_CC_Estado_SelsJson | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| TFvw_CC_Estado_Sels | — | — | — | idBasedOn=Attribute:vw_CC_Estado, AttCollection=True, AddEmptyItem=True |
| AuxText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| vw_CC_EstadoWithTags | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| LoadGridData | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| TFCuentaCorrCliente | — | — | — | Description=Cuenta Corr Cliente, idIsAutoDefinedVariable=True, idBasedOn=Attribute:CuentaCorrCliente |
