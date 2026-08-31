# Variables

Resumen estructurado de variables. El XML completo de la part está disponible en `parts/` y en `variables/variables.json`.

[Abrir variables/variables.json](.[REDACTED_PATH])

| Nombre | Tipo | based_on | Nullable | Propiedades relevantes |
|---|---|---|---|---|
| IsAuthorized | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| WWPContext | sdt:WWPContext, WWPBaseObjects | — | — | ATTCUSTOMTYPE=sdt:WWPContext, WWPBaseObjects |
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
| TFAuditoriaUser | — | — | — | idBasedOn=Attribute:AuditoriaUser |
| TFAuditoriaUser_Sel | — | — | — | idBasedOn=Attribute:AuditoriaUser |
| TFAuditoriaDateTime | — | — | — | idBasedOn=Attribute:AuditoriaDateTime |
| TFAuditoriaDateTime_To | — | — | — | idBasedOn=Attribute:AuditoriaDateTime |
| SearchTxtParms | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| SkipItems | — | — | — | — |
| PageIndex | — | — | — | — |
| MaxItems | — | — | — | — |
| SearchTxt | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| SearchTxtTo | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=100, AttMaxLen=100 |
| DDOName | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| InsertIndex | — | — | — | Length=6, AttMaxLen=6 |
| Option | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| Options | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, AttCollection=True |
| OptionsJson | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| OptionDesc | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200 |
| OptionsDesc | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, Length=200, AttMaxLen=200, AttCollection=True |
| OptionsDescJson | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| OptionIndexes | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar, AttCollection=True |
| OptionIndexesJson | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| count | — | — | — | Length=10, AttMaxLen=10, idTHOUSANDSEP=True |
| Session | ext:WebSession | — | — | ATTCUSTOMTYPE=ext:WebSession |
| GridStateXML | bas:LongVarChar | — | — | ATTCUSTOMTYPE=bas:LongVarChar |
| GridState | sdt:WWPGridState, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState, WorkWithPlus_Web |
| GridStateFilterValue | sdt:WWPGridState.FilterValue, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.FilterValue, WorkWithPlus_Web |
| GridStateDynamicFilter | sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WWPGridState.DynamicFilter, WorkWithPlus_Web |
| FilterFullText | — | — | — | idBasedOn=Domain:WWPFullTextFilter, WorkWithPlus_Web |
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
