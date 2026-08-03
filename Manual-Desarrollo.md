# Manual de Desarrollo Estándar — Gaci

Este manual establece las bases arquitectónicas, metodológicas y operativas para el desarrollo de software en Gaci, transitando desde GeneXus hacia un ecosistema estándar, robusto y escalable con asistencia de Inteligencia Artificial.

## Módulos de contexto portables

Los archivos de `skills/` son módulos de contexto portables e independientes del proveedor. Pueden usarse con OpenCode, Claude, Codex u otro asistente capaz de recibir instrucciones o archivos de contexto; no constituyen un formato propietario ni requieren frontmatter específico.

### Uso general

1. Elegir el módulo que corresponda a la tarea.
2. Compartirlo con el asistente junto con el objetivo, archivos relevantes, restricciones y resultado esperado.
3. Aplicar sus reglas y revisar la salida contra el manual y el código real.
4. Combinar módulos cuando la tarea cruce disciplinas, sin asumir que el asistente los cargará automáticamente.

---

## 0. Fase Cero: Descubrimiento de Producto y Documentación de Legacy
Antes de escribir una sola línea de código nuevo, debemos entender a la perfección **QUÉ** queremos construir y **CÓMO** funciona actualmente el sistema antiguo. El éxito de la migración depende de esta fase.

### A. Descubrimiento de Producto
Para proyectos nuevos, no partimos de la tecnología, sino del problema de negocio. Utilizamos el módulo `gaci-product-discovery.md` para realizar una entrevista de producto que defina usuarios, reglas de negocio, flujos de interacción y alcance (MVP) antes de diseñar la arquitectura técnica.

### B. Puente desde GeneXus (Legacy a Moderno)
Los analistas funcionales poseen un valioso conocimiento de las reglas de negocio encapsuladas en el código de GeneXus. Para extraer ese conocimiento y documentarlo de forma moderna, utilizamos el módulo `gaci-gx-bridge.md`. Este módulo permite:
* Analizar transacciones o código de GX para desenterrar reglas de negocio ocultas.
* Mapear pantallas de GX a interfaces modernas.
* Generar especificaciones técnicas para una futura implementación en Arquitectura Hexagonal, preservando la lógica de negocio original pero eliminando deudas técnicas heredadas.

---

## 1. Filosofía de Desarrollo: Fundamentos > Sintaxis

El desarrollo estándar nos devuelve el control total de las aplicaciones, pero también nos exige responsabilidad. Para evitar la deuda técnica y garantizar el éxito de la migración, nos regimos por tres pilares fundamentales:

1. **La lógica de negocio es sagrada:** El código que describe las reglas comerciales de Gaci debe estar completamente desacoplado del framework, de la base de datos y de cualquier librería externa.
2. **La IA es un copiloto, no el piloto:** Usamos asistentes de IA para acelerar la escritura de código, pero todo código generado debe cumplir estrictamente con los contratos de arquitectura y calidad definidos en este manual.
3. **Diseño guiado por contratos:** Definimos interfaces e invariantes antes de escribir implementaciones concretas. Esto facilita la colaboración en equipo y el testeo automatizado.

---

## 2. Arquitectura de referencia para Backend: Hexagonal (Clean Architecture)

> **Alcance de esta guía:** la Arquitectura Hexagonal y las tecnologías descritas en este manual son referencias para proyectos compatibles con ellas. La arquitectura concreta debe decidirse según el contexto del proyecto y el estándar corporativo; no constituye una obligación tecnológica universal.

Para desacoplar el negocio de la tecnología y permitir una evolución continua, esta guía utiliza **Arquitectura Hexagonal** como referencia. Esta estructura divide nuestra aplicación en tres capas concéntricas con una regla de dependencia estricta: *las capas externas dependen de las internas, nunca al revés*.

```
       [ Infraestructura (Adapters) ]
                 |
        [ Aplicación (Use Cases) ]
                 |
             [ Dominio ]
```

### Capa 1: Dominio (Domain)
Es el núcleo de la aplicación. Contiene las entidades de negocio, los objetos de valor (Value Objects) y las reglas de validación puras.
* **Regla de oro:** No puede tener dependencias externas (sin frameworks, sin ORMs, sin decoradores de NestJS). Es código TypeScript puro.
* **Ejemplo:** Entidad `Articulo`, que valida que un precio de lista nunca sea negativo.

### Capa 2: Aplicación (Application / Use Cases)
Orquesta el flujo de datos. Implementa los "Casos de Uso" de la empresa (ej. `CrearPedido`, `SincronizarStockGaciWin`).
* **Puertos (Ports):** Define interfaces para la entrada (Input Ports, ej. comandos de los controladores) y la salida (Output Ports, ej. `IArticuloRepository` para persistencia o `IIAClient` para integración con IA).
* **Dependencias:** Solo depende del Dominio. No sabe si los datos se guardan en SQL Server, PostgreSQL o en un archivo plano.

