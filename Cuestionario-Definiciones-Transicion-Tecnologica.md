# Cuestionario de definiciones para la transición tecnológica

**Gaci · Documento de trabajo para reunión**  
**Versión:** 0.1 · **Fecha de preparación:** 2026-07-29  
**Propósito:** ayudar a Juli y al equipo a completar definiciones surgidas de la conversación sobre stack, orden interno, transición desde GeneXus y uso de IA.

> **Importante:** este documento no es una política aprobada ni reemplaza al `Manual-Corporativo-V1.0.md`. Las preguntas, ejemplos y alternativas deben discutirse y aprobarse según corresponda.
>
> **Marca de ejemplos:** todo bloque rotulado `EJEMPLO — NO APROBADO — NO USAR COMO REGLA` es ilustrativo y no puede trasladarse al manual ni aplicarse como criterio hasta contar con aprobación explícita.

## Cómo usar este cuestionario

1. No responder por intuición individual si requiere decisión de dirección.
2. Registrar desacuerdos y alternativas, en lugar de ocultarlos o resolverlos informalmente.
3. Separar hechos actuales, decisiones y propuestas.
4. No convertir ejemplos en acuerdos automáticamente.
5. Llevar las respuestas aprobadas luego al `Manual-Corporativo-V1.0.md` o a un anexo operativo.

### Convenciones de registro

- **Tipo:** `Decisión requerida`, `Dato a relevar`, `Criterio a definir` o `Pendiente`.
- **Estado sugerido:** `Abierto`, `En análisis`, `Acordado`, `Bloqueado`, `Descartado`.
- Completar cada campo con información verificable o indicar `A confirmar`.
- Si una respuesta tiene condiciones, registrar la condición y quién puede exceptuarla.

---

## 1. Objetivo y alcance de la transición tecnológica

**Tipo:** `Decisión requerida`  
**Problema que estamos tratando de resolver:** Gaci necesita pasar de una situación dominada por GeneXus a una convivencia ordenada con un stack moderno, sin convertir la modernización en una migración indiscriminada ni interrumpir el servicio a clientes.

### Preguntas para responder en reunión

- ¿Qué resultados concretos esperamos de la transición: velocidad, mantenibilidad, disponibilidad de talento, integración, experiencia de usuario, costo u otros?
- ¿Qué queda dentro del alcance de esta transición y qué queda explícitamente fuera?
- ¿La transición es por producto, por módulo, por capacidad transversal o por fecha? ¿Por qué?
- ¿Qué condiciones deben cumplirse para considerar que una etapa terminó?
- ¿Qué riesgos no estamos dispuestos a aceptar durante la transición?
- ¿Quién puede modificar el objetivo o el alcance?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Modernizar primero productos nuevos y módulos con alto costo de cambio, manteniendo GeneXus en sistemas estables hasta contar con una justificación técnica y económica.

### Espacio de respuesta y acuerdo

| Campo | Respuesta / acuerdo | Evidencia o comentario |
|---|---|---|
| Objetivo principal |  |  |
| Alcance incluido |  |  |
| Alcance excluido |  |  |
| Criterio de éxito |  |  |
| Riesgo aceptable / no aceptable |  |  |
| Aprobador |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 2. Diagnóstico de la situación actual

**Tipo:** `Dato a relevar`  
**Problema que estamos tratando de resolver:** No se puede priorizar una transición sin una imagen común de los proyectos parados, la base instalada, la capacidad real del equipo y las causas de los bloqueos.

### Preguntas para responder en reunión

1. ¿Qué proyectos están parados?
2. ¿En qué estado se encuentra cada proyecto parado?
3. ¿Desde cuándo está detenido cada proyecto?
4. ¿Qué sistemas GeneXus siguen siendo críticos?
5. ¿Quién conoce cada sistema GeneXus crítico?
6. ¿Qué dependencias tiene cada sistema GeneXus crítico?
7. ¿Qué capacidad mensual existe por especialidad?
8. ¿Cuánta capacidad mensual está comprometida con clientes?
9. ¿Cuál es la causa principal de la detención de cada proyecto: alcance, decisión pendiente, datos, integración, ambiente, capacidad, deuda o dependencia externa?
10. ¿Qué conocimiento está concentrado en una sola persona y en qué sistema o proyecto?
11. ¿Qué datos actuales son hechos comprobables?
12. ¿Qué datos actuales son estimaciones y cómo se identifican?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Armar un inventario con columnas para producto, cliente, versión de GeneXus, responsables, horas pendientes estimadas, última entrega, bloqueo principal y evidencia.

