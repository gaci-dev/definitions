# Manual de Desarrollo de Gaci

Esta carpeta contiene el marco corporativo, la guía técnica detallada y módulos portables para asistir tareas de desarrollo con IA.

## Qué leer

1. **Adopción y gobierno:** [Manual Corporativo V1.0](./Manual-Corporativo-V1.0.md). Es el punto de entrada: define principios, roles, ciclo de vida, calidad, seguridad, operación y checklists.
2. **Implementación técnica:** [Manual-Desarrollo.md](./Manual-Desarrollo.md). Complementa al manual corporativo con arquitectura hexagonal, frontend, Git, GEM y uso operativo de las skills.
3. **Contexto por tarea:** [skills/](./skills/). Son los 12 módulos portables existentes, independientes de OpenCode, Claude, Codex u otro proveedor.
4. **Documentación lista para copiar:** [templates/](./templates/). Incluye requerimientos, ADRs, postmortems y checklist de PR.
5. **Herramientas de documentación:** [tools/](./tools/). Incluye generadores para producir entregables editables y finales con el formato corporativo.

## Relación entre los materiales

El manual corporativo establece **qué debe gobernarse y por qué**. `Manual-Desarrollo.md` explica **cómo implementar** varias prácticas. Las skills aportan contexto especializado para una tarea concreta y las plantillas convierten el proceso en evidencia reutilizable. Ningún archivo reemplaza la revisión humana ni autoriza enviar datos sensibles a una IA.

## Skills disponibles

- [`gaci-ai-usage.md`](./skills/gaci-ai-usage.md)
- [`gaci-angular.md`](./skills/gaci-angular.md)
- [`gaci-doc-functional.md`](./skills/gaci-doc-functional.md)
- [`gaci-doc-technical.md`](./skills/gaci-doc-technical.md)
- [`gaci-frontend-general.md`](./skills/gaci-frontend-general.md)
- [`gaci-git-workflow.md`](./skills/gaci-git-workflow.md)
- [`gaci-gx-bridge.md`](./skills/gaci-gx-bridge.md)
- [`gaci-gxkb-navigation.md`](./skills/gaci-gxkb-navigation.md)
- [`gaci-nestjs-hexagonal.md`](./skills/gaci-nestjs-hexagonal.md)
- [`gaci-product-discovery.md`](./skills/gaci-product-discovery.md)
- [`gaci-react.md`](./skills/gaci-react.md)
- [`gaci-ui-styles.md`](./skills/gaci-ui-styles.md)

## Herramientas disponibles

- [`generador-documentacion`](./tools/generador-documentacion/README.md): genera documentos corporativos genéricos en PDF y DOCX editable a partir de una definición JSON.
- [`kb-extractor`](./tools/kb-extractor/README.md): normaliza exportaciones GeneXus XML/XPZ y selecciones GX9 GXL en una base de conocimiento portable.

## Orden mínimo de adopción

Leer el manual corporativo, clasificar el proyecto, copiar la plantilla de requerimiento, trabajar con PR y checklist, y agregar documentación/controles según riesgo. Las excepciones se registran; no se ocultan en conversaciones o código.
