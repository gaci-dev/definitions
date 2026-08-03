# React — Gaci

## Propósito
Definir la separación de presentación, lógica y estado para funcionalidades React de Gaci, y establecer las prácticas de rendimiento, tipado y manejo de datos que se validan en code review.

## Cuándo usar
Activar al crear o modificar componentes, hooks, formularios, tablas, servicios HTTP o estado global React.

## Entradas esperadas
Objetivo funcional, contrato de datos, estados de carga/error/vacío, arquitectura de servicios, complejidad del formulario y volumen esperado de registros (define si hace falta paginación server-side o virtualización).

---

## Reglas obligatorias

### Componentes y hooks
- Separar vistas complejas en componente de presentación y Custom Hook controlador.
- El componente recibe datos y eventos; el hook coordina estado y servicios. **Sin llamadas HTTP en la vista.**
- Componentes funcionales con props tipadas de forma explícita. **No usar `React.FC`.**
- Un hook nunca devuelve JSX. Si hay JSX reutilizable, es un componente.
- El hook expone una API estable: funciones en `useCallback`, objetos derivados en `useMemo`.
- No usar componentes de clase.

### Estado
- Estado local (`useState`) por defecto. Escalar a Zustand solo cuando el estado se comparte entre vistas o niveles lejanos del árbol.
- **Zustand** para estado global, siempre mediante **selectores atómicos**. Prohibido desestructurar el store completo.
- Para varios campos del store en un mismo componente, usar `useShallow`.
- **No guardar respuestas de API en el store global.** Los datos de servidor viven en el hook controlador.
- No guardar estado derivable: se calcula en el selector o con `useMemo`.
- Las acciones viven dentro del store. Nunca mutar estado fuera de él.
- No usar Context para estado que cambia seguido (re-renderiza a todos los consumidores). Context solo para valores casi estáticos: tema, i18n, config de sesión.
- Nunca persistir tokens ni datos sensibles con el middleware `persist`.

### Rendimiento y re-renders
- No abusar de `useMemo`/`useCallback`. Justificarlos por rendimiento o referencias estables. Casos donde **sí** son obligatorios:
  - La función/valor se pasa a un componente envuelto en `React.memo`.
  - Es dependencia de un `useEffect` / `useMemo` / `useCallback`.
  - Se retorna desde un custom hook.
  - Cálculos costosos: filtrados, ordenamientos o agrupaciones sobre listas grandes.
  - Definiciones de columnas de TanStack Table (`ColumnDef[]`): **siempre**.
- No crear objetos, arrays ni funciones inline como props de componentes memoizados.
- `key` estable y única. Nunca el índice en listas paginadas, filtradas u ordenables.
- Inputs de filtro y búsqueda: **debounce obligatorio** (300–500 ms) antes de disparar la request.
- Al cambiar un filtro, resetear la paginación **en el handler**, no en un `useEffect` que observa los filtros.
- Medir con el Profiler antes de optimizar. Memoizar "por las dudas" agrega ruido sin beneficio.

### Efectos
- `useEffect` es último recurso. No usarlo para derivar estado ni para reaccionar a eventos del usuario (eso va en el handler).
- Todo efecto que dispara una request **debe cancelarse con `AbortController`** en el cleanup.
- Array de dependencias completo. No silenciar `react-hooks/exhaustive-deps` sin comentario justificando.

### Servicios y datos
- Cliente HTTP centralizado con interceptores de auth y error. El servicio es I/O puro: parámetros tipados, respuesta tipada, soporte de `signal`.
- Errores normalizados a un tipo propio del dominio antes de llegar al hook. El componente nunca ve un `AxiosError` crudo.
- Paginación, orden y filtros **server-side** por defecto en listados grandes.

### Formularios
- Estado controlado en formularios simples (hasta 3 campos, sin validación).
- **React Hook Form + Zod** (`zodResolver`) en formularios complejos.
- El schema Zod es la única fuente de verdad: el tipo se infiere con `z.infer`, no se escribe a mano.
- `Controller` únicamente para componentes de terceros; el resto con `register` para evitar re-render del formulario completo.

### Tipado
- `strict: true`. Prohibido `any`: usar `unknown` + narrowing. Prohibido `@ts-ignore` (usar `@ts-expect-error` con justificación).
- Tipos de dominio únicos: no duplicar la misma interfaz entre feature y service.

---

## Procedimiento
1. Definir props, modelo de datos y estados `data`, `isLoading`, `error`.
2. Implementar el servicio aislado con soporte de cancelación y errores normalizados.
3. Implementar el hook controlador con dependencias completas, cleanup con `AbortController` y API estable.
4. Implementar la vista como presentación pura, contemplando los **cuatro** estados: carga, error, vacío y con datos.
5. Si corresponde, modelar el store global con selectores atómicos y acciones internas.
6. Revisar re-renders con el Profiler y aplicar memoización solo donde haya impacto medible.
7. Probar comportamiento normal, errores, cancelación al desmontar y re-renderizados relevantes.

