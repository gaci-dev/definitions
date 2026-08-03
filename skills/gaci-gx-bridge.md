# Puente GeneXus (Legacy a Moderno) — Gaci

## Propósito
Extraer la intención de negocio de GeneXus y transformarla en documentación funcional y técnica moderna, sin traducir línea por línea.

## Cuándo usar
Activar al analizar código, transacciones, eventos, layouts o una base de conocimiento GeneXus para documentar o planificar una migración.

## Entradas esperadas
Código GX, `.kb`, transacción, eventos, pantallas, parámetros, datos y contexto funcional disponible.

## Reglas obligatorias
- Identificar reglas, triggers, condiciones, fórmulas, datos, inputs y eventos.
- Mantener el vocabulario de negocio original.
- Reestructurar deuda técnica; no copiar la mala estructura de GX.
- Registrar bugs o atajos detectados.
- Relacionar la salida funcional con `gaci-doc-functional.md` y la técnica con `gaci-nestjs-hexagonal.md` cuando corresponda.

## Procedimiento
1. Analizar reglas y modelo de datos oculto.
2. Mapear pantallas, entradas y eventos.
3. Separar reglas de negocio, flujo funcional y propuesta técnica.
4. Generar mapeo a dominio, aplicación e infraestructura.
5. Dividir la funcionalidad en historias y documentar trazabilidad.

## Salida esperada
Documento de migración con reglas, flujos, deuda técnica, mapeo hexagonal e historias de usuario.

## Restricciones
No inventar comportamiento ausente en la fuente ni comprometer una implementación moderna sin señalar supuestos.

## Ejemplos

Este módulo establece el protocolo para analizar código o transacciones de GeneXus (GX 9 o GX 18) y traducirlas a documentación técnica y funcional moderna. El objetivo es extraer el **"Know-How"** encapsulado en el sistema legado y transformarlo en especificaciones limpias.

---

## Referencia de análisis
GeneXus oculta la complejidad técnica bajo la alfombra. La IA debe actuar como un ingeniero de software que "desempaca" esa lógica. No se trata de traducir el código GX línea por línea a otro lenguaje, sino de **documentar la intención del negocio** que ese código implementaba.

## 2. Protocolo de Análisis de Código GeneXus
Cuando el usuario pego código GX, realice un *upload* de un `.kb` o describa una transacción, la IA debe extraer información en tres capas:

### Capa 1: Reglas de Negocio (La magia de GX)
*   **Ejecutar el código mentalmente:** Identificar los triggers (`AfterLevel`, `Start`, `Valid`), las condiciones (`If`, `Event`) y las fórmulas.
*   **Traducción a Lenguaje Humano:** Transformar la lógica condicional de GX en reglas de negocio claras. (Ej. El código de GX `if Stock < 0 { Error('No hay stock'); }` se documenta como: *"Regra de Validação: O sistema não permite registrar saídas caso o estoque disponível seja inferior à quantidade solicitada."*).
*   **Descubrir el Modelo de Datos Oculto:** Analizar cómo GX define las variables y parámetros para deducir la estructura de la base de datos relacional subyacente (entidades y relaciones).

### Capa 2: Flujos de Pantalla (Interfaces)
*   **Análisis de layouts:** Extraer de los controles de la pantalla GX qué información se muestra al usuario y qué inputs recibe.
*   **Identificar eventos:** Mapear qué acciones del usuario disparen qué lógica en el backend (ej. botón "Guardar" dispara un Commit en GX).

---

## 3. Generación de Documentación Moderna
Una vez analizado el código GX, la IA debe generar un documento de migración que incluya:

### A. Especificación Técnica Moderna (Para NestJS/Hexagonal)
La IA debe sugerir cómo mapear la lógica de GX a una Arquitectura Hexagonal.
*   **Entidad de Dominio:** La IA sugiere cómo crear una entidad pura que contenga la lógica de validación que antes vivía en GX.
*   **Caso de Uso:** La IA documenta el flujo de datos que antes hacía GX automáticamente en un Use Case explícito.

#### Ejemplo de Salida Técnica (Post-Análisis de GX)
```markdown
### Mapeo de Lógica de GX a Hexagonal
**Fuente GX:** Transacción `Pedidos GX` (Evento: `Valid`)
**Problema:** GX validaba stock en el mismo nivel de la grilla.
**Solución Moderna:**
1. **Domain:** Crear entidad `Pedido` con método `validarStockDisponible()`.
2. **Application:** Crear use case `CrearPedidoUseCase` que valide contra el repositorio de stock antes de persistir.
3. **Infra:** El controller de NestJS debe capturar esta excepción de dominio y retornar un HTTP 400 Bad Request.
```

### B. Historias de Usuario Regeneradas
La IA debe tomar la funcionalidad monolítica de GX y dividirla en **Historias de Usuario modulares**, siguiendo el formato del módulo `gaci-doc-functional.md`.

---

## 4. Integración con GEM (Trazabilidad de Migración)
Si existe un evento o ticket GEM, vincular la documentación y la propuesta técnica a su referencia. Si no existe o no corresponde crear uno, documentar explícitamente esa ausencia y continuar sin inventar una referencia ni crear un ticket artificial.

## 5. Reglas de Estilo para el Puente GeneXus
1. **No Copiar la Mala Estructura:** GeneXus suele generar spaguetis de lógica. La IA tiene prohibido sugerir "Copiar la misma lógica" en un proyecto limpio. Debe reestructurarla.
2. **Identificar Deuda Técnica de GX:** La IA debe anotar explícitamente si la lógica original de GX contenía bugs conocidos o atajos que no deben repetirse (ej. uso excesivo de consultas SQL dinámicas).
3. **Vocabulario del Negocio:** Mantener el vocabulario original de Gaci tal cual aparece en las pantallas de GX para que los desarrolladores funcionales lo reconozcan inmediatamente.
