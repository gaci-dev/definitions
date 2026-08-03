# React — Gaci (adaptado: server state con TanStack Query)

> **Qué cambia respecto de la versión original.** El "hook controlador" con `useState` + `useEffect` +
> `AbortController` es una reimplementación a mano de lo que TanStack Query (react-query) ya hace:
> `data` / `isLoading` / `error` / `refetch`, cancelación incluida. Esta versión lo reemplaza y suma
> lo que ese patrón no puede dar solo: cache compartido, deduplicación y una regla clara de
> invalidación. El resto de la skill —tipado, formularios, tablas, efectos, rendimiento— se mantiene,
> con dos reglas nuevas sobre props y granularidad de hooks.

## Propósito

Definir la separación de presentación, lógica y estado para funcionalidades React de Gaci, y
establecer las prácticas de rendimiento, tipado y manejo de datos que se validan en code review.

## Cuándo usar

Activar al crear o modificar componentes, hooks, formularios, tablas, servicios HTTP o estado global React.

## Entradas esperadas

Objetivo funcional, contrato de datos, estados de carga/error/vacío, arquitectura de servicios,
complejidad del formulario y volumen esperado de registros (define si hace falta paginación
server-side o virtualización).

---

## La regla de una línea

> **Lo del servidor va a react-query, lo global se consume adentro, y por props va sólo lo que el
> padre sabe y el hijo no puede averiguar.**

Todo lo demás sale de esto.

---

## Reglas obligatorias

### Dónde vive cada estado

Antes de escribir un `useState`, la pregunta es **de quién es ese dato**. Cuatro respuestas, y la
primera que aplique gana:

| Origen del dato                      | Dónde vive                   | Ejemplo                                           |
| ------------------------------------ | ---------------------------- | ------------------------------------------------- |
| Del servidor                         | **react-query**              | el artículo, el listado, los filtros ya aplicados |
| Compartido entre componentes lejanos | **Zustand**                  | sesión, filtros de una vista, selección múltiple  |
| Una orden que se ejecuta una vez     | **Zustand, pero se consume** | "abrí este artículo y enfocá esta fila"           |
| Sólo de este componente              | **`useState`**               | el texto de un input mientras se escribe          |

- **Nunca copiar la respuesta de una query a un `useState` ni a Zustand.** Es la fuente de los estados que se contradicen: uno se actualiza y el otro no.
- **No guardar estado derivable.** Si sale de otras dos cosas, es un cálculo o un hook derivado, no un campo.

### Datos del servidor (react-query)

- **Toda lectura de la API es un `useQuery`.** Nada de `useEffect` + `useState` para traer datos.
- **La `queryKey` lleva todo lo que cambia la respuesta**: `['articulos', filtros, page]`. Si un
  parámetro no está en la key, dos pedidos distintos comparten entrada y se pisan.
- **`enabled`** para las queries que dependen de algo que todavía no está (un id, la sesión).
- **El servicio sigue siendo I/O puro**: parámetros tipados, respuesta tipada y soporte de `signal`.
  react-query pasa el `signal` en el `queryFn` y cancela solo — no se escribe un `AbortController` a mano.
- **Las mutaciones actualizan el cache, no refetchean**, cuando la respuesta alcanza para saber cómo quedó (`setQueryData`). Se invalida (`invalidateQueries`) sólo cuando el backend recompone algo que el cliente no puede predecir (totales, orden calculado, campos derivados).
- **`onError` con un aviso al usuario en toda mutación que se dispara a mano.** Un fallo silencioso se lee como "no pasó nada" y se vuelve a intentar.
- **Errores normalizados a un tipo del dominio** en el cliente HTTP, antes de llegar al hook. El
  componente nunca ve un `AxiosError` crudo.
- **Paginación, orden y filtros server-side por defecto** en listados grandes. La `queryKey` los
  incluye, así que cambiar de página es una query nueva y la anterior queda cacheada.

### Componentes y hooks

- Separar vistas complejas en componente de presentación y hooks. Sin llamadas HTTP en la vista.
- Componentes funcionales con props tipadas de forma explícita. No usar `React.FC`. No usar clases.
- Un hook nunca devuelve JSX. Si hay JSX reutilizable, es un componente.
- **Lo global se consume adentro.** Un componente que necesita datos los pide con su hook; uno que necesita hacer algo pide la acción. **Por props va sólo lo que el padre sabe y el hijo no puede averiguar**: el id de la fila, una `ref` del DOM, una decisión de layout.
  Llamar el mismo hook desde dos lugares no cuesta nada: react-query devuelve del cache y Zustand del store.
