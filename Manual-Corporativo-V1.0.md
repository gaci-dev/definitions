# Manual Corporativo de Desarrollo de Software — Gaci V1.0

**Versión:** 1.0  
**Estado:** Base corporativa para adopción gradual  
**Ámbito:** Productos, aplicaciones, integraciones, satélites y procesos batch de Gaci

Este manual define el marco común para descubrir, construir, operar y mejorar software en Gaci. Complementa la [Guía Técnica de Desarrollo](./Manual-Desarrollo.md), que contiene mayor detalle de implementación, y se apoya en los [módulos de contexto portables](./skills/) para trabajar con asistentes de IA sin depender de un proveedor específico.

## Cómo usar este manual

1. Leer el **camino mínimo**: principios, ciclo de vida, GEM, calidad, seguridad y checklists.
2. Aplicar el nivel de exigencia indicado: **Obligatorio**, **Recomendado**, **Condicionado** o **Excepción**.
3. Usar las plantillas de [requerimiento](./templates/Plantilla-Requerimiento.md), [ADR](./templates/Plantilla-ADR.md), [postmortem](./templates/Plantilla-Postmortem.md) y [Pull Request](./templates/Checklist-Pull-Request.md).
4. Consultar `Manual-Desarrollo.md` y las skills cuando se necesite una guía técnica detallada.

> **Regla de interpretación:** “Obligatorio” establece el piso corporativo. “Recomendado” expresa la práctica preferida. “Condicionado” aplica cuando se cumplen los criterios indicados. “Excepción” permite apartarse del estándar solo con justificación, alcance, responsable y fecha de revisión.

## 1. Propósito, objetivos y alcance

### Propósito

Construir y mantener software confiable, seguro, trazable y sostenible, preservando el conocimiento de negocio existente mientras Gaci evoluciona desde GeneXus hacia un ecosistema tecnológico moderno.

### Objetivos

- Convertir necesidades de negocio en cambios verificables y operables.
- Reducir riesgo mediante diseño explícito, revisión por pares, automatización y despliegues reversibles.
- Preservar reglas de negocio, ownership de datos y conocimiento del legacy.
- Permitir adopción progresiva sin exigir la misma profundidad documental a todos los cambios.
- Usar IA para acelerar el trabajo sin delegar responsabilidad ni criterio profesional.

### Alcance

Aplica a software nuevo, evolución de aplicaciones existentes, correcciones, migraciones, integraciones, APIs, frontend, workers, procesos batch, scripts operativos y cambios de datos. Incluye desarrollo interno y terceros que entreguen código o componentes bajo responsabilidad de Gaci.

## 2. Principios corporativos

1. **Negocio primero.** El problema, el usuario, el valor y las reglas de negocio preceden a la elección tecnológica.
2. **Seguridad desde diseño.** Se identifican amenazas, accesos, datos sensibles y controles antes de exponer una solución.
3. **Trazabilidad.** Cada cambio relevante debe poder vincularse con su requerimiento, decisión, código, pruebas y despliegue.
4. **Ownership de datos.** Todo dato crítico tiene responsable funcional, definición, origen, reglas de calidad, acceso y ciclo de vida.
5. **Calidad automatizada.** Las verificaciones repetibles se ejecutan en CI/CD; la automatización complementa, no reemplaza, el juicio técnico.
6. **IA bajo revisión humana.** La persona que integra un resultado generado o asistido por IA entiende, prueba, asegura y responde por ese resultado.
7. **Excepciones documentadas.** Apartarse del estándar es válido cuando se explicita el motivo, el riesgo aceptado, el responsable y la fecha de revisión.

### Niveles de aplicación

| Nivel | Significado | Evidencia esperada |
|---|---|---|
| **Obligatorio** | Piso corporativo para todo cambio alcanzado. | Registro, revisión o control automatizado verificable. |
| **Recomendado** | Práctica preferida que reduce riesgo o costo futuro. | Aplicación o justificación breve si no se usa. |
| **Condicionado** | Aplica por riesgo, tipo de sistema, datos, criticidad o tecnología. | Criterio que activa la condición. |
| **Excepción** | Desvío temporal o permanente aprobado. | Registro de excepción, responsable, riesgo y vencimiento/revisión. |