### Espacio de respuesta y acuerdo

| Producto / proyecto | Estado actual | Base instalada / versión | Capacidad necesaria | Causa del bloqueo | Conocimiento concentrado | Hecho / estimación | Evidencia |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

**Responsable del relevamiento:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 3. Modelo híbrido GeneXus + stack moderno

**Tipo:** `Criterio a definir`  
**Problema que estamos tratando de resolver:** La convivencia de tecnologías puede producir decisiones inconsistentes, duplicación de capacidades y excepciones sin autoridad clara si no se define cuándo conviene cada enfoque.

### Preguntas para responder en reunión

1. ¿En qué casos se mantiene GeneXus?
2. ¿En qué casos se elige stack moderno?
3. ¿Cuándo se permite una solución híbrida dentro del mismo producto?
4. ¿Qué excepciones son válidas?
5. ¿Qué evidencia debe presentar cada excepción?
6. ¿Quién aprueba una excepción?
7. ¿Por cuánto tiempo es válida cada excepción?
8. ¿Cómo se documentan la deuda y el costo de reversión?
9. ¿Cuál es el plan de salida de cada excepción o decisión híbrida?
10. ¿Qué decisión se toma si la velocidad inicial contradice la mantenibilidad?
11. ¿Qué decisión se toma si la velocidad inicial contradice la seguridad?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Mantener GeneXus para un sistema estable con bajo cambio y alto riesgo operativo; elegir stack moderno para una experiencia nueva con integración API, necesidades de escalabilidad y disponibilidad de talento.

### Espacio de respuesta y acuerdo

| Situación / decisión | Opción elegida | Condiciones y evidencia requerida | Aprobador | Vigencia / plan de salida |
|---|---|---|---|---|
| Sistema estable, bajo cambio |  |  |  |  |
| Producto nuevo |  |  |  |  |
| Módulo con integración externa |  |  |  |  |
| Excepción válida |  |  |  |  |
| Deuda y costo de reversión |  |  |  |  |
| Conflicto entre velocidad, mantenibilidad y seguridad |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 4. Criterios para seleccionar stack por producto

**Tipo:** `Criterio a definir`  
**Problema que estamos tratando de resolver:** Elegir tecnologías por preferencia individual puede aumentar el costo de soporte y hacer imposible comparar productos o justificar excepciones.

### Preguntas para responder en reunión

1. ¿Qué dimensiones se evalúan: dominio, integraciones, datos, rendimiento, seguridad, talento, costo, soporte y ciclo de vida?
2. ¿Qué criterios son obligatorios?
3. ¿Qué criterios son comparativos?
4. ¿Cómo se pondera cada criterio?
5. ¿Quién puede cambiar la ponderación?
6. ¿Qué nivel de evidencia se exige antes de seleccionar un stack?
7. ¿Se debe preferir tecnología ya operada por Gaci?
8. ¿Cómo se evalúan las licencias?
9. ¿Cómo se evalúa la dependencia de proveedor?
10. ¿Cómo se evalúa la obsolescencia?
11. ¿Qué prueba mínima debe existir antes de llevar la decisión a producción?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Usar una matriz de 1 a 5 para dominio, integración, rendimiento, seguridad, talento disponible, costo operativo y facilidad de migración, con una justificación escrita para cada puntaje.

### Espacio de respuesta y acuerdo

| Criterio / regla | ¿Obligatorio? | Peso / método | Evidencia mínima | Responsable de evaluar |
|---|---:|---:|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
| Regla para cambiar ponderaciones |  |  |  |  |
| Preferencia por tecnología operada por Gaci |  |  |  |  |
| Licencias, proveedor y obsolescencia |  |  |  |  |
| Prueba mínima antes de producción |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 5. Clasificación y priorización de productos candidatos