- **Una acción del usuario, un hook**, en `hooks/actions/`, con sus validaciones adentro. No un hook controlador gigante por vista: ese archivo llega a 300 líneas en cuanto la vista tiene veinte
  acciones, y obliga a bajar veinte callbacks por props.
- Los hooks de acción **no guardan estado**. Es lo que los hace seguros de llamar desde dos lugares a la vez.
- **Cuando la acción es un proceso** (un debounce, un temporizador, un listener de `window`), se parte en dos: un **motor** que monta los efectos y lo llama un solo componente, y una **acción** que
  cualquiera llama y sólo escribe el estado que el motor mira. Si no, son dos temporizadores
  compitiendo.

### Estado global (Zustand)

- Zustand para estado de cliente compartido, siempre mediante **selectores atómicos**. Prohibido
  desestructurar el store completo.
- Para varios campos del store en un mismo componente, `useShallow`.
  Excepción: si el selector devuelve una porción **que ya existe en el store** (`s.panels[type]`) y no
  un objeto nuevo armado en el selector, la referencia es estable y `useShallow` no hace falta.
- **Un store por dominio**, nunca uno global único. Varios stores chicos por sección antes que uno
  grande: un store monolítico hace que tocar el cursor re-renderice a quien sólo miraba el buscador.
- **Los stores guardan ESTADO, no COMPORTAMIENTO.** Setters tontos, sin validaciones; las reglas viven
  en los hooks de acción.
- Las acciones que sí van en el store son las que sólo tocan ese estado. Nunca mutar el estado fuera.
- No usar Context para estado que cambia seguido. Context sólo para valores casi estáticos: tema,
  i18n, config de sesión.
- **Nunca persistir tokens ni datos sensibles** con el middleware `persist`. Persistir sólo
  preferencias.
- **Leer el store fuera de React** (`getState()`) sólo cuando el timing lo exige —dentro de una
  promesa, un `setTimeout`, dos handlers seguidos— y con un comentario que diga por qué.

### Efectos

- `useEffect` es último recurso. **Con react-query, la mayoría de los efectos de datos desaparecen.**
- No usarlo para derivar estado ni para reaccionar a eventos del usuario (eso va en el handler).
- Al cambiar un filtro, resetear la paginación **en el handler**, no en un efecto que observa los
  filtros.
- Un debounce se escribe como efecto con cleanup, no como un timer guardado en el estado:
  ```ts
  useEffect(() => {
      const timer = setTimeout(() => setDebounced(texto), 400)
      return () => clearTimeout(timer) // cada cambio cancela el anterior: eso es el debounce
  }, [texto])
  ```
- Array de dependencias completo. No silenciar `react-hooks/exhaustive-deps` sin un comentario que lo justifique.

### Rendimiento y re-renders

- **No memoizar por reflejo.** `useMemo`/`useCallback` se justifican por una razón concreta:
  - El valor se pasa a un componente envuelto en `React.memo`.
  - Es dependencia de un `useEffect` / `useMemo` / `useCallback` (sin memoizar, el efecto corre en
    cada render).
  - Cálculos costosos: filtrados, ordenamientos o agrupaciones sobre listas grandes.
  - Definiciones de columnas de TanStack Table (`ColumnDef[]`): siempre.
- **Memoizar el objeto que devuelve un hook no es automático.** Si quien lo consume lo desestructura
  al toque, memoizar su identidad no evita un solo render. Sirve cuando ese objeto entra en un dep
  array o baja a un componente memoizado.
- ⚠️ **Si el proyecto tiene las reglas del React Compiler en el lint** (`eslint-plugin-react-hooks`
  v7), la memoización manual de más **rompe el lint**: el compiler no la puede preservar y abandona el componente entero. Antes de agregar un `useMemo` "por las dudas", conviene saber si el compiler está activo y si está en el build o sólo en el lint. **Si no está en el build, nadie memoiza por vos y un  padre re-renderiza a todos sus hijos igual.**
- No crear objetos, arrays ni funciones inline como props de componentes memoizados.
- `key` estable y única. **Nunca el índice** en listas paginadas, filtradas u ordenables.
- Inputs de filtro y búsqueda: debounce (300–500 ms) antes de disparar la request.
- Medir con el Profiler antes de optimizar.

### Formularios

- Estado controlado en formularios simples (hasta 3 campos, sin validación).
- React Hook Form + Zod (`zodResolver`) en formularios complejos.
- El schema Zod es la única fuente de verdad: el tipo se infiere con `z.infer`, no se escribe a mano.
- `Controller` únicamente para componentes de terceros; el resto con `register`.
- **El submit es un `useMutation`**, no un `fetch` suelto: así el formulario tiene `isPending` y
  `onError` sin estado propio.

