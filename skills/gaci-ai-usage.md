# Uso de Inteligencia Artificial — Gaci

## Propósito
Definir reglas éticas, operativas y de seguridad para usar asistentes de inteligencia artificial generativa durante el desarrollo de Gaci.

## Cuándo usar
Aplicar al solicitar, revisar, modificar, probar o documentar código con cualquier asistente de IA, sin depender del proveedor o la interfaz utilizada.

## Entradas esperadas
- Contexto funcional: historias de usuario y reglas de negocio.
- Contexto técnico: archivos, arquitectura, restricciones y objetivo.
- Requisitos de seguridad, pruebas y alcance.

## Reglas obligatorias
1. La IA es copiloto, no piloto: la responsabilidad final es humana.
2. No aceptar código que el desarrollador no comprenda y pueda validar.
3. Revisar secretos, variables de entorno, endpoints sensibles e inyecciones.
4. Todo código asistido debe validarse de forma proporcional al riesgo. Cuando corresponda, debe contar con pruebas unitarias para escenarios normales, de error y casos borde; cuando no corresponda automatizarlas, se debe registrar evidencia alternativa y justificación.
5. Rechazar propuestas que contradigan las reglas de Gaci.
6. No usar modelos o servicios no autorizados ni subir información sensible a plataformas externas no aprobadas.
7. No integrar cambios masivos sin revisar cada archivo y verificar la coherencia del proyecto.

## Procedimiento
1. Definir rol, contexto, objetivo y restricciones. Ejemplo: “Actuá como desarrollador senior de NestJS y respetá Arquitectura Hexagonal”.
2. Proveer el contexto mínimo suficiente, sin secretos.
3. Evaluar la propuesta contra arquitectura, negocio, seguridad y pruebas.
4. Implementar solo lo comprendido; ejecutar pruebas y revisión de código.

## Salida esperada
Una solución revisada, segura, trazable y acompañada por pruebas o evidencia alternativa justificada, o una explicación explícita de por qué la propuesta no puede aceptarse.

## Restricciones
Los nombres de herramientas en ejemplos son ilustrativos; ninguna herramienta o proveedor concreto es requisito. Las reglas de Gaci prevalecen sobre cualquier sugerencia del asistente.
