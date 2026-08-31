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
| OrderedBy | — | — | — | — |
| OrderedDsc | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| OrderedByAux | — | — | — | — |
| FilterFullText | — | — | — | idBasedOn=Domain:WWPFullTextFilter, WorkWithPlus_Web |
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
| TFAuditoriaTRN | — | — | — | idBasedOn=Attribute:AuditoriaTRN, AddEmptyItem=True |
| TFAuditoriaTRN_Sel | — | — | — | idBasedOn=Attribute:AuditoriaTRN, AddEmptyItem=True |
| TFAuditoriaPK | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, AddEmptyItem=True |
| TFAuditoriaPK_Sel | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, AddEmptyItem=True |
| TFAuditoriaATTR | — | — | — | idBasedOn=Attribute:AuditoriaATTR, AddEmptyItem=True |
| TFAuditoriaATTR_Sel | — | — | — | idBasedOn=Attribute:AuditoriaATTR, AddEmptyItem=True |
| TFAuditoriaOldValue | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, AddEmptyItem=True |
| TFAuditoriaOldValue_Sel | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, AddEmptyItem=True |
| TFAuditoriaValue | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, AddEmptyItem=True |
| TFAuditoriaValue_Sel | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, AddEmptyItem=True |
| TFAuditoriaMode_SelsJson | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| TFAuditoriaMode_Sels | — | — | — | idBasedOn=Attribute:AuditoriaMode, AttCollection=True, ControlType=Edit, AddEmptyItem=True |
| TFAuditoriaUser | — | — | — | idBasedOn=Attribute:AuditoriaUser, AddEmptyItem=True |
| TFAuditoriaUser_Sel | — | — | — | idBasedOn=Attribute:AuditoriaUser, AddEmptyItem=True |
| TFAuditoriaDateTime | — | — | — | idBasedOn=Attribute:AuditoriaDateTime, AddEmptyItem=True |
| TFAuditoriaDateTime_To | — | — | — | idBasedOn=Attribute:AuditoriaDateTime, AddEmptyItem=True |
| DDO_AuditoriaDateTimeAuxDate | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_AuditoriaDateTimeAuxDateTo | bas:Date | — | — | ATTCUSTOMTYPE=bas:Date |
| DDO_AuditoriaDateTimeAuxDateText | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| DDO_TitleSettingsIcons | sdt:DVB_SDTDropDownOptionsTitleSettingsIcons, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTDropDownOptionsTitleSettingsIcons, WorkWithPlus_Web |
| PageToGo | — | — | — | Length=6, AttMaxLen=6 |
| GridCurrentPage | — | — | — | Length=10, AttMaxLen=10 |
| GridPageCount | — | — | — | Length=10, AttMaxLen=10 |
| GridAppliedFilters | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| GridActions | — | — | — | ControlType=Combo Box |
| AGExportData | sdt:DVB_SDTDropDownOptionsData, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTDropDownOptionsData, WorkWithPlus_Web |
| AGExportDataItem | sdt:DVB_SDTDropDownOptionsData.Item, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:DVB_SDTDropDownOptionsData.Item, WorkWithPlus_Web |
| AuditoriaTRNWithTags | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| GridStateDynamicFilter | sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web |
| DynamicFiltersSelector1 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, ControlType=Combo Box, ControlValues=Transaccion:AUDITORIATRN |
| DynamicFiltersOperator1 | — | — | — | ControlType=Combo Box, ControlValues=WWP_FilterLike:0,WWP_FilterContains:1 |
| AuditoriaTRN1 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| DynamicFiltersEnabled2 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector2 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, ControlType=Combo Box, ControlValues=Transaccion:AUDITORIATRN |
| DynamicFiltersOperator2 | — | — | — | ControlType=Combo Box, ControlValues=WWP_FilterLike:0,WWP_FilterContains:1 |
| AuditoriaTRN2 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| DynamicFiltersEnabled3 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector3 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, ControlType=Combo Box, ControlValues=Transaccion:AUDITORIATRN |
| DynamicFiltersOperator3 | — | — | — | ControlType=Combo Box, ControlValues=WWP_FilterLike:0,WWP_FilterContains:1 |
| AuditoriaTRN3 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| DynamicFiltersRemoving | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersIgnoreFirst | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