### Tipado

- `strict: true`. Prohibido `any`: usar `unknown` + narrowing. Prohibido `@ts-ignore` (usar
  `@ts-expect-error` con justificación).
- Tipos de dominio únicos: no duplicar la misma interfaz entre feature y service.

### Tests

- Montar el componente real y **falsear sólo la red** (`fetch` o el cliente HTTP). Mockear los hooks
  de datos hace que el test siga pasando cuando se rompe la integración de verdad.
- Qué conviene cubrir, por orden de rédito: lo que no se ve mirando la pantalla (que una ráfaga mande un solo request), lo que depende del timing (debounces, cancelaciones), y lo que tiene varios
  caminos según el contexto.
- **Un test nuevo se verifica rompiendo el código a propósito.** Si no falla, no está probando lo que
  creés.
- Un store global sobrevive al unmount: **resetearlo entre tests**, o uno le deja estado al siguiente
  y el fallo aparece en otro lado.
- Si hay que editar un test existente, algo cambió de comportamiento y hay que discutirlo antes.

---

## Procedimiento

1. Definir props, modelo de datos y los cuatro estados de la vista: carga, error, vacío y con datos.
2. Implementar el servicio aislado: I/O puro, tipado, con soporte de `signal` y errores normalizados.
3. Envolverlo en un `useQuery` con la `queryKey` completa. Las escrituras, en `useMutation` con su actualización de cache.
4. Implementar cada acción del usuario como su propio hook, con las validaciones adentro.
5. Implementar la vista como presentación pura: pide sus datos y sus acciones, no las recibe por
   props.
6. Si hay estado de cliente compartido, modelar el store con selectores atómicos.
7. Revisar re-renders con el Profiler y memoizar sólo donde haya impacto medible.
8. Probar comportamiento normal, errores, cancelación al desmontar y re-renderizados relevantes.

## Salida esperada

Componentes funcionales, tipados y fáciles de probar, con flujo de datos unidireccional, sin fetches duplicados ni re-renders innecesarios, y con una sola fuente de verdad por dato.

## Restricciones

No acoplar la vista a infraestructura, no duplicar estado derivable, no copiar datos del servidor a
otro estado, y no importar código entre features (lo compartido sube a `components/`, `hooks/` o
`lib/`).

---

## Referencia de implementación

### 1. Servicio (I/O puro)

```ts
// articulo.service.ts
import { http } from '@/lib/http' // cliente centralizado: auth, errores normalizados
import type { Articulo } from '../types'

export const ArticuloService = {
    obtenerPorId: (id: string, signal?: AbortSignal) => http.get<Articulo>(`/articulos/${id}`, { signal }),

    actualizar: (id: string, cambios: Partial<Articulo>) => http.patch<Articulo>(`/articulos/${id}`, cambios)
}
```

### 2. Query: leer

```ts
// useArticulo.ts
import { useQuery } from '@tanstack/react-query'
import { ArticuloService } from '../services/articulo.service'
import type { Articulo } from '../types'

export function useArticulo(articuloId: string) {
    return useQuery<Articulo>({
        queryKey: ['articulo', articuloId],
        // El signal lo pasa react-query: la cancelación al desmontar es automática.
        queryFn: ({ signal }) => ArticuloService.obtenerPorId(articuloId, signal),
        enabled: Boolean(articuloId)
    })
}
```

Comparado con el hook controlador manual: sin `useState`, sin `useEffect`, sin `AbortController`, sin `useCallback`, sin `useMemo`. Y además, dos componentes que llamen `useArticulo('7')` hacen **un solo request**.

### 3. Mutación: escribir

```ts
// useActualizarArticulo.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { ArticuloService } from '../services/articulo.service'
import type { Articulo } from '../types'

export function useActualizarArticulo(articuloId: string) {
    const qc = useQueryClient()

    return useMutation({
        mutationFn: (cambios: Partial<Articulo>) => ArticuloService.actualizar(articuloId, cambios),
        // La respuesta alcanza para saber cómo quedó: se escribe el cache, no se refetchea.
        onSuccess: articulo => {
            qc.setQueryData(['articulo', articuloId], articulo)
            // El listado sí se invalida: el backend recalcula orden y totales.
            qc.invalidateQueries({ queryKey: ['articulos'] })
        },
        onError: () => toast.error('No se pudo guardar el artículo')
    })
}
```

### 4. Acción del usuario: un hook, con la regla adentro