**Tipo:** `Decisión requerida`  
**Problema que estamos tratando de resolver:** Hay iniciativas atractivas —como portal de pacientes, automatización de facturas y WMS— pero todavía no debe asumirse que están aprobadas ni que tienen la misma prioridad, valor o riesgo.

### Preguntas para responder en reunión

- ¿Qué problema de negocio resuelve cada candidato y para quién?
- ¿Es una iniciativa de cliente, interna, exploratoria o estratégica?
- ¿Qué valor, urgencia, riesgo y dependencia tiene?
- ¿Qué evidencia existe de demanda, alcance y capacidad disponible?
- ¿Qué candidato sirve para aprender sin comprometer producción?
- ¿Qué condición debe cumplirse para pasar de candidato a iniciativa aprobada?
- ¿Quién prioriza cuando compiten entre sí?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Comparar portal de pacientes, automatización de facturas y WMS en una matriz de valor esperado, urgencia, esfuerzo, riesgo de integración, aprendizaje y capacidad requerida.

### Espacio de respuesta y acuerdo

| Candidato | Problema / usuario | Valor | Esfuerzo | Dependencias | Prioridad provisoria | Decisión |
|---|---|---:|---:|---|---|---|
| Portal de pacientes |  |  |  |  |  |  |
| Automatización de facturas |  |  |  |  |  |  |
| WMS |  |  |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 6. Evaluación específica del WMS

**Tipo:** `Decisión requerida`  
**Problema que estamos tratando de resolver:** El WMS puede ser una oportunidad de aprendizaje y de negocio, pero una estimación de 200–300 horas, datos mock o un prototipo no demuestran por sí solos que exista una solución productiva viable.

### Preguntas para responder en reunión

- ¿Qué valor de negocio se espera y cómo se medirá?
- ¿Qué incluye exactamente la estimación de 200–300 horas y qué queda fuera?
- ¿Qué integraciones son necesarias: ERP, stock, compras, expedición, dispositivos, usuarios o clientes?
- ¿Qué volumen, concurrencia, latencia y disponibilidad debe soportar?
- ¿Qué datos mock son aceptables para aprender y qué datos reales se necesitan para validar?
- ¿Qué diferencia habrá entre prototipo, piloto y producción?
- ¿Qué criterios permiten detener, continuar o rediseñar el trabajo?
- ¿Quién es dueño del producto y quién aprueba el paso a producción?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Un prototipo podría validar el flujo de recepción y picking con datos mock; no podría presentarse como listo para producción hasta validar integración, seguridad, rendimiento, recuperación ante errores, trazabilidad y operación.

### Espacio de respuesta y acuerdo

| Aspecto | Prototipo | Piloto | Producción | Respuesta / evidencia |
|---|---|---|---|---|
| Objetivo |  |  |  |  |
| Datos permitidos |  |  |  |  |
| Integraciones |  |  |  |  |
| Rendimiento esperado |  |  |  |  |
| Seguridad y auditoría |  |  |  |  |
| Criterio de salida |  |  |  |  |

**Estimación revisada:** ______ · **Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 7. Orden interno de desarrollo

**Tipo:** `Criterio a definir`  
**Problema que estamos tratando de resolver:** Sin un orden común para ramas, PRs, impactos de base de datos, conflictos, releases y paquetes, el trabajo puede bloquearse o llegar a producción sin trazabilidad.

### Preguntas para responder en reunión

- ¿Cuál es el flujo de ramas y qué nombre o propósito tiene cada una?
- ¿Qué debe contener un PR y quién lo revisa?
- ¿Cómo se detectan y coordinan impactos de base de datos?
- ¿Cómo se resuelven conflictos entre iniciativas?
- ¿Qué condiciones habilitan una release y quién la aprueba?
- ¿Qué se publica en GitHub Packages, con qué versionado y quién puede consumirlo?
- ¿Cómo se comunica un cambio incompatible?
- ¿Qué evidencia queda de rollback, migraciones y configuración?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Exigir que un PR con migración de base de datos incluya impacto, plan de despliegue, compatibilidad hacia atrás y plan de reversión antes de aprobarse.