## 3. Clasificación de proyectos

Clasificar el proyecto al inicio y revisarlo si cambia su riesgo.

| Tipo | Características | Enfoque inicial |
|---|---|---|
| **GeneXus legacy** | Aplicación o procedimiento cuyo comportamiento principal vive en GeneXus. | Relevamiento, preservación de reglas, control de regresión y documentación progresiva. |
| **Híbrido** | Conviven componentes GeneXus y servicios o interfaces modernas. | Contratos explícitos, ownership por componente y observabilidad de la frontera. |
| **Nuevo** | Solución sin dependencia funcional principal de un sistema legacy. | Descubrimiento, diseño por capas, automatización desde el comienzo. |
| **Satélite o integración** | Adaptador, API, intercambio de archivos, sincronización o conexión con otro sistema. | Contratos, idempotencia, reintentos, errores, seguridad y reconciliación. |
| **Worker o batch** | Proceso asincrónico, programado o de larga duración. | Idempotencia, checkpoints, reanudación, métricas, alertas y operación manual documentada. |

La clasificación no prescribe una herramienta. Define el nivel de análisis y controles que el contexto requiere.

## 4. Roles y responsabilidades

| Rol | Responsabilidades principales |
|---|---|
| **Sponsor / owner de negocio** | Priorizar valor, alcance y riesgo; aceptar resultados y decisiones de negocio. |
| **Responsable funcional** | Detallar reglas, actores, datos, criterios de aceptación y validación funcional. |
| **Líder técnico** | Guiar arquitectura, riesgos, decisiones, estándares, revisión técnica y sostenibilidad. |
| **Desarrolladores** | Diseñar e implementar, mantener pruebas y documentación, revisar código y operar lo construido. |
| **QA** | Diseñar estrategia de pruebas, evaluar riesgo, verificar criterios y aportar evidencia independiente. |
| **DevOps / infraestructura** | Proveer CI/CD, ambientes, configuración, despliegue, rollback y controles operativos. |
| **Seguridad** | Asesorar sobre amenazas, accesos, secretos, datos sensibles, dependencias y controles. |
| **Responsable de datos** | Definir ownership, calidad, clasificación, retención, acceso y uso permitido de los datos. |

En equipos pequeños una persona puede cubrir varios roles. La combinación debe ser explícita y no elimina la necesidad de revisión independiente en cambios de alto riesgo.

## 5. Ciclo de vida estándar

El flujo completo es: **descubrimiento → requerimiento → análisis/diseño → planificación → desarrollo → revisión → testing → despliegue → operación → aprendizaje/mantenimiento**.

### 5.1 Descubrimiento

Entender problema, usuarios, proceso actual, restricciones, datos, integraciones, métricas de éxito y riesgos. Para producto nuevo, consultar `gaci-product-discovery.md`; para GeneXus, consultar `gaci-gx-bridge.md`.

### 5.2 Requerimiento

Registrar objetivo, alcance, no objetivos, actores, reglas, criterios de aceptación, dependencias y trazabilidad GEM. Usar la [Plantilla de Requerimiento](./templates/Plantilla-Requerimiento.md).

### 5.3 Análisis y diseño

Evaluar alternativas, impacto, seguridad, datos, observabilidad, compatibilidad y operación. Registrar decisiones relevantes en una ADR.

### 5.4 Planificación

Descomponer en unidades entregables, ordenar dependencias, estimar riesgo y definir estrategia de pruebas, migración y despliegue.

### 5.5 Desarrollo y revisión

Implementar en ramas de trabajo, con commits comprensibles, pruebas adecuadas y documentación actualizada. Ningún cambio llega a ramas protegidas sin Pull Request.

### 5.6 Testing y despliegue

Ejecutar los controles definidos por riesgo, revisar evidencia y desplegar con un plan de monitoreo y rollback.

### 5.7 Operación y aprendizaje

Verificar métricas, errores y aceptación. Registrar incidentes, deuda, decisiones pendientes y aprendizajes para mejorar el producto y el proceso.

