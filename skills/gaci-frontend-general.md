# Frontend General — Gaci

## Propósito
Establecer principios comunes de arquitectura frontend para React, Angular y otros clientes de Gaci.

## Cuándo usar
Activar al diseñar o revisar componentes, estado, integraciones HTTP, modelos de datos o estructura de una aplicación frontend.

## Entradas esperadas
Framework, flujo de usuario, contratos de API, estados de UI, estructura del proyecto y configuración de entornos.

## Reglas obligatorias
- Separar presentación, lógica de negocio e infraestructura.
- Modelar requests, responses y estado con tipos estrictos; no usar `any`.
- Mantener flujo unidireccional y una única fuente de verdad.
- Encapsular `fetch`, `axios` u otro cliente HTTP en servicios.
- Toda operación asíncrona debe representar `idle`, `loading`, `success` y `error`.
- Leer URLs de API desde variables de entorno, nunca hardcodearlas.

## Procedimiento
1. Definir modelos y estados del flujo.
2. Ubicar lógica en hooks, servicios o controladores según el framework.
3. Implementar la vista con datos procesados y eventos explícitos.
4. Revisar estados de conectividad y errores.
5. Verificar que no haya estado duplicado ni dependencias de entorno embebidas.

## Salida esperada
Frontend modular, tipado, testeable y desacoplado de APIs y detalles de infraestructura.

## Restricciones
Ningún componente debe instanciar o invocar directamente un cliente HTTP.

## Ejemplos

Este módulo define los principios arquitectónicos generales de desarrollo frontend para proyectos React, Angular y otros clientes.

---

## Referencia de implementación
La interfaz de usuario debe estar completamente divorciada de la lógica de negocio y de los detalles de infraestructura (llamadas directas a APIs, formateo de fechas crudas, cálculos matemáticos, etc.). 
* **Componente (La Capa de Presentación):** Su único propósito es pintar elementos en pantalla (HTML/JSX/Templates) y capturar las interacciones del usuario (clicks, submits). Debe consumir datos ya procesados.
* **Controlador/Servicio (La Capa de Lógica):** Se encarga de coordinar el estado de la UI, reaccionar a eventos, y solicitar datos.

---

## 2. Tipado Estricto de Datos (TypeScript)
No se permite el uso del tipo `any` ni de variables con tipado implícito laxo. Toda comunicación de datos debe estar perfectamente modelada.
* **Modelos de API:** Cada endpoint consumido debe tener definida su interfaz para el Request (entrada) y el Response (salida).
* **Uso de Readonly:** Para evitar mutaciones accidentales del estado, definir propiedades de lectura obligatoria en las interfaces de estado complejo.

### Ejemplo de Modelado de Datos
```typescript
export interface ArticuloResponse {
  readonly id: string;
  readonly codigoArticulo: string;
  readonly descripcion: string;
  readonly precioSugerido: number;
  readonly stockActual: number;
}

export interface ActualizarStockRequest {
  readonly nuevoStock: number;
  readonly motivoAjuste: string;
}
```

---

## 3. Flujo de Datos Unidireccional y Orígenes de Verdad
* El estado debe fluir en una sola dirección: **Acción -> Mutación del Estado -> Renderizado**.
* Se debe evitar la duplicidad del estado. Si un dato puede ser calculado a partir de otro (ej. el total de un carrito a partir del listado de ítems seleccionados), debe ser un "valor derivado" en lugar de un estado independiente.

---

## 4. Gestión de Conectividad e Integración con APIs
* **Abstracción del Cliente HTTP:** Ningún componente puede instanciar o llamar directamente a `fetch` o `axios`. Toda comunicación debe pasar por una clase o módulo de servicio (ej. `ArticuloService`).
* **Estados de Carga y Error:** Toda llamada asíncrona debe contemplar de forma nativa e integrada los estados de:
  - `idle`: Estado inicial de espera.
  - `loading`: Llamada en curso (activar loaders visuales).
  - `success`: Datos recibidos correctamente.
  - `error`: Llamada fallida (captura, parseo de error y exposición amigable).
* **Manejo de Environs:** Las URLs base de las APIs de Gaci (desarrollo, testing, producción) deben leerse obligatoriamente de variables de entorno y nunca estar escritas en duro (hardcoded).
