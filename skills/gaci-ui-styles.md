# Estilos y UI — Gaci

## Propósito
Mantener interfaces consistentes, accesibles y responsivas en los proyectos frontend de Gaci.

## Cuándo usar
Activar al diseñar o modificar componentes visuales, layouts, estados de negocio o clases de estilo.

## Entradas esperadas
Framework frontend, diseño o referencia visual, estados de la interfaz, breakpoints y tokens de marca disponibles.

## Reglas obligatorias
- Usar Tailwind CSS como estándar; evitar hojas `.css`/`.scss` salvo bases globales o integraciones complejas.
- Aplicar mobile-first y prefijos responsive (`md:`, `lg:`).
- Respetar colores semánticos: azul primario, slate para superficies/texto, emerald para éxito, amber para alerta y rose para error.
- No usar estilos inline salvo cálculos dinámicos en tiempo real.
- En React, preferir `clsx` o `tailwind-merge` para clases condicionales.
- Verificar contraste, estados interactivos y legibilidad.

## Procedimiento
1. Identificar contenido, estado y jerarquía visual.
2. Construir el layout con utilidades Tailwind desde mobile.
3. Agregar estados de interacción y negocio con clases semánticas.
4. Revisar responsive, accesibilidad y consistencia de marca.

## Salida esperada
Componentes visuales responsivos y consistentes, sin estilos duplicados ni valores de presentación arbitrarios.

## Restricciones
No introducir CSS aislado ni estilos inline por comodidad cuando una utilidad o token existente resuelva el caso.

## Ejemplos

Este módulo define las pautas de diseño visual, estilos, consistencia y maquetación de interfaces para cualquier desarrollo frontend en Gaci.

---

## Referencia de implementación
Para garantizar la consistencia visual, la rapidez de desarrollo y evitar la fragmentación en miles de archivos CSS personalizados que causan colisiones, adoptamos **Tailwind CSS** como el estándar de estilos oficial de Gaci.

* **Regla de oro:** No escribas hojas de estilos CSS independientes (`.css` / `.scss`) a menos que sea para declarar directivas base globales de Tailwind o integrar alguna librería de terceros con estilos complejos. Toda la maquetación debe realizarse usando clases de utilidad de Tailwind en el componente HTML/JSX.

---

## 2. Consistencia Temática (Diseño de Marca Gaci)
Todo componente generado debe hacer uso de las directrices y variables de diseño preestablecidas para mantener un ecosistema visual unificado.

### Colores de Referencia en Tailwind
* **Primarios (Gaci Brand):** Usar `bg-blue-600` / `text-blue-600` para componentes clave como botones principales, barras de navegación o estados seleccionados. Para interacciones: `hover:bg-blue-700`.
* **Secundarios (Fondo y Bordes):** Para fondos limpios usar `bg-slate-50` o `bg-white`. Para textos usar `text-slate-800` (textos principales) y `text-slate-500` (descripciones y textos secundarios).
* **Estados de Negocio (Semántica):**
  - **Éxito (Stock disponible, Pedido completado):** `text-emerald-600` / `bg-emerald-50` / `border-emerald-200`.
  - **Alerta (Stock crítico, Pedido pendiente):** `text-amber-600` / `bg-amber-50` / `border-amber-200`.
  - **Error (Error de API, Cancelado):** `text-rose-600` / `bg-rose-50` / `border-rose-200`.

---

## 3. Ejemplo de Maquetación Reutilizable con Tailwind

### Tarjeta de Información de Artículo (React con Tailwind)
```tsx
import React from 'react';

interface ArticuloCardProps {
  readonly codigo: string;
  readonly descripcion: string;
  readonly stock: number;
  readonly precio: number;
}

export const ArticuloCard: React.FC<ArticuloCardProps> = ({ codigo, descripcion, stock, precio }) => {
  const esStockCritico = stock <= 5;

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{codigo}</span>
        <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${
          esStockCritico 
            ? 'bg-rose-50 text-rose-700 border border-rose-100' 
            : 'bg-emerald-50 text-emerald-700 border border-emerald-100'
        }`}>
          {esStockCritico ? `Stock Crítico: ${stock}` : `Stock: ${stock}`}
        </span>
      </div>
      <h4 className="mt-3 text-lg font-bold text-slate-800">{descripcion}</h4>
      <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3">
        <span className="text-sm text-slate-500">Precio unitario</span>
        <span className="text-base font-extrabold text-blue-600">${precio.toFixed(2)}</span>
      </div>
    </div>
  );
};
```

---

## 4. Reglas de Estilos para IA
1. **PROHIBIDO el uso de estilos inline:** No utilices `style={{ color: 'red' }}` (React) o `style="color: red"` (Angular) en tus componentes. La única excepción es para cálculos dinámicos de tamaño que cambien en tiempo real (ej. el ancho de una barra de progreso que dependa de un estado: `style={{ width: `${progreso}%` }}`).
2. **Uso de Clases Condicionales Inteligentes:** Para manejar clases condicionales en React de forma limpia, utiliza la utilidad `clsx` o `tailwind-merge` (ej. `className={clsx('base-class', esActivo && 'active-class')}`).
3. **Responsive Design Obligatorio:** Todos los componentes generados deben ser responsivos desde el origen (mobile-first). Utiliza prefijos como `md:` o `lg:` para adaptar grillas y espacios en pantallas grandes (ej. `grid grid-cols-1 md:grid-cols-3 gap-4`).