## 6. Requerimientos y trazabilidad GEM

### Reglas de trazabilidad

- **Obligatorio:** si existe un ticket o evento GEM, vincularlo en la rama, commits, PR, documentación y resumen de cierre.
- **Obligatorio:** si no existe GEM, no inventar un identificador. Registrar “sin GEM” y la referencia alternativa disponible (pedido, correo, incidente, reunión o documento).
- **Condicionado:** una migración técnica sin cambio funcional puede no tener ticket GEM; debe conservar evidencia del alcance, componente afectado, validación y aprobación del responsable.
- **Recomendado:** publicar en GEM o en el sistema de trabajo el resumen, resultado, riesgos, pruebas, diagramas y enlaces a commits/PR.

Todo requerimiento debe incluir:

- objetivo y valor esperado;
- alcance y **no objetivos**;
- usuarios, actores, datos e integraciones;
- reglas de negocio y supuestos;
- criterios de aceptación observables;
- dependencias, riesgos y restricciones;
- estrategia de pruebas y definición de terminado.

### Definición de terminado (DoD)

Un cambio está terminado cuando cumple los criterios de aceptación, tiene código revisado, pruebas ejecutadas con evidencia, documentación actualizada, controles de seguridad aplicados, trazabilidad registrada y plan de despliegue/operación definido cuando corresponde.

## 7. Arquitecturas de referencia y criterios tecnológicos

La referencia corporativa separa **dominio, aplicación e infraestructura**: el dominio contiene reglas de negocio; aplicación coordina casos de uso y puertos; infraestructura implementa adaptadores, persistencia, transporte e integraciones. Las dependencias apuntan hacia el negocio, no al revés. Ver el detalle en [`Manual-Desarrollo.md`](./Manual-Desarrollo.md), especialmente su arquitectura hexagonal.

### Criterios

- **Obligatorio:** separar reglas de negocio de detalles tecnológicos cuando el cambio o riesgo lo justifique.
- **Obligatorio:** definir contratos para APIs e integraciones, incluyendo errores, versionado, autenticación, límites e idempotencia cuando aplique.
- **Condicionado:** usar workers o colas cuando el procesamiento sea asincrónico, pesado, reintentable o desacoplable.
- **Recomendado:** documentar flujos y límites con Mermaid y APIs con OpenAPI.

NestJS, React, Angular y .NET son tecnologías recomendadas según contexto, capacidades del equipo, ecosistema existente, requisitos y costo de operación; **no son obligaciones universales**. La decisión debe explicitar el problema que resuelve, alternativas consideradas y consecuencias.

## 8. Repositorio y documentación

### Estructura sugerida

```text
README.md
docs/
  funcional/
  tecnica/
  adr/
src/
tests/
  unit/
  integration/
  e2e/
openapi/
```

La estructura puede adaptarse al framework o legacy. No se debe mover código solo para cumplir una forma.

### Estándares mínimos

- **Obligatorio:** README con propósito, alcance, dependencias, configuración segura, ejecución, testing, despliegue y ownership.
- **Obligatorio:** documentación funcional y técnica actualizada cuando cambia el comportamiento o la operación.
- **Condicionado:** OpenAPI para APIs HTTP y contrato equivalente para otros protocolos.
- **Recomendado:** Mermaid para diagramas versionables y ADRs para decisiones con impacto futuro.
- **Obligatorio para IA:** mantener archivos de contexto del proyecto con reglas, arquitectura, comandos, límites y validaciones; no incluir secretos.

Consultar `gaci-doc-functional.md`, `gaci-doc-technical.md` y los módulos portables de [skills](./skills/).

## 9. Git, ramas, commits y Pull Requests

- **Obligatorio:** crear features desde `develop` y hotfixes desde `main`.
- **Obligatorio:** no commitear directamente en `main` ni `develop` protegidas.
- **Obligatorio:** todo cambio integrado pasa por PR, revisión y controles definidos.
- **Obligatorio:** un hotfix se revisa e integra hacia `main` y luego se reintegra a `develop` cuando corresponda, evitando que las ramas diverjan.
- **Obligatorio:** usar Conventional Commits (`feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`).
- **Recomendado:** mantener PRs pequeños, enfocados y con descripción de alcance, no objetivos, riesgos y evidencia.