### Espacio de respuesta y acuerdo

| Elemento | Definición acordada | Responsable / aprobador | Evidencia |
|---|---|---|---|
| Ramas |  |  |  |
| PR y revisiones |  |  |  |
| Base de datos |  |  |  |
| Conflictos |  |  |  |
| Release |  |  |  |
| GitHub Packages |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 8. Capacidad protegida: clientes, internos, documentación, deuda y automatización

**Tipo:** `Decisión requerida`  
**Problema que estamos tratando de resolver:** La urgencia de clientes puede consumir toda la capacidad y dejar sin espacio la transición, la documentación, la deuda técnica y la automatización que sostendrán el futuro.

### Preguntas para responder en reunión

- ¿Qué proporción de capacidad se protege para clientes, desarrollos internos, deuda, documentación y automatización?
- ¿La proporción es fija o cambia por trimestre y por emergencia?
- ¿Quién autoriza consumir la capacidad protegida?
- ¿Cómo se registra el trabajo que no genera una entrega inmediata?
- ¿Qué iniciativas internas se priorizan y con qué criterio?
- ¿Cómo se evita que una estimación optimista destruya la capacidad reservada?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Reservar una capacidad trimestral explícita para documentación y automatización, y permitir consumirla sólo con una decisión registrada de dirección.

### Espacio de respuesta y acuerdo

| Uso de capacidad | Porcentaje / horas | Regla de uso | Aprobador | Métrica |
|---|---:|---|---|---|
| Clientes |  |  |  |  |
| Desarrollo interno |  |  |  |  |
| Documentación |  |  |  |  |
| Deuda técnica |  |  |  |  |
| Automatización |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 9. Repositorio único de conocimiento

**Tipo:** `Decisión requerida`  
**Problema que estamos tratando de resolver:** La información distribuida o desactualizada dificulta operar, incorporar personas, decidir sobre migraciones y permitir que la IA use contexto confiable sin exponer información indebida.

### Preguntas para responder en reunión

1. ¿Cuál es la ubicación oficial del conocimiento?
2. ¿Qué estructura mínima tendrá la sección de productos?
3. ¿Qué estructura mínima tendrá la sección de arquitectura?
4. ¿Qué estructura mínima tendrá la sección de decisiones?
5. ¿Qué estructura mínima tendrá la sección de operación?
6. ¿Qué estructura mínima tendrá la sección de clientes?
7. ¿Qué estructura mínima tendrá la sección de datos?
8. ¿Qué estructura mínima tendrá la sección de reuniones?
9. ¿Quién es owner de cada sección?
10. ¿Quién revisa la vigencia de cada sección?
11. ¿Qué contenido puede leer una IA?
12. ¿Qué contenido debe quedar restringido para una IA?
13. ¿Cómo se controlan los permisos?
14. ¿Cómo se controlan los secretos?
15. ¿Cómo se controlan los datos personales?
16. ¿Cómo se controlan las credenciales?
17. ¿Cada cuánto se actualiza cada sección?
18. ¿Cómo se detecta contenido obsoleto?
19. ¿Qué documento prevalece si hay contradicciones?
20. ¿Cómo se enlaza la evidencia con el repositorio?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Mantener un índice único con links a repositorios, ADRs, runbooks, decisiones y fichas de producto, sin copiar secretos ni datos personales en el contexto de un agente.

### Espacio de respuesta y acuerdo

| Decisión | Respuesta / acuerdo | Owner | Revisión | Control de acceso |
|---|---|---|---|---|
| Ubicación |  |  |  |  |
| Estructura |  |  |  |  |
| Ownership |  |  |  |  |
| Acceso de IA |  |  |  |  |
| Seguridad |  |  |  |  |
| Vigencia |  |  |  |  |
| Documento prevalente ante contradicciones |  |  |  |  |
| Enlace de evidencia |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 10. Uso de IA y agentes