```ts
// useArchivarArticulo.ts
export function useArchivarArticulo(articuloId: string) {
    const actualizar = useActualizarArticulo(articuloId)

    return {
        archivar: (articulo: Articulo) => {
            if (articulo.stock > 0) return // la regla vive acá, no en el store ni en la vista
            actualizar.mutate({ archivado: true })
        },
        isPending: actualizar.isPending
    }
}
```

Devuelve un **objeto con la acción nombrada**, no la función pelada: así se le puede agregar un
`isPending` sin tocar a los que ya la usan.

### 5. Componente de presentación

```tsx
// ArticuloDetalle.tsx
import { useArticulo } from '../hooks/useArticulo'
import { useArchivarArticulo } from '../hooks/actions/useArchivarArticulo'

type ArticuloDetalleProps = {
    readonly articuloId: string
}

export function ArticuloDetalle({ articuloId }: ArticuloDetalleProps) {
    const { data: articulo, isLoading, error } = useArticulo(articuloId)
    const { archivar } = useArchivarArticulo(articuloId)

    if (isLoading) return <ArticuloSkeleton />
    if (error) return <ErrorState mensaje={error.message} />
    if (!articulo) return <EmptyState mensaje='El artículo no existe.' />

    return (
        <div className='card'>
            <h3>{articulo.descripcion}</h3>
            <p>Código: {articulo.codigo}</p>
            <p>Stock: {articulo.stock}</p>
            <button onClick={() => archivar(articulo)}>Archivar</button>
        </div>
    )
}
```

Recibe **sólo el `articuloId`**: lo que el padre sabe y el hijo no puede averiguar. Los datos y la
acción se los pide él. Los cuatro estados están contemplados de forma explícita.

### 6. Estado global de cliente con Zustand

Para el estado que **no** viene del servidor: sesión, filtros, selección, preferencias de la vista.

```ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

interface AuthState {
    usuario: string | null
    token: string | null
    login: (usuario: string, token: string) => void
    logout: () => void
}

export const useAuthStore = create<AuthState>()(
    devtools(set => ({
        usuario: null,
        token: null,
        login: (usuario, token) => set({ usuario, token }),
        logout: () => set({ usuario: null, token: null })
    }))
)
```

Consumo correcto:

```ts
// ❌ re-renderiza ante cualquier cambio del store
const { usuario, logout } = useAuthStore()

// ✅ selector atómico: solo re-renderiza si cambia `usuario`
const usuario = useAuthStore(s => s.usuario)
const logout = useAuthStore(s => s.logout)

// ✅ varios campos juntos, sin crear un objeto nuevo en cada render
import { useShallow } from 'zustand/react/shallow'
const { usuario, token } = useAuthStore(useShallow(s => ({ usuario: s.usuario, token: s.token })))
```

**Alcance del store**: uno por dominio (`useAuthStore`, `useArticuloFiltrosStore`), nunca un store
único global. **Los datos que vienen del backend no van acá**: viven en react-query.

---

## Checklist de code review

| ❌ No hacer | ✅ Hacer |
| --- | --- |
| `useState` + `useEffect` para traer datos | `useQuery` |
| `AbortController` a mano en el fetch | El `signal` que pasa `queryFn` |
| Copiar la respuesta de una query a `useState` o Zustand | Leerla del cache donde haga falta |
| `refetch()` después de cada escritura | `setQueryData`, e invalidar sólo lo que recalcula el backend |
| `queryKey` sin los parámetros que cambian la respuesta | La key lleva filtros, página y orden |
| Un hook controlador con las veinte acciones de la vista | Un hook por acción, componibles |
| Bajar datos y callbacks por props | El hijo pide sus datos y sus acciones |
| `React.FC<Props>` | Props tipadas en el parámetro de la función |
| Desestructurar el store completo | Selector atómico / `useShallow` |
| `useEffect` para derivar estado | Calcular en render o `useMemo` |
| `useEffect` para resetear paginación al filtrar | Resetear en el handler del filtro |
| Memoizar el retorno de un hook por reflejo | Memoizar si entra en un dep array o baja a un memo |
| `key={index}` en listas paginadas o filtradas | `key` = id del registro |
| Un `useState` por campo del formulario | React Hook Form + Zod, submit con `useMutation` |
| Fetch dentro del componente | Servicio aislado + `useQuery` |
| `any` para salir del paso | `unknown` + narrowing |
| Importar código desde otra feature | Subirlo a `components/`, `hooks/` o `lib/` |
| Mockear los hooks de datos en los tests | Falsear la red y montar el componente real |