La herramienta concreta de repositorio o CI puede variar; el control debe existir aunque cambie el proveedor. Usar `gaci-git-workflow.md` y la [Checklist de PR](./templates/Checklist-Pull-Request.md).

## 10. Calidad y testing

La estrategia depende del riesgo, criticidad, novedad, datos y superficie de integración.

| Tipo | Uso |
|---|---|
| **Unitarias** | Reglas de dominio, validaciones y casos de uso aislables. |
| **Integración** | Persistencia, mensajería, archivos, servicios o adaptadores reales. |
| **Contrato** | Compatibilidad entre consumidores y proveedores de APIs/eventos. |
| **E2E** | Flujos críticos completos, seleccionados por riesgo. |

- **Obligatorio:** cubrir reglas críticas y regresiones con pruebas automatizadas o evidencia equivalente justificada.
- **Obligatorio:** ejecutar lint, format, análisis estático y controles de seguridad disponibles en CI.
- **Condicionado:** exigir contrato o E2E cuando una falla de integración pueda afectar clientes, facturación, datos críticos o procesos irreversibles.
- **Excepción:** si no es viable automatizar una prueba, documentar riesgo, prueba manual, responsable y plan de automatización.

Los quality gates deben impedir la integración cuando fallan controles obligatorios, salvo excepción aprobada.

## 11. CI/CD, despliegue, rollback y migraciones

- **Obligatorio:** compilar, testear y ejecutar controles repetibles antes de desplegar.
- **Obligatorio:** separar configuración y secretos del código; promover artefactos verificables entre ambientes.
- **Obligatorio:** cada despliegue debe indicar versión, cambios, migraciones, validación posterior, owner y plan de rollback.
- **Recomendado:** despliegues pequeños, progresivos y observables.
- **Condicionado:** usar feature flags, canary o blue/green cuando el impacto, volumen o reversibilidad lo requiera.

Las migraciones de base de datos deben ser versionadas, revisadas, compatibles con la transición y probadas sobre una copia representativa. Preferir cambios expand/contract: agregar compatibilidad, migrar datos y retirar lo viejo en una etapa posterior. Un rollback de aplicación no siempre revierte datos; el plan debe tratar ambos riesgos por separado.

## 12. Seguridad y privacidad

- **Obligatorio:** nunca versionar secretos, tokens, credenciales ni datos productivos innecesarios.
- **Obligatorio:** aplicar mínimo privilegio, separación de ambientes, autenticación/autorización y registro de acciones sensibles.
- **Obligatorio:** revisar dependencias, vulnerabilidades conocidas, validación de entradas y exposición de errores.
- **Condicionado:** realizar threat modeling básico para autenticación, datos sensibles, integraciones externas, cambios de permisos o procesos críticos.
- **Obligatorio:** revisar manualmente todo código generado o modificado por IA, incluyendo dependencias, licencias, seguridad, rendimiento y cumplimiento de la arquitectura.

No enviar a asistentes de IA secretos, credenciales, información personal identificable, datos financieros, código confidencial no autorizado, dumps de producción ni documentación restringida. Sanitizar, minimizar y usar únicamente información aprobada.

## 13. Observabilidad y operación

- **Obligatorio:** logs estructurados con timestamp, correlación, resultado y contexto suficiente sin exponer datos sensibles.
- **Condicionado:** métricas y trazas para APIs, procesos asincrónicos, integraciones y flujos críticos.
- **Obligatorio:** definir owner operativo, alertas accionables, umbrales razonables y runbook para servicios críticos.
- **Recomendado:** medir disponibilidad, latencia, errores, volumen, colas, reintentos y resultado de negocio.

Un runbook debe explicar diagnóstico, acciones seguras, escalamiento, rollback/reprocesamiento y comunicación. Las alertas sin acción definida deben revisarse.

## 14. Incidentes y postmortems

Los incidentes se gestionan sin culpabilización. El objetivo es restaurar el servicio, reducir impacto y mejorar el sistema.