**Tipo:** `Criterio a definir`  
**Problema que estamos tratando de resolver:** La IA puede acelerar tareas, pero sin límites, revisión humana y métricas puede introducir errores, filtrar información o generar costos y dependencia difíciles de controlar.

### Preguntas para responder en reunión

- ¿Qué tareas se permiten: documentación, tests, refactor, análisis, scaffolding, migración u operación?
- ¿Qué tareas requieren aprobación humana antes de ejecutarse o integrarse?
- ¿Qué datos sensibles no pueden enviarse a herramientas de IA?
- ¿Qué evidencia debe acompañar una contribución generada con IA?
- ¿Cómo se miden calidad, rendimiento, seguridad, costo y tiempo ahorrado?
- ¿Qué nivel de madurez se exige antes de usar agentes para migración GeneXus?
- ¿Puede un agente modificar base de datos, infraestructura o producción? ¿Bajo qué controles?
- ¿Cómo se registra el uso de modelos, prompts relevantes y revisión?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Permitir que un agente proponga tests o documentación en una rama aislada, pero exigir revisión humana, ejecución de pruebas y aprobación de PR antes de incorporar cambios.

### Espacio de respuesta y acuerdo

| Capacidad de IA | Permitida | Revisión humana | Datos prohibidos | Métrica / evidencia |
|---|---|---|---|---|
| Documentación |  |  |  |  |
| Tests |  |  |  |  |
| Refactor |  |  |  |  |
| Migración |  |  |  |  |
| Infraestructura / producción |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 11. Roles y responsables

**Tipo:** `Criterio a definir`  
**Problema que estamos tratando de resolver:** Las decisiones se demoran o quedan implícitas cuando no está claro quién decide, quién aporta información, quién ejecuta y quién responde por cada iniciativa.

### Preguntas para responder en reunión

- ¿Qué decisiones corresponden a dirección?
- ¿Qué autoridad tienen los referentes técnicos?
- ¿Quién representa la perspectiva funcional y del cliente?
- ¿Quién valida infraestructura, seguridad y datos?
- ¿Quién es responsable final de cada iniciativa candidata?
- ¿Cómo se reemplaza temporalmente a un responsable ausente?
- ¿Qué conflictos de prioridad debe resolver dirección?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Usar una matriz RACI por iniciativa: dirección como aprobadora, referente técnico como responsable de la solución, referente funcional como dueño del problema y seguridad/datos/infraestructura como consultados u obligatorios según impacto.

### Espacio de respuesta y acuerdo

| Rol / persona | Responsabilidad | Autoridad | Reemplazo | Iniciativa |
|---|---|---|---|---|
| Dirección |  |  |  |  |
| Referente técnico |  |  |  |  |
| Referente funcional |  |  |  |  |
| Infraestructura |  |  |  |  |
| Seguridad |  |  |  |  |
| Datos |  |  |  |  |
| Responsable de iniciativa |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 12. Migración y aprendizaje externo

**Tipo:** `Dato a relevar`  
**Problema que estamos tratando de resolver:** La experiencia de Gabriel Fernández puede aportar aprendizajes, pero copiar una solución externa sin entender contexto, métricas, costos y restricciones puede trasladar problemas en lugar de resolverlos.

### Preguntas para hacerle a Gabriel Fernández

- ¿Qué problema intentaron resolver y cuál era su contexto inicial?
- ¿Qué arquitectura y stack eligieron, y qué alternativas descartaron?
- ¿Qué parte migraron primero y por qué?
- ¿Qué métricas tenían antes y después: tiempo de entrega, incidentes, rendimiento, costo y calidad?
- ¿Qué supuestos resultaron falsos?
- ¿Qué esfuerzo de capacitación, operación y mantenimiento requirió?
- ¿Qué salió mal y cómo lo corrigieron?
- ¿Qué recomendaría no copiar sin adaptar?
- ¿Qué evidencia podría compartir y bajo qué restricciones?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Pedir una comparación antes/después con métricas y luego contrastarla con el tamaño del equipo, la base instalada y las restricciones de Gaci, en vez de adoptar automáticamente su stack.