## Salida esperada
Componentes funcionales, tipados y fáciles de probar, con flujo de datos unidireccional, sin fetches huérfanos ni re-renders innecesarios.

## Restricciones
No acoplar la vista a infraestructura, no duplicar estado derivable, no importar código entre features (lo compartido sube a `components/`, `hooks/` o `lib/`).

---

## Referencia de implementación

### 1. Custom Hook controlador

```typescript
// useArticulo.ts (Controlador de Lógica)
import { useState, useEffect, useCallback, useMemo } from 'react';
import { ArticuloService } from '../services/articulo.service';
import type { Articulo } from '../types';

export const useArticulo = (articuloId: string) => {
  const [articulo, setArticulo] = useState<Articulo | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchArticulo = useCallback(
    async (signal: AbortSignal) => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await ArticuloService.obtenerPorId(articuloId, signal);
        setArticulo(data);
      } catch (err) {
        if ((err as Error).name === 'AbortError') return; // desmontaje: no es un error
        setError((err as Error).message);
      } finally {
        setIsLoading(false);
      }
    },
    [articuloId]
  );

  useEffect(() => {
    const controller = new AbortController();
    void fetchArticulo(controller.signal);
    return () => controller.abort(); // cancelación obligatoria
  }, [fetchArticulo]);

  return useMemo(
    () => ({ articulo, isLoading, error, refetch: fetchArticulo }),
    [articulo, isLoading, error, fetchArticulo]
  );
};
```

### 2. Componente de presentación

```tsx
// ArticuloDetalle.tsx (Vista de Presentación)
import { useArticulo } from '../hooks/useArticulo';

type ArticuloDetalleProps = {
  readonly articuloId: string;
};

export function ArticuloDetalle({ articuloId }: ArticuloDetalleProps) {
  const { articulo, isLoading, error } = useArticulo(articuloId);

  if (isLoading) return <ArticuloSkeleton />;
  if (error) return <ErrorState mensaje={error} />;
  if (!articulo) return <EmptyState mensaje="El artículo no existe." />;

  return (
    <div className="card">
      <h3>{articulo.descripcion}</h3>
      <p>Código: {articulo.codigo}</p>
      <p>Stock: {articulo.stock}</p>
    </div>
  );
}
```

> Sin `React.FC`: las props se tipan directamente en el parámetro. Los cuatro estados (carga, error, vacío, datos) están contemplados de forma explícita.

---

### 3. Gestión de Estado Global con Zustand

Para evitar la complejidad innecesaria de Redux y el acoplamiento/renders masivos de React Context, adoptamos **Zustand** como herramienta oficial para el estado global de cliente.

```typescript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface AuthState {
  usuario: string | null;
  token: string | null;
  login: (usuario: string, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  devtools((set) => ({
    usuario: null,
    token: null,
    login: (usuario, token) => set({ usuario, token }),
    logout: () => set({ usuario: null, token: null }),
  }))
);
```

**Consumo correcto:**

```typescript
// ❌ re-renderiza ante cualquier cambio del store
const { usuario, logout } = useAuthStore();

// ✅ selector atómico: solo re-renderiza si cambia `usuario`
const usuario = useAuthStore((s) => s.usuario);
const logout  = useAuthStore((s) => s.logout);

// ✅ varios campos juntos, sin crear un objeto nuevo en cada render
import { useShallow } from 'zustand/react/shallow';
const { usuario, token } = useAuthStore(
  useShallow((s) => ({ usuario: s.usuario, token: s.token }))
);
```

**Alcance del store:** un store por dominio (`useAuthStore`, `useArticuloFiltrosStore`), nunca un store único global. Los datos que vienen del backend no van acá: viven en el hook controlador de la vista.

---

## Checklist de code review

| ❌ No hacer | ✅ Hacer |
|---|---|
| `React.FC<Props>` | Props tipadas en el parámetro de la función |
| Desestructurar el store completo | Selector atómico / `useShallow` |
| Guardar respuestas de API en Zustand | Manejarlas en el hook controlador |
| `useEffect` para derivar estado | Calcular en render o `useMemo` |
| `useEffect` para resetear paginación al filtrar | Resetear en el handler del filtro |
| Fetch sin cancelar al desmontar | `AbortController` en el cleanup |
| `key={index}` en listas paginadas o filtradas | `key` = id del registro |
| Memoizar todo "por las dudas" | Medir con el Profiler y memoizar donde impacta |
| Un `useState` por campo del formulario | React Hook Form + Zod |
| Fetch dentro del componente | Servicio aislado, orquestado por el hook |
| `any` para salir del paso | `unknown` + narrowing |
| Importar código desde otra feature | Subirlo a `components/`, `hooks/` o `lib/` |