1. Detectar, clasificar y asignar un responsable de coordinación.
2. Contener y comunicar según impacto.
3. Recuperar con la acción más segura y registrar decisiones.
4. Confirmar estabilidad y cerrar técnicamente.
5. Elaborar un [postmortem](./templates/Plantilla-Postmortem.md) con línea de tiempo, impacto, causa contribuyente, detección, respuesta y acciones preventivas.

El análisis busca condiciones del sistema, procesos y controles; no castigos individuales. Las acciones deben tener owner y fecha.

## 15. Mantenimiento, dependencias y deuda técnica

- **Obligatorio:** registrar deuda técnica que afecte riesgo, costo, velocidad, seguridad o capacidad de cambio.
- **Obligatorio:** mantener dependencias soportadas o documentar el riesgo y la excepción.
- **Recomendado:** reservar capacidad periódica para actualización, simplificación, observabilidad y eliminación de código muerto.
- **Condicionado:** priorizar deuda según impacto, probabilidad, urgencia y costo de no resolverla.

Una dependencia no se actualiza solo por estar disponible: evaluar compatibilidad, seguridad, licencias, pruebas, migración y rollback.

## 16. Migración gradual desde GeneXus

La modernización preserva comportamiento de negocio antes de cambiar tecnología.

1. **Relevamiento:** identificar procesos, reglas, pantallas, datos, integraciones, jobs, usuarios y dependencias ocultas.
2. **Preservación de reglas:** documentar decisiones y comportamiento observable; validar con responsables funcionales.
3. **Coexistencia:** definir fronteras, contratos, ownership, sincronización, reconciliación y operación conjunta.
4. **Incremento:** extraer capacidades acotadas mediante strangler pattern u otra modernización incremental.
5. **Validación:** comparar resultados, ejecutar regresión, observar métricas y obtener aceptación.
6. **Retiro:** eliminar el componente viejo solo cuando el nuevo tenga ownership, soporte, datos y evidencia de estabilidad.

Riesgos principales: reglas implícitas, diferencias de redondeo/fechas, integraciones no documentadas, duplicación de datos, doble escritura, permisos, rendimiento y pérdida de conocimiento. Para cada riesgo definir control y responsable. `gaci-gx-bridge.md` es la referencia operativa; una migración puramente técnica no debe inventar trabajo GEM.

## 17. Uso corporativo de IA

### Puede hacer

Ayudar a explorar código, resumir, proponer alternativas, generar borradores, crear pruebas, detectar inconsistencias, actualizar documentación y acelerar tareas repetibles, siempre dentro de los permisos y contexto aprobados.

### Debe revisar la persona

Exactitud de reglas de negocio, seguridad, privacidad, dependencias, licencias, rendimiento, mantenibilidad, tests, compatibilidad con el legacy y trazabilidad. Quien integra el resultado es responsable de su comportamiento.

### Flujo mínimo

1. Definir objetivo, restricciones, archivos permitidos y resultado esperado.
2. Elegir skills portables por nombre real: `gaci-ai-usage.md`, `gaci-product-discovery.md`, `gaci-gx-bridge.md`, `gaci-git-workflow.md`, `gaci-nestjs-hexagonal.md`, `gaci-frontend-general.md`, `gaci-react.md`, `gaci-angular.md`, `gaci-ui-styles.md`, `gaci-doc-functional.md` y `gaci-doc-technical.md`.
3. Revisar el resultado línea por línea y contrastarlo con código y documentación reales.
4. Ejecutar pruebas y controles; registrar decisiones y limitaciones.
5. Mantener trazabilidad del cambio asistido sin atribuir a la IA responsabilidad de aprobación.

Las skills son módulos de contexto portables, no un formato propietario ni una obligación de adoptar una herramienta concreta.

## 18. Gobernanza, excepciones y evolución

El líder técnico y los responsables de negocio, calidad, seguridad o datos —según el impacto— gobiernan la aplicación del manual. La gobernanza debe ser proporcional al riesgo, no burocracia uniforme.

Una excepción debe registrar: estándar afectado, motivo, alcance, riesgo, mitigación, aprobador, owner, fecha de vigencia y condición de revisión. Las excepciones vencidas se revisan, renuevan o cierran.