### Espacio de respuesta y acuerdo

| Tema consultado | Respuesta de Gabriel | Evidencia | Aplicabilidad a Gaci | Próxima validación |
|---|---|---|---|---|
| Contexto |  |  |  |  |
| Stack y alternativas |  |  |  |  |
| Métricas |  |  |  |  |
| Costos y operación |  |  |  |  |
| Errores / aprendizajes |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

## 13. Gobernanza y decisiones pendientes

**Tipo:** `Decisión requerida`  
**Problema que estamos tratando de resolver:** Sin un registro de decisiones, fechas, aprobadores, excepciones y revisiones, los acuerdos se pierden y el manual termina expresando recomendaciones desactualizadas como si fueran reglas vigentes.

### Preguntas para responder en reunión

- ¿Dónde se registra cada decisión y qué ID recibe?
- ¿Quién puede aprobar, rechazar o reabrir una decisión?
- ¿Qué información mínima debe tener una decisión?
- ¿Cómo se registran alternativas y desacuerdos?
- ¿Cómo se vencen o revisan las excepciones?
- ¿Cuándo se revisa el manual y quién valida el cambio?
- ¿Qué decisiones deben quedar en el manual y cuáles en un anexo operativo?

### EJEMPLO — NO APROBADO — NO USAR COMO REGLA

> Revisar mensualmente el registro de decisiones abiertas y trimestralmente las reglas del manual, manteniendo cada excepción con dueño, fecha de vencimiento y evidencia.

### Espacio de respuesta y acuerdo

| Elemento | Definición acordada | Responsable | Aprobador | Frecuencia |
|---|---|---|---|---|
| Registro de decisiones |  |  |  |  |
| Excepciones |  |  |  |  |
| Revisión del manual |  |  |  |  |
| Reapertura |  |  |  |  |

**Responsable:** ______ · **Participantes:** ______ · **Fecha objetivo:** ______ · **Estado:** ______  
**Evidencia/documento relacionado:** ______

---

## Tabla consolidada de decisiones pendientes

| ID | Tema | Pregunta | Responsable | Fecha | Estado | Decisión | Evidencia |
|---|---|---|---|---|---|---|---|
| D-01 | Objetivo y alcance | ¿Cuál es el resultado y límite de la transición? |  |  | Abierto |  |  |
| D-02 | Diagnóstico | ¿Cuál es el inventario verificable de proyectos y capacidad? |  |  | Abierto |  |  |
| D-03 | Modelo híbrido | ¿Cuándo usar GeneXus, moderno o híbrido? |  |  | Abierto |  |  |
| D-04 | Stack | ¿Qué criterios y pesos se usarán por producto? |  |  | Abierto |  |  |
| D-05 | Cartera | ¿Cómo se priorizan portal, facturas y WMS? |  |  | Abierto |  |  |
| D-06 | WMS | ¿Qué valida el prototipo y qué habilita producción? |  |  | Abierto |  |  |
| D-07 | Desarrollo | ¿Cuál será el flujo de ramas, PRs, releases y paquetes? |  |  | Abierto |  |  |
| D-08 | Capacidad | ¿Qué capacidad se protege y quién puede reasignarla? |  |  | Abierto |  |  |
| D-09 | Conocimiento | ¿Cuál es el repositorio oficial y cómo se controla el acceso? |  |  | Abierto |  |  |
| D-10 | IA | ¿Qué tareas y datos se permiten, con qué revisión y métricas? |  |  | Abierto |  |  |
| D-11 | Roles | ¿Quién decide y responde por cada iniciativa? |  |  | Abierto |  |  |
| D-12 | Aprendizaje externo | ¿Qué evidencia se pedirá a Gabriel y cómo se adaptará? |  |  | Abierto |  |  |
| D-13 | Gobernanza | ¿Cómo se registran, aprueban y revisan decisiones? |  |  | Abierto |  |  |

## Hechos reportados y pendientes de validación

> Completar sólo con afirmaciones que el grupo pueda confirmar como hechos o acuerdos explícitos. No mezclar propuestas ni preguntas abiertas.
>
> **Instrucción obligatoria:** H-01, H-02 y H-03 no deben trasladarse al manual como hechos hasta completar la evidencia y validarlos en reunión.