### Capa 3: Infraestructura (Infrastructure / Adapters)
Contiene las implementaciones tecnológicas concretas que interactúan con el mundo exterior.
* **Adaptadores de Entrada (Primary Adapters):** Controladores REST de NestJS, listeners de colas de mensajería, etc.
* **Adaptadores de Salida (Secondary Adapters):** Repositorios de persistencia que implementan las interfaces de Aplicación (usando TypeORM o Prisma), clientes HTTP que conectan con APIs externas de IA o con los sistemas legados en GeneXus 9 (Gaci Win).

---

## 3. Implementación de Referencia en Backend: NestJS

Cuando el proyecto adopta TypeScript y esta arquitectura, **NestJS** es una implementación de referencia por su robustez empresarial, soporte nativo de TypeScript y arquitectura basada en módulos, la cual encaja perfectamente con los conceptos de la Arquitectura Hexagonal. La elección final queda sujeta a la decisión del proyecto y al estándar corporativo.

### Estructura de Carpetas Recomendada (por Módulo)
Cada módulo funcional (ej. `pedidos`, `articulos`) debe estructurarse de la siguiente manera:

```text
src/
└── modulos/
    └── articulos/
        ├── domain/                  # Capa de Dominio (TypeScript puro)
        │   ├── entities/            # Entidades (ej. articulo.entity.ts)
        │   └── exceptions/          # Excepciones de negocio customizadas
        ├── application/             # Capa de Aplicación (Casos de Uso)
        │   ├── use-cases/           # Casos de uso (ej. crear-articulo.use-case.ts)
        │   └── ports/               # Interfaces / Puertos (ej. articulo.repository.port.ts)
        └── infrastructure/          # Capa de Infraestructura (Adapters)
            ├── controllers/         # Controladores de NestJS (ej. articulo.controller.ts)
            ├── persistence/         # Repositorio concreto (ej. articulo.orm.repository.ts)
            └── dto/                 # Data Transfer Objects para validación de entrada
```

---

## 4. Lineamientos de referencia para Frontend: React y Angular

En proyectos que adopten React o Angular, se recomienda un desarrollo frontend altamente modular, declarativo y centrado en la separación de responsabilidades: **la UI solo debe renderizar, la lógica debe vivir fuera de ella**. La tecnología y los lineamientos concretos quedan sujetos a la decisión del proyecto y al estándar corporativo.

### A. Lineamientos Generales (Comunes a ambos)
1. **Separación de Lógica y UI:** Los componentes visuales deben ser lo más tontos posibles. Toda la lógica de negocio, llamadas a APIs y manejo de estado complejo debe estar encapsulado en Custom Hooks (React) o Servicios (Angular).
2. **Tipado Estricto:** Prohibido el uso de `any`. Cada payload de API y estado local debe estar completamente tipado mediante interfaces.
3. **Manejo de Estado:** En Angular, preferir `toSignal` cuando el componente necesite exponer el estado de un Observable como Signal y combinarlo con estado local. Usar `async` para consumos simples directamente en el template cuando no sea necesario transformar ni componer ese estado. Mantener RxJS para composición de streams, eventos o integraciones complejas donde los Observables sean la abstracción natural.

### B. Especificaciones para React
* **Componentes Funcionales:** Uso exclusivo de componentes funcionales y Hooks.
* **Custom Hooks como Controladores:** Cada vista compleja debe tener su correspondiente hook (ej. `useArticuloList.ts`) que maneje los estados de carga (`loading`), error (`error`) y los datos listados. El componente React solo los consume y renderiza.
* **Estructura de Carpetas:**
  ```text
  src/
  ├── components/       # Componentes atómicos y reutilizables (Botones, Inputs)
  ├── features/         # Módulos de negocio (ej. articulos, ventas)
  │   └── articulos/
  │       ├── components/    # Componentes específicos de la feature
  │       ├── hooks/         # Lógica y llamadas a API (useArticulo.ts)
  │       └── views/         # Páginas o pantallas contenedoras
  └── services/         # Clientes de API compartidos
  ```

### C. Especificaciones para Angular (Consideración de Coexistencia)
* **Componentes Standalone:** Adoptar componentes Standalone para simplificar la modularidad y reducir el boilerplate de `NgModule`.
* **Servicios como Orígenes de Verdad:** Utilizar inyección de dependencias para proveer lógica de negocio y llamadas HTTP a través de servicios dedicados.
  * **Estado y programación reactiva:** Preferir `toSignal` cuando el componente necesite exponer el estado de un Observable como Signal y combinarlo con estado local. Usar `async` para consumos simples directamente en el template cuando no sea necesario transformar ni componer ese estado. Mantener RxJS para composición de streams, eventos o integraciones complejas donde los Observables sean la abstracción natural.

