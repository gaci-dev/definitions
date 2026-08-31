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
| TFAuditoriaTRN | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| TFAuditoriaTRN_Sel | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| TFAuditoriaPK | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| TFAuditoriaPK_Sel | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| TFAuditoriaATTR | — | — | — | idBasedOn=Attribute:AuditoriaATTR |
| TFAuditoriaATTR_Sel | — | — | — | idBasedOn=Attribute:AuditoriaATTR |
| TFAuditoriaOldValue | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| TFAuditoriaOldValue_Sel | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| TFAuditoriaValue | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| TFAuditoriaValue_Sel | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| TFAuditoriaMode_SelsJson | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| TFAuditoriaMode_Sels | — | — | — | idBasedOn=Attribute:AuditoriaMode, AttCollection=True |
| TFAuditoriaMode_Sel | — | — | — | idBasedOn=Attribute:AuditoriaMode |
| TFAuditoriaUser | — | — | — | idBasedOn=Attribute:AuditoriaUser |
| TFAuditoriaUser_Sel | — | — | — | idBasedOn=Attribute:AuditoriaUser |
| TFAuditoriaDateTime | — | — | — | idBasedOn=Attribute:AuditoriaDateTime |
| TFAuditoriaDateTime_To | — | — | — | idBasedOn=Attribute:AuditoriaDateTime |
| i | — | — | — | Length=10, AttMaxLen=10 |
| DynamicFiltersSelector1 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator1 | — | — | — | — |
| AuditoriaTRN1 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| DynamicFiltersEnabled2 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector2 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator2 | — | — | — | — |
| AuditoriaTRN2 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| DynamicFiltersEnabled3 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector3 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator3 | — | — | — | — |
| AuditoriaTRN3 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| GridStateDynamicFilter | sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web |