### Hechos actuales confirmados

| ID | Hecho | Quién lo confirmó | Evidencia | Estado |
|---|---|---|---|---|
| H-01 | Gaci cuenta con una base instalada relevante en GeneXus. |  |  | A validar en reunión |
| H-02 | Existen proyectos o iniciativas detenidas que requieren diagnóstico. |  |  | A validar en reunión |
| H-03 | Se conversó sobre stack moderno, orden interno y uso de IA. |  |  | A validar en reunión |

### Propuestas, no acuerdos

| ID | Propuesta | Autor / fuente | Qué falta validar |
|---|---|---|---|
| P-01 | Evaluar portal de pacientes, automatización de facturas y WMS como candidatos. |  |  |
| P-02 | Analizar un WMS con una estimación preliminar de 200–300 horas. |  |  |
| P-03 | Usar un repositorio único de conocimiento y agentes bajo revisión humana. |  |  |

### Preguntas abiertas

| ID | Pregunta | Responsable de responder | Fecha |
|---|---|---|---|
| A-01 | ¿Qué stack se recomienda para cada producto y con qué evidencia? |  |  |
| A-02 | ¿Qué capacidad puede protegerse sin comprometer clientes? |  |  |
| A-03 | ¿Qué madurez se exige para agentes de migración? |  |  |

## Checklist de cierre de la próxima reunión

- [ ] Se confirmó el objetivo y el alcance de la transición.
- [ ] Se separaron hechos actuales, decisiones y propuestas.
- [ ] Se completó o asignó el diagnóstico de proyectos, base instalada, capacidad y causas.
- [ ] Se acordaron criterios para GeneXus, stack moderno, híbrido y excepciones.
- [ ] Se clasificaron portal de pacientes, automatización de facturas y WMS sin asumir aprobación.
- [ ] Se aclaró qué significa prototipo, piloto y producción para el WMS.
- [ ] Se definió el flujo mínimo de ramas, PRs, base de datos, releases y GitHub Packages.
- [ ] Se acordó cómo proteger capacidad para clientes, internos, documentación, deuda y automatización.
- [ ] Se asignó owner al repositorio de conocimiento y se discutieron permisos de IA y seguridad.
- [ ] Se definieron límites, revisión humana y métricas para IA y agentes.
- [ ] Cada decisión tiene responsable, aprobador, fecha, estado y evidencia.
- [ ] Se registraron desacuerdos, alternativas y decisiones postergadas.
- [ ] Se acordó qué respuestas van al `Manual-Corporativo-V1.0.md` y cuáles a un anexo operativo.

## Cómo convertir las respuestas en documentación

1. **Limpiar el registro:** separar hechos confirmados, decisiones aprobadas, propuestas descartadas y preguntas que siguen abiertas.
2. **Verificar autoridad:** confirmar que cada decisión fue tomada por el nivel que corresponde y registrar aprobador y fecha.
3. **Conservar evidencia:** enlazar actas, inventarios, métricas, ADRs, pruebas, estimaciones y acuerdos de excepción.
4. **Elegir destino:** llevar principios y reglas estables al `Manual-Corporativo-V1.0.md`; llevar procedimientos, matrices, checklists y detalles cambiantes a un anexo operativo.
5. **Redactar sin ejemplos ambiguos:** eliminar o rotular cualquier ejemplo que no haya sido aprobado.
6. **Revisar impactos:** verificar coherencia con seguridad, datos, infraestructura, clientes, contratos y operación.
7. **Publicar con control:** asignar versión, owner, fecha de vigencia y próxima revisión.
8. **Comunicar el cambio:** informar qué cambió, desde cuándo aplica, a quién afecta y dónde consultar la evidencia.

### Registro de conversión

| Respuesta / decisión | Destino | Owner de documentación | Aprobador | Fecha de publicación | Link |
|---|---|---|---|---|---|
|  | Manual / anexo |  |  |  |  |
|  | Manual / anexo |  |  |  |  |
