# Documentación Funcional — Gaci

## Propósito
Documentar qué hace el sistema desde el negocio, con requisitos claros, reglas verificables y trazabilidad.

## Cuándo usar
Activar al relevar, definir, modificar o cerrar una funcionalidad, historia de usuario o regla de negocio.

## Entradas esperadas
Problema de negocio, usuarios, flujo esperado, reglas, excepciones, criterios de aceptación e identificador de GEM si existe.

## Reglas obligatorias
- Separar el qué funcional del cómo técnico.
- Usar lenguaje de negocio y evitar tecnicismos innecesarios.
- Explicitar reglas, validaciones y resultado ante errores.
- Si existe un evento/ticket GEM, vincular la documentación, la rama y el cierre a su ID. Si no existe, dejar explícita la ausencia y no inventar un identificador.
- Usar Mermaid para procesos o estados complejos.

## Procedimiento
1. Identificar rol, objetivo y beneficio.
2. Documentar escenarios en formato Dado/Cuando/Entonces.
3. Enumerar reglas y casos alternativos.
4. Registrar la trazabilidad disponible y generar el resumen de cierre; si existe GEM, publicarlo allí.

## Salida esperada
Historia o documento funcional en Markdown, listo para revisión y trazable a su trabajo asociado.

## Restricciones
No definir tecnología para resolver un problema que todavía no está entendido.

## Ejemplos

Este módulo define las pautas para crear, estructurar y mantener documentación de negocio (requerimientos, historias de usuario y reglas de negocio) clara, trazable y unificada.

---

## Referencia de formato
La documentación funcional describe el **QUÉ** hace el sistema desde el punto de vista del negocio, desacoplado del **CÓMO** se implementa técnicamente. Sirve como contrato entre los analistas que definen las reglas de Gaci y los desarrolladores que implementan el código.

## 2. Estructura de Requerimiento (User Story)
Cada funcionalidad o cambio debe documentarse utilizando el formato estándar de **Historia de Usuario**. La IA debe generar estas historias de forma clara y concisa para evitar ambigüedades.

```markdown
### Historia de Usuario: [Título descriptivo de la funcionalidad]
**Como** [rol del usuario (ej. Analista de Gaci, Usuario del sistema)],
**Quiero** [realizar una acción específica en el sistema],
**Para** [obtener un beneficio o resultado de negocio concreto].

**Criterios de Aceptación (Escenarios):**
1. **Dado** [contexto inicial], **Cuando** [acción del usuario], **Entonces** [resultado esperado].
2. **Dado** [condición alternativa], **Cuando** [acción inválida], **Entonces** [mensaje de error esperado].
3. **Reglas de Negocio:**
   - [Lista explícita de restricciones, validaciones o cálculos de negocio que el sistema debe respetar].
```

## 3. Gestión de Trazabilidad (Integración con GEM)
Cuando existe un evento o ticket GEM, la documentación funcional debe estar vinculada a su identificador único (número de tarea, ID de evento o tag de versión). Si la tarea no tiene GEM, se documenta explícitamente esa ausencia y no se inventa un identificador.

* **Mapeo de Commits y ramas:** Cuando existe GEM, la documentación funcional debe referenciar el nombre de la rama de trabajo y el identificador (ej. `feature/GEM-105-crear-api-cheeky`).
* **Etiquetado de eventos:** Al cerrar una historia vinculada a GEM, la IA o el desarrollador debe generar un resumen técnico que se registre como comentario en la tarea correspondiente.

### Plantilla para Resumen de Cierre (Pegar en GEM cuando exista)
```markdown
**Funcionalidad Cerrada:** [Título de la Historia de Usuario]
**Estado:** Implementada y probada.
**Impacto Negocio:** [Descripción breve de cómo este cambio soluciona la necesidad del usuario].
**Commits Asociados:** [Listar hashes o números de commit principal].
```

## 4. Reglas de Estilo para Documentación Funcional
1. **Lenguaje del Negocio:** Evitar tecnicismos de programación en la descripción de la historia (ej. no decir "crear un endpoint", sino "disponer de la información para visualizar").
2. **Claridad Absoluta:** Si un cálculo es complejo (ej. Liquidación de IVA), documentarlo paso a paso en un archivo de conocimiento anexo y referenciarlo desde la Historia de Usuario.
3. **Uso de Diagramas Mermaid:** Para procesos de negocio secuenciales o de estados complejos, usar la sintaxis de Mermaid para generar diagramas visuales directamente en el Markdown (ej. `graph TD; A-->B;`).
