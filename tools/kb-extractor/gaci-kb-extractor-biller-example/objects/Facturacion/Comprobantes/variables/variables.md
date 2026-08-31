# Variables

Resumen estructurado de variables. El XML completo de la part está disponible en `parts/` y en `variables/variables.json`.

[Abrir variables/variables.json](.[REDACTED_PATH])

| Nombre | Tipo | based_on | Nullable | Propiedades relevantes |
|---|---|---|---|---|
| CurrentStep | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| CurrentStepAux | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| FacturaEmpresa | — | — | — | idBasedOn=Attribute:FacturaEmpresa |
| FacturaOrigen | — | — | — | idBasedOn=Attribute:FacturaOrigen |
| GoingBack | bas:Boolean | — | — | ATTCUSTOMTYPE=bas:Boolean |
| PreviousStep | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| StepNumber | — | — | — | idBasedOn=Domain:StepNumber, WorkWithPlus_Web |
| WebSession | ext:WebSession | — | — | ATTCUSTOMTYPE=ext:WebSession |
| WebSessionKey | bas:VarChar | — | — | ATTCUSTOMTYPE=bas:VarChar |
| WizardStep | sdt:WizardSteps.WizardStepsItem, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WizardSteps.WizardStepsItem, WorkWithPlus_Web |
| WizardSteps | sdt:WizardSteps, WorkWithPlus_Web | — | — | ATTCUSTOMTYPE=sdt:WizardSteps, WorkWithPlus_Web |
| ClienteId | — | — | — | Description=Id, idBasedOn=Attribute:ClienteId |
| ParVentaID | — | — | — | idBasedOn=Attribute:ParVentaID |
