# Variables

Resumen estructurado de variables. El XML completo de la part está disponible en `parts/` y en `variables/variables.json`.

[Abrir variables/variables.json](.[REDACTED_PATH])

| Nombre | Tipo | based_on | Nullable | Propiedades relevantes |
|---|---|---|---|---|
| IsAuthorized | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| WWPContext | sdt:WWPContext, WWPBaseObjects | — | — | ATTCUSTOMTYPE=sdt:WWPContext, WWPBaseObjects |
| ExcelDocument | ext:ExcelDocument | — | — | ATTCUSTOMTYPE=ext:ExcelDocument |
| Filename | — | — | — | idBasedOn=Domain:Url, GeneXus |
| ErrorMessage | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=512, AttMaxLen=512 |
| CellRow | — | — | — | Length=8, AttMaxLen=8 |
| FirstColumn | — | — | — | Length=8, AttMaxLen=8 |
| Random | — | — | — | Length=8, AttMaxLen=8 |
| OrderedBy | — | — | — | — |
| OrderedDsc | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| FilterFullText | — | — | — | idBasedOn=Domain:WWPFullTextFilter, WorkWithPlus_Web |
| DynamicFiltersSelector1 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator1 | — | — | — | — |
| vw_CC_Empresa1 | — | — | — | idBasedOn=Attribute:vw_CC_Empresa |
| DynamicFiltersEnabled2 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector2 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator2 | — | — | — | — |
| vw_CC_Empresa2 | — | — | — | idBasedOn=Attribute:vw_CC_Empresa |
| DynamicFiltersEnabled3 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector3 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator3 | — | — | — | — |
| vw_CC_Empresa3 | — | — | — | idBasedOn=Attribute:vw_CC_Empresa |
| GridStateDynamicFilter | sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web |
| Session | ext:WebSession | — | — | ATTCUSTOMTYPE=ext:WebSession |
| GridStateXML | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| GridState | sdt:WWPGridState, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState, WorkWithPlus_Web |
| GridStateFilterValue | sdt:WWPGridState.FilterValue, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.FilterValue, WorkWithPlus_Web |
| ColumnsSelector | sdt:WWPColumnsSelector, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPColumnsSelector, WorkWithPlus_Web |
| ColumnsSelectorAux | sdt:WWPColumnsSelector, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPColumnsSelector, WorkWithPlus_Web |
| ColumnsSelector_Column | sdt:WWPColumnsSelector.Column, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPColumnsSelector.Column, WorkWithPlus_Web |
| ColumnsSelectorXML | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| UserCustomValue | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| ColumnsToRemove | — | — | — | Length=10, AttMaxLen=10, AttCollection=True |
| ColumnToRemove | — | — | — | Length=10, AttMaxLen=10 |
| ColumnName | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| VisibleColumnCount | — | — | — | Length=10, AttMaxLen=10 |
| NewColumnVisible | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| ColumnsSelectorXML2 | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| TFvw_CC_Id | — | — | — | idBasedOn=Attribute:vw_CC_Id |
| TFvw_CC_Id_To | — | — | — | idBasedOn=Attribute:vw_CC_Id |
| TFvw_CC_Empresa | — | — | — | idBasedOn=Attribute:vw_CC_Empresa |
| TFvw_CC_Empresa_To | — | — | — | idBasedOn=Attribute:vw_CC_Empresa |
| TFvw_CC_Cliente | — | — | — | idBasedOn=Attribute:vw_CC_Cliente |
| TFvw_CC_Cliente_To | — | — | — | idBasedOn=Attribute:vw_CC_Cliente |
| TFvw_CC_ClieNombre | — | — | — | idBasedOn=Attribute:vw_CC_ClieNombre |
| TFvw_CC_ClieNombre_Sel | — | — | — | idBasedOn=Attribute:vw_CC_ClieNombre |
| TFvw_CC_ClieNroDoc | — | — | — | idBasedOn=Attribute:vw_CC_ClieNroDoc |
| TFvw_CC_ClieNroDoc_To | — | — | — | idBasedOn=Attribute:vw_CC_ClieNroDoc |
| TFvw_CC_ClieCBU | — | — | — | idBasedOn=Attribute:vw_CC_ClieCBU |
| TFvw_CC_ClieCBU_Sel | — | — | — | idBasedOn=Attribute:vw_CC_ClieCBU |
| TFvw_CC_ClieEmail | — | — | — | idBasedOn=Attribute:vw_CC_ClieEmail |
| TFvw_CC_ClieEmail_Sel | — | — | — | idBasedOn=Attribute:vw_CC_ClieEmail |
| TFvw_CC_EstAdmId | — | — | — | idBasedOn=Attribute:vw_CC_EstAdmId |
| TFvw_CC_EstAdmId_To | — | — | — | idBasedOn=Attribute:vw_CC_EstAdmId |
| TFvw_CC_EstAdmDesc | — | — | — | idBasedOn=Attribute:vw_CC_EstAdmDesc |
| TFvw_CC_EstAdmDesc_Sel | — | — | — | idBasedOn=Attribute:vw_CC_EstAdmDesc |
| TFvw_CC_EstAcaId | — | — | — | idBasedOn=Attribute:vw_CC_EstAcaId |
| TFvw_CC_EstAcaId_To | — | — | — | idBasedOn=Attribute:vw_CC_EstAcaId |
| TFvw_CC_EstAcaDesc | — | — | — | idBasedOn=Attribute:vw_CC_EstAcaDesc |
| TFvw_CC_EstAcaDesc_Sel | — | — | — | idBasedOn=Attribute:vw_CC_EstAcaDesc |
| TFvw_CC_FacTipo | — | — | — | idBasedOn=Attribute:vw_CC_FacTipo |
| TFvw_CC_FacTipo_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacTipo |
| TFvw_CC_FacSerie | — | — | — | idBasedOn=Attribute:vw_CC_FacSerie |
| TFvw_CC_FacSerie_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacSerie |
| TFvw_CC_FacSuc | — | — | — | idBasedOn=Attribute:vw_CC_FacSuc |
| TFvw_CC_FacSuc_To | — | — | — | idBasedOn=Attribute:vw_CC_FacSuc |
| TFvw_CC_FacNro | — | — | — | idBasedOn=Attribute:vw_CC_FacNro |
| TFvw_CC_FacNro_To | — | — | — | idBasedOn=Attribute:vw_CC_FacNro |
| TFvw_CC_FacFecha | — | — | — | idBasedOn=Attribute:vw_CC_FacFecha |
| TFvw_CC_FacFecha_To | — | — | — | idBasedOn=Attribute:vw_CC_FacFecha |
| TFvw_CC_FacVto | — | — | — | idBasedOn=Attribute:vw_CC_FacVto |
| TFvw_CC_FacVto_To | — | — | — | idBasedOn=Attribute:vw_CC_FacVto |
| TFvw_CC_FacMoneda | — | — | — | idBasedOn=Attribute:vw_CC_FacMoneda |
| TFvw_CC_FacMoneda_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacMoneda |
| TFvw_CC_FacTotal | — | — | — | idBasedOn=Attribute:vw_CC_FacTotal |
| TFvw_CC_FacTotal_To | — | — | — | idBasedOn=Attribute:vw_CC_FacTotal |
| TFvw_CC_FacNroSAP | — | — | — | idBasedOn=Attribute:vw_CC_FacNroSAP |
| TFvw_CC_FacNroSAP_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacNroSAP |
| TFvw_CC_McCod | — | — | — | idBasedOn=Attribute:vw_CC_McCod |
| TFvw_CC_McCod_Sel | — | — | — | idBasedOn=Attribute:vw_CC_McCod |
| TFvw_CC_McNro | — | — | — | idBasedOn=Attribute:vw_CC_McNro |
| TFvw_CC_McNro_To | — | — | — | idBasedOn=Attribute:vw_CC_McNro |
| TFvw_CC_McMoneda | — | — | — | idBasedOn=Attribute:vw_CC_McMoneda |
| TFvw_CC_McMoneda_Sel | — | — | — | idBasedOn=Attribute:vw_CC_McMoneda |
| TFvw_CC_McTotal | — | — | — | idBasedOn=Attribute:vw_CC_McTotal |
| TFvw_CC_McTotal_To | — | — | — | idBasedOn=Attribute:vw_CC_McTotal |
| TFvw_CC_McFecha | — | — | — | idBasedOn=Attribute:vw_CC_McFecha |
| TFvw_CC_McFecha_To | — | — | — | idBasedOn=Attribute:vw_CC_McFecha |
| i | — | — | — | Length=10, AttMaxLen=10 |
| CuentaCorrCarreraDescription | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| CuentaCorrCarrera | — | — | — | idBasedOn=Attribute:vw_CC_Carrera, AttCollection=True |
| CuentaCorrCL_CarreraIdDescription | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| CuentaCorrCL_CarreraId | — | — | — | idBasedOn=Attribute:vw_CC_CLCarreraId, AttCollection=True |
| CuentaCorrMedioCobroCodDescription | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| CuentaCorrMedioCobroCod | — | — | — | idBasedOn=Attribute:vw_CC_McCod, AttCollection=True |
| CuentaCorrClienteTipoKey | — | — | — | idBasedOn=Attribute:CuentaCorrClienteTipo |
| CuentaCorrClienteTipoDescription | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| CuentaCorrClienteTipo | — | — | — | idBasedOn=Attribute:CuentaCorrClienteTipo, AttCollection=True |
| CuentaCorrEstadoKey | — | — | — | idBasedOn=Attribute:CuentaCorrEstado |
| CuentaCorrEstadoDescription | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| CuentaCorrEstado | — | — | — | idBasedOn=Attribute:CuentaCorrEstado, AttCollection=True |
| CuentaCorrFacturaFecha | — | — | — | idBasedOn=Attribute:vw_CC_FacFecha |
| CuentaCorrFacturaFecha_To | — | — | — | idBasedOn=Attribute:vw_CC_FacFecha |
| CuentaCorrFacturaVto | — | — | — | idBasedOn=Attribute:vw_CC_FacVto |
| CuentaCorrFacturaVto_To | — | — | — | idBasedOn=Attribute:vw_CC_FacVto |
| TFvw_CC_McVto | — | — | — | idBasedOn=Attribute:vw_CC_McVto |
| TFvw_CC_McVto_To | — | — | — | idBasedOn=Attribute:vw_CC_McVto |
| TFvw_CC_AsigNro | — | — | — | idBasedOn=Attribute:vw_CC_AsigNro |
| TFvw_CC_AsigNro_To | — | — | — | idBasedOn=Attribute:vw_CC_AsigNro |
| TFvw_CC_AsigFecha | — | — | — | idBasedOn=Attribute:vw_CC_AsigFecha |
| TFvw_CC_AsigFecha_To | — | — | — | idBasedOn=Attribute:vw_CC_AsigFecha |
| TFvw_CC_DiasPago | — | — | — | idBasedOn=Attribute:vw_CC_DiasPago |
| TFvw_CC_DiasPago_To | — | — | — | idBasedOn=Attribute:vw_CC_DiasPago |
| TFvw_CC_IntTipo | — | — | — | idBasedOn=Attribute:vw_CC_IntTipo |
| TFvw_CC_IntTipo_Sel | — | — | — | idBasedOn=Attribute:vw_CC_IntTipo |
| TFvw_CC_IntNro | — | — | — | idBasedOn=Attribute:vw_CC_IntNro |
| TFvw_CC_IntNro_To | — | — | — | idBasedOn=Attribute:vw_CC_IntNro |
| TFvw_CC_Carrera | — | — | — | idBasedOn=Attribute:vw_CC_Carrera |
| TFvw_CC_Carrera_To | — | — | — | idBasedOn=Attribute:vw_CC_Carrera |
| TFvw_CC_CLCarreraId | — | — | — | idBasedOn=Attribute:vw_CC_CLCarreraId |
| TFvw_CC_CLCarreraId_Sel | — | — | — | idBasedOn=Attribute:vw_CC_CLCarreraId |
| TFvw_CC_CLObs | — | — | — | idBasedOn=Attribute:vw_CC_CLObs |
| TFvw_CC_CLObs_Sel | — | — | — | idBasedOn=Attribute:vw_CC_CLObs |
| TFvw_CC_MaterialId | — | — | — | idBasedOn=Attribute:vw_CC_MaterialId |
| TFvw_CC_MaterialId_Sel | — | — | — | idBasedOn=Attribute:vw_CC_MaterialId |
| TFvw_CC_CCostoId | — | — | — | idBasedOn=Attribute:vw_CC_CCostoId |
| TFvw_CC_CCostoId_To | — | — | — | idBasedOn=Attribute:vw_CC_CCostoId |
| TFvw_CC_CCostoDesc | — | — | — | idBasedOn=Attribute:vw_CC_CCostoDesc |
| TFvw_CC_CCostoDesc_Sel | — | — | — | idBasedOn=Attribute:vw_CC_CCostoDesc |
| TFvw_CC_FacDetPlanItem | — | — | — | idBasedOn=Attribute:vw_CC_FacDetPlanItem |
| TFvw_CC_FacDetPlanItem_To | — | — | — | idBasedOn=Attribute:vw_CC_FacDetPlanItem |
| TFvw_CC_FacDetPlanId | — | — | — | idBasedOn=Attribute:vw_CC_FacDetPlanId |
| TFvw_CC_FacDetPlanId_To | — | — | — | idBasedOn=Attribute:vw_CC_FacDetPlanId |
| TFvw_CC_FacDebAuto | — | — | — | idBasedOn=Attribute:vw_CC_FacDebAuto |
| TFvw_CC_FacDebAuto_Sel | — | — | — | idBasedOn=Attribute:vw_CC_FacDebAuto |
| TFvw_CC_Texto | — | — | — | idBasedOn=Attribute:vw_CC_Texto |
| TFvw_CC_Texto_Sel | — | — | — | idBasedOn=Attribute:vw_CC_Texto |
| TFvw_CC_Anulado | — | — | — | idBasedOn=Attribute:vw_CC_Anulado |
| TFvw_CC_Anulado_Sel | — | — | — | idBasedOn=Attribute:vw_CC_Anulado |
| TFvw_CC_ModalidadId | — | — | — | idBasedOn=Attribute:vw_CC_ModalidadId |
| TFvw_CC_ModalidadId_Sel | — | — | — | idBasedOn=Attribute:vw_CC_ModalidadId |
| TFvw_CC_Usuario | — | — | — | idBasedOn=Attribute:vw_CC_Usuario |
| TFvw_CC_Usuario_Sel | — | — | — | idBasedOn=Attribute:vw_CC_Usuario |
| TFvw_CC_FechaHoraAud | — | — | — | idBasedOn=Attribute:vw_CC_FechaHoraAud |
| TFvw_CC_FechaHoraAud_To | — | — | — | idBasedOn=Attribute:vw_CC_FechaHoraAud |
| estadoAdmin | bas:Character | — | — | ATTCUSTOMTYPE=bas:Character, Length=60, AttMaxLen=60 |
| estadoAcademico | bas:Character | — | — | ATTCUSTOMTYPE=bas:Character, Length=60, AttMaxLen=60 |
| TFvw_CC_Estado_SelsJson | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| TFvw_CC_Estado_Sel | — | — | — | idBasedOn=Attribute:vw_CC_Estado |
| TFvw_CC_Estado_Sels | — | — | — | idBasedOn=Attribute:vw_CC_Estado, AttCollection=True |
