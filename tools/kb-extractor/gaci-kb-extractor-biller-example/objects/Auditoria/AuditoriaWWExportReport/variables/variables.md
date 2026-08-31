# Variables

Resumen estructurado de variables. El XML completo de la part está disponible en `parts/` y en `variables/variables.json`.

[Abrir variables/variables.json](.[REDACTED_PATH])

| Nombre | Tipo | based_on | Nullable | Propiedades relevantes |
|---|---|---|---|---|
| IsAuthorized | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| WWPContext | sdt:WWPContext, WWPBaseObjects | — | — | ATTCUSTOMTYPE=sdt:WWPContext, WWPBaseObjects |
| OrderedBy | — | — | — | — |
| OrderedDsc | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| FilterFullText | — | — | — | idBasedOn=Domain:WWPFullTextFilter, WorkWithPlus_Web |
| DynamicFiltersSelector1 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator1 | — | — | — | — |
| AuditoriaTRN1 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| FilterAuditoriaTRNDescription | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| AuditoriaTRN | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| DynamicFiltersEnabled2 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector2 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator2 | — | — | — | — |
| AuditoriaTRN2 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| DynamicFiltersEnabled3 | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| DynamicFiltersSelector3 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| DynamicFiltersOperator3 | — | — | — | — |
| AuditoriaTRN3 | — | — | — | idBasedOn=Attribute:AuditoriaTRN |
| GridStateDynamicFilter | sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web |
| AuditoriaModeDescription | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| Session | ext:WebSession | — | — | ATTCUSTOMTYPE=ext:WebSession |
| GridStateXML | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| GridState | sdt:WWPGridState, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState, WorkWithPlus_Web |
| GridStateFilterValue | sdt:WWPGridState.FilterValue, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.FilterValue, WorkWithPlus_Web |
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
| TFAuditoriaMode_SelDscs | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| TFAuditoriaMode_Sel | — | — | — | idBasedOn=Attribute:AuditoriaMode |
| TFAuditoriaMode_Sels | — | — | — | idBasedOn=Attribute:AuditoriaMode, AttCollection=True |
| TFAuditoriaUser | — | — | — | idBasedOn=Attribute:AuditoriaUser |
| TFAuditoriaUser_Sel | — | — | — | idBasedOn=Attribute:AuditoriaUser |
| TFAuditoriaDateTime | — | — | — | idBasedOn=Attribute:AuditoriaDateTime |
| TFAuditoriaDateTime_To | — | — | — | idBasedOn=Attribute:AuditoriaDateTime |
| FilterTFAuditoriaMode_SelValueDescription | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| TFAuditoriaDateTime_To_Description | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| TempBoolean | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| i | — | — | — | Length=10, AttMaxLen=10 |
| AddressLine1 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| AddressLine2 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| AddressLine3 | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| AppName | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| Attribute | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| DateInfo | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| Filter | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| Mail | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| PageInfo | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| Phone | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| Title | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| Website | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