La revisión del manual debe considerar incidentes, auditorías, feedback de equipos, cambios regulatorios, evolución tecnológica y resultados de adopción. La versión se incrementa con fecha, cambios relevantes y responsables. Ningún estándar de herramienta se vuelve corporativo por aparecer como ejemplo en este documento.

## 19. Plan de adopción gradual

### Fase 0 — Mínimo viable

- Clasificar cada proyecto y asignar owners.
- Exigir requerimiento con alcance, no objetivos, criterios de aceptación y trazabilidad.
- Proteger ramas, usar PR y commits comprensibles.
- Ejecutar controles básicos de build, tests disponibles, lint/format y revisión humana.
- Prohibir secretos en repositorios y definir rollback/owner para despliegues.

### Primeros 90 días

- Aplicar plantillas a nuevos cambios y documentar excepciones.
- Incorporar ADRs, quality gates, matriz de riesgos y runbooks para servicios críticos.
- Medir lead time, defectos, cambios fallidos, recuperación y cobertura de flujos críticos.
- Elegir un proyecto nuevo y uno GeneXus/híbrido como pilotos; ajustar el manual con evidencia.
- Capacitar roles y acordar el uso seguro de IA y skills portables.

### Evolución posterior

Extender testing de contrato/E2E según riesgo, observabilidad, análisis de dependencias, ownership de datos, migración incremental, revisiones periódicas de deuda y automatización de controles. La adopción se escala cuando el equipo puede demostrar valor y sostenibilidad, no por cumplimiento documental aislado.

## 20. Checklists de salida

### Requerimiento

- [ ] Objetivo, valor, usuarios y alcance definidos.
- [ ] No objetivos, supuestos, dependencias y riesgos explícitos.
- [ ] Reglas y criterios de aceptación observables.
- [ ] GEM vinculado o ausencia registrada sin inventar identificador.
- [ ] Owner funcional y técnico asignados.

### Diseño

- [ ] Alternativas y decisión documentadas.
- [ ] Dominio, aplicación, infraestructura y límites identificados.
- [ ] Datos, seguridad, privacidad, integraciones y observabilidad evaluados.
- [ ] Migraciones, compatibilidad, rollback y operación considerados.
- [ ] ADR, OpenAPI y/o Mermaid actualizados cuando corresponde.

### Desarrollo

- [ ] Rama creada desde la base correcta y commits convencionales.
- [ ] Reglas de negocio separadas de detalles tecnológicos según riesgo.
- [ ] Pruebas adecuadas y regresiones cubiertas.
- [ ] No hay secretos ni datos sensibles innecesarios.
- [ ] Código generado por IA revisado por una persona.

### Pull Request

- [ ] Alcance, no objetivos, riesgos y evidencia incluidos.
- [ ] GEM, requerimiento y ADR enlazados.
- [ ] CI y quality gates aprobados.
- [ ] Revisión técnica/funcional realizada.
- [ ] Documentación y plan de despliegue actualizados.

### Despliegue

- [ ] Artefacto y versión identificables.
- [ ] Migraciones probadas y ordenadas.
- [ ] Rollback de aplicación y datos definido.
- [ ] Owner, monitoreo, alertas y comunicación preparados.
- [ ] Validación posterior ejecutada y registrada.

### Operación

- [ ] Logs, métricas y trazas disponibles según riesgo.
- [ ] Runbook y escalamiento accesibles.
- [ ] Incidentes y aprendizajes registrados.
- [ ] Deuda técnica y dependencias revisadas.
- [ ] Ownership vigente y conocido por el equipo.

## Referencias internas

- [Manual de Desarrollo Estándar](./Manual-Desarrollo.md)
- [Módulos de contexto portables](./skills/)
- [README de la carpeta](./README.md)
- [Plantilla de requerimiento](./templates/Plantilla-Requerimiento.md)
- [Plantilla de ADR](./templates/Plantilla-ADR.md)
- [Plantilla de postmortem](./templates/Plantilla-Postmortem.md)
- [Checklist de Pull Request](./templates/Checklist-Pull-Request.md)
