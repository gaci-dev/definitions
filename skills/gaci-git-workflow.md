# Flujo de Trabajo en Git — Gaci

## Propósito
Guiar ramas, commits, revisión y publicación de cambios con trazabilidad y calidad.

## Cuándo usar
Activar al crear ramas, sugerir commits, preparar un PR, revisar cambios o resolver un hotfix.

## Entradas esperadas
Tipo de trabajo, ID de GEM si existe, rama base, alcance, pruebas disponibles y archivos afectados.

## Reglas obligatorias
- Proteger `main` y `develop`; no commitear directamente en ellas.
- Crear features desde `develop` con `feature/[gem-id]-[descripcion]` cuando exista un GEM; si no existe, usar `feature/[descripcion]` y dejar explícita la ausencia.
- Crear hotfix desde `main` y revisarlo e integrarlo mediante PR tanto hacia `main` como, cuando corresponda, hacia `develop`, manteniendo ambas ramas protegidas.
- Usar el formato base de Conventional Commits: `tipo(alcance-opcional): descripción`.
- Mantener el identificador GEM como dato separado de trazabilidad. Si las herramientas del repositorio requieren incluirlo en el mensaje, validar con esas herramientas el formato exacto admitido; no tratar una sintaxis específica de GEM como parte del estándar de Conventional Commits.
- No commitear secretos ni `.env`.
- Integrar código mediante PR con pruebas, formato/lint y revisión de al menos un par técnico.

## Procedimiento
1. Confirmar rama base, ID de GEM si existe y alcance.
2. Crear o revisar el nombre de rama.
3. Mantener commits pequeños y semánticos.
4. Ejecutar tests, formatter y lint antes del PR.
5. Revisar secretos, cambios y trazabilidad; solicitar aprobación.

## Salida esperada
Nombre de rama, mensajes de commit y checklist de PR coherentes con el tipo de cambio y con GEM cuando exista.

## Restricciones
No inventar un ID de GEM: si falta, dejarlo explícito y no presentarlo como real.

## Ejemplos

Este módulo define la estrategia de ramificación (branching), convenciones de commits y pautas de publicación mediante Pull Requests para Gaci.

---

## Referencia de implementación
Adoptamos un flujo de trabajo ágil y ordenado basado en ramas temporales para evitar conflictos de código en producción, garantizando la trazabilidad de cambios en la plataforma GEM.

* **Rama `main` (Producción):** Es la rama donde vive el código estable y en producción. Nadie puede realizar commits directamente sobre `main`.
* **Rama `develop` (Desarrollo / Staging):** Aquí se integran todas las nuevas características completadas para su validación previa a producción.
 * **Ramas de Características (`feature/`):** Se crean a partir de `develop` para desarrollar una tarea específica. Cuando existe un evento/ticket GEM, deben incluir su ID; cuando no existe, no se inventa uno y se deja explícita su ausencia.
   - **Convención de nombre:** `feature/[gem-id]-[descripcion-corta]` si existe GEM (ej. `feature/GEM-105-crear-api-cheeky`) o `feature/[descripcion-corta]` si no existe.
 * **Ramas de Hotfix (`hotfix/`):** Se abren directamente desde `main` ante fallos críticos en producción y, una vez resueltas, se revisan e integran mediante PR hacia `main` y, cuando corresponda, hacia `develop`; ambas ramas permanecen protegidas.
  - **Convención de nombre:** `hotfix/[descripcion-corta]` (ej. `hotfix/caida-api-gaci`).

---

## 2. Formato de commits y trazabilidad GEM
Para mantener un historial de cambios profesional y legible, usamos el formato base estándar de **Conventional Commits**. La referencia GEM se gestiona por separado y debe conservarse en la rama, PR, documentación, sistema de trabajo o metadatos de commit según las capacidades del repositorio.

Cada mensaje de commit debe seguir la siguiente estructura:
```text
<tipo>(<alcance-opcional>): <descripcion en minuscula y directo al grano>
```

Cuando el repositorio exija una referencia GEM en el commit, el formato exacto de esa extensión debe validarse con sus hooks, herramientas de CI o documentación local. La ausencia de GEM debe quedar explícita en la trazabilidad del cambio, sin inventar un identificador.

### Tipos de Commit Admitidos
* **`feat`**: Incorporación de una nueva funcionalidad para el usuario (ej. `feat(cheeky): agregar endpoint de sincronizacion`).
* **`fix`**: Corrección de un error o bug en el código (ej. `fix(pedidos): resolver calculo de total con centavos`).
* **`docs`**: Cambios exclusivos en la documentación del proyecto o manuales (ej. `docs(api): actualizar guia de integracion con Gaci Win`).
* **`style`**: Cambios que no afectan la lógica del código, relacionados con estilos o formato visual (ej. `style(ui): aplicar clases de espaciado en la lista de articulos`).
* **`refactor`**: Reestructuración del código existente que no añade funcionalidad nueva ni corrige bugs (ej. `refactor(auth): desacoplar jwt-service de controladores`).
* **`test`**: Añadir o corregir pruebas unitarias, de integración o de extremo a extremo (ej. `test(pedidos): agregar casos borde para crear usecase`).
* **`chore`**: Tareas de mantenimiento, actualización de dependencias o herramientas del entorno de compilación (ej. `chore(deps): actualizar nestjs a ultima version estable`).

---

## 3. Flujo de Pull Request (PR) y Calidad de Código
Cualquier código desarrollado fuera de GeneXus debe integrarse mediante Pull Requests para garantizar la revisión de pares.

1. **Self-Review de Código:** Antes de abrir un PR, el desarrollador (o la IA) debe:
   - Correr las pruebas unitarias y verificar que todas pasen de forma exitosa.
   - Ejecutar el formateador de código (`npm run format` / `npm run lint`) para asegurar el cumplimiento del estándar estético.
2. **Exclusión de Secretos:** Queda estrictamente prohibido cometer archivos `.env` o credenciales de APIs (como claves de IA, tokens de bases de datos, etc.). El archivo `.gitignore` debe estar configurado desde el primer commit para excluir estos datos confidenciales.
3. **Revisión de Pares:** Todo PR requiere la revisión y aprobación de al menos un integrante de la capa de ingeniería antes de fusionarse con la rama protegida de destino. Un hotfix requiere PR hacia `main` y, cuando corresponda, otro PR hacia `develop`.
