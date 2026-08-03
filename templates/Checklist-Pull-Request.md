# Checklist de Pull Request — [Título]

## Contexto

- [ ] Requerimiento/GEM enlazado o ausencia registrada sin inventar identificador.
- [ ] Objetivo y valor explicados.
- [ ] Alcance y no objetivos explícitos.
- [ ] ADR, documentación funcional/técnica y diagramas enlazados cuando corresponde.

## Código y diseño

- [ ] La rama se creó desde `develop` (feature) o `main` (hotfix).
- [ ] El cambio respeta la arquitectura y separa reglas de negocio de detalles tecnológicos según riesgo.
- [ ] No hay secretos, credenciales ni datos sensibles innecesarios.
- [ ] El código generado o asistido por IA fue revisado línea por línea por una persona.
- [ ] Dependencias nuevas justificadas y evaluadas.

## Calidad y seguridad

- [ ] Estrategia de pruebas definida y ejecutada según el riesgo del cambio, con tipo, alcance, resultado y evidencia registrados.
- [ ] Pruebas de integración, contrato o E2E incluidas si el riesgo lo requiere.
- [ ] Regresiones y casos límite cubiertos.
- [ ] En cambios de documentación/configuración o cuando existe una excepción justificada, se documentó la validación aplicable sin agregar pruebas unitarias artificiales.
- [ ] Lint, format, análisis estático y quality gates aprobados.
- [ ] Seguridad, permisos, validación de entradas y privacidad revisados.

## Datos y operación

- [ ] Migraciones versionadas, compatibles y probadas cuando aplican.
- [ ] Logs, métricas, trazas y alertas definidos según criticidad.
- [ ] Despliegue, validación posterior y rollback documentados.
- [ ] Runbook y owner actualizados cuando el cambio afecta operación.

## Revisión y cierre

- [ ] Revisor técnico asignado y aprobación obtenida.
- [ ] Revisión funcional obtenida cuando cambia comportamiento de negocio.
- [ ] CI ejecutada sobre la versión final.
- [ ] Comentarios resueltos o documentados.
- [ ] Si es hotfix, se planificó la reintegración a `develop` cuando corresponda.
- [ ] GEM, documentación y resumen de cierre actualizados.