---

## 5. Flujo de Trabajo con Git

Para garantizar la estabilidad de las aplicaciones en producción y permitir que múltiples desarrolladores colaboren de forma organizada, adoptamos un flujo de trabajo estructurado basado en ramas temporales y commits semánticos.

1. **Ramas de Trabajo:** Las features se crean desde `develop`. Los hotfixes se crean desde `main` y, una vez resueltos, se revisan e integran mediante PR hacia `main` y, cuando corresponda, hacia `develop`. Está prohibido commitear directamente a las ramas protegidas `main` o `develop`.
2. **Mensajes de Confirmación Semánticos:** Seguimos el estándar de **Conventional Commits** (`feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`). Esto asegura un historial ordenado y comprensible.
3. **Revisión por Pares (Pull Requests):** Todo código integrado a las ramas protegidas debe pasar por un proceso de Pull Request y ser aprobado por al menos un par técnico antes de fusionarse.

---

## 6. Documentación Técnica y Funcional

Para garantizar el traspaso de conocimiento claro y la trazabilidad de las decisiones de negocio, toda funcionalidad desarrollada debe acompañarse de documentación estructurada:

### A. Documentación Funcional (El QUÉ)
Describe las reglas de negocio, historias de usuario y requisitos de negocio, desacoplados de la implementación técnica. Utilizamos el formato **Historia de Usuario** estándar con criterios de aceptación claros.

### B. Documentación Técnica (El CÓMO)
Describe la arquitectura de las soluciones, modelos de datos y especificaciones de las APIs. Debe apoyarse en diagramas de Mermaid y especificaciones **OpenAPI 3.0**.

---

## 7. Integración con la Plataforma GEM (Trazabilidad y Eventos)
Para asegurar una trazabilidad absoluta entre la definición de negocio y la ejecución técnica, integramos los flujos de trabajo con la plataforma GEM:

1. **Cuando existe un evento o ticket GEM:** La rama `feature/`, los commits relevantes y la documentación funcional y técnica deben vincularse a su ID. Al finalizar, el desarrollador debe publicar en GEM el resumen del cambio con diagramas y referencias a los commits.
2. **Cuando no existe un evento o ticket GEM:** No se debe inventar un identificador. La tarea debe dejar explícita la ausencia de GEM y continuar sin agregar una referencia ficticia.

---

## 8. El uso de Inteligencia Artificial (IA) en el Desarrollo

Para asegurar que el uso de asistentes de IA no degrade la calidad de nuestra base de código, todo desarrollador debe aplicar las siguientes directrices operativas:

1. **Carga de módulos de contexto:** Compartir activamente los siguientes módulos portables en el contexto del asistente según el tipo de tarea:
   - `gaci-git-workflow.md`: Para estructurar ramas, mensajes de commit semánticos y trazabilidad con GEM.
   - `gaci-nestjs-hexagonal.md`: Para la creación de servicios, entidades y puertos en el backend.
   - `gaci-frontend-general.md`: Para los principios generales del frontend de Gaci.
   - `gaci-react.md`: Para componentes, hooks y estado global (Zustand) en proyectos React.
   - `gaci-angular.md`: Para componentes standalone y signals en proyectos Angular.
   - `gaci-ui-styles.md`: Para maquetación responsiva y consistente basada en Tailwind CSS.
    - `gaci-doc-functional.md`: Para generar historias de usuario y reglas de negocio, vinculadas a GEM cuando exista un evento o ticket.
   - `gaci-doc-technical.md`: Para documentación de APIs, diagramas Mermaid y modelos de datos.
   - `gaci-ai-usage.md`: Para auditoría de código generado por IA y reglas éticas del uso de copilotos.
   - `gaci-product-discovery.md`: Para liderar entrevistas de producto y definir alcances (MVP) antes del desarrollo.
    - `gaci-gx-bridge.md`: Para analizar código de GeneXus y generar documentación técnica moderna para migraciones.
2. **Revisión del Código Generado:** Queda terminantemente prohibido integrar código generado por IA sin haber realizado una lectura crítica línea por línea.
3. **Aseguramiento proporcional al riesgo:** Todo código asistido por IA debe validarse según su nivel de riesgo y criticidad. Cuando corresponda, deben ejecutarse pruebas unitarias que demuestren el comportamiento esperado frente a casos borde y entradas inválidas; cuando no corresponda automatizarlas, se debe documentar la evidencia alternativa y la justificación, sin omitir la validación de esos casos.
