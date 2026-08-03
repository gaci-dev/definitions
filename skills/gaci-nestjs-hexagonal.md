# NestJS + Arquitectura Hexagonal — Gaci

## Propósito
Definir una implementación backend modular y fuertemente tipada, con dominio independiente de NestJS, persistencia y terceros.

## Cuándo usar
Activar al crear, modificar o auditar módulos NestJS, casos de uso, entidades, puertos, controladores o adaptadores.

## Entradas esperadas
Objetivo de negocio, módulo afectado, contratos de entrada/salida, persistencia, integraciones y restricciones existentes.

## Reglas obligatorias
- Separar `domain`, `application` e `infrastructure`; las dependencias apuntan hacia adentro.
- Dominio: TypeScript puro, sin NestJS, ORM ni decoradores externos.
- Aplicación: casos de uso y puertos; recibir dependencias por interfaces.
- Infraestructura: controladores, DTOs, ORM y adaptadores; registrar casos de uso con providers cuando corresponda.
- Los controladores llaman casos de uso, no repositorios.
- Mapear modelos ORM a dominio y exponer DTOs; no retornar modelos de base de datos.
- No usar `any` ni `unknown` sin validar.

## Procedimiento
1. Identificar entidad, invariantes y caso de uso.
2. Definir puertos y contratos en aplicación.
3. Implementar dominio sin dependencias tecnológicas.
4. Implementar adaptadores y composición NestJS en infraestructura.
5. Verificar errores, mapeos, tipado y pruebas.

## Salida esperada
Código organizado por capas, con reglas de negocio testeables y adaptadores reemplazables.

## Restricciones
No filtrar excepciones de negocio manualmente en controladores; delegar en filtros globales.

## Ejemplos

Este módulo define las instrucciones operativas para generar, modificar o auditar código del backend de Gaci utilizando NestJS y Arquitectura Hexagonal.

---

## Referencia de implementación
Todo el código backend debe ser modular, fuertemente tipado en TypeScript y seguir de forma rigurosa la separación de capas de la Arquitectura Hexagonal. El objetivo primordial es que la lógica de negocio (Dominio) sea agnóstica de NestJS, de las bases de datos y de herramientas de terceros.

---

## 2. Reglas de Capas y Dependencias

Al generar código, debes estructurarlo en tres capas bien diferenciadas:

### Capa de Dominio (Domain)
* **Ubicación:** `src/modulos/[modulo]/domain/`
* **Contenido:** Entidades puras de negocio y excepciones customizadas.
* **REGLA ESTRICTA:** Queda terminantemente prohibido importar librerías externas o módulos de NestJS. No uses decoradores como `@Injectable()`, `@Entity()`, `@Column()`, ni decoradores de validación como `@IsString()`. Es TypeScript puro (`.ts`).
* **Ejemplo de Entidad Pura:**
  ```typescript
  // src/modulos/pedidos/domain/entities/pedido.entity.ts
  export class Pedido {
    constructor(
      public readonly id: string,
      public readonly clienteId: string,
      private estado: string,
      private total: number
    ) {}

    public cambiarEstado(nuevoEstado: string): void {
      const estadosValidos = ['pendiente', 'procesado', 'completado', 'cancelado'];
      if (!estadosValidos.includes(nuevoEstado)) {
        throw new Error(`Estado de pedido inválido: ${nuevoEstado}`);
      }
      this.estado = nuevoEstado;
    }

    public obtenerEstado(): string {
      return this.estado;
    }
  }
  ```

### Capa de Aplicación (Application)
* **Ubicación:** `src/modulos/[modulo]/application/`
* **Contenido:** Casos de uso e interfaces de puertos (Ports).
* **Puertos de Salida (Output Ports):** Son interfaces de TypeScript que definen los métodos de acceso a datos u otros servicios externos (ej. `IPedidoRepository`).
* **Casos de Uso (Use Cases):** Clases que implementan la lógica de orquestación. No usan decoradores de NestJS. Reciben las dependencias en su constructor a través de las interfaces de los puertos.
* **Ejemplo de Caso de Uso y Puerto:**
  ```typescript
  // src/modulos/pedidos/application/ports/pedido-repository.port.ts
  import { Pedido } from '../../domain/entities/pedido.entity';

  export interface IPedidoRepository {
    guardar(pedido: Pedido): Promise<void>;
    buscarPorId(id: string): Promise<Pedido | null>;
  }

  // src/modulos/pedidos/application/use-cases/crear-pedido.use-case.ts
  import { Pedido } from '../../domain/entities/pedido.entity';
  import { IPedidoRepository } from '../ports/pedido-repository.port';

  export class CrearPedidoUseCase {
    constructor(private readonly pedidoRepository: IPedidoRepository) {}

    public async ejecutar(id: string, clienteId: string, total: number): Promise<Pedido> {
      const nuevoPedido = new Pedido(id, clienteId, 'pendiente', total);
      await this.pedidoRepository.guardar(nuevoPedido);
      return nuevoPedido;
    }
  }
  ```

### Capa de Infraestructura (Infrastructure)
* **Ubicación:** `src/modulos/[modulo]/infrastructure/`
* **Contenido:** Controladores de NestJS, entidades de ORM (TypeORM/Prisma), adaptadores de persistencia y DTOs de validación.
* **Inyección de Dependencias en NestJS:** Dado que los Casos de Uso son clases puras sin decoradores, debes registrarlos en los módulos de NestJS usando proveedores personalizados (custom providers) para inyectar los adaptadores de infraestructura correspondientes.
* **Ejemplo de Registro en Módulo:**
  ```typescript
  // src/modulos/pedidos/infrastructure/pedidos.module.ts
  import { Module } from '@nestjs/common';
  import { PedidosController } from './controllers/pedidos.controller';
  import { PedidoOrmRepository } from './persistence/pedido-orm.repository';
  import { CrearPedidoUseCase } from '../application/use-cases/crear-pedido.use-case';

  @Module({
    controllers: [PedidosController],
    providers: [
      PedidoOrmRepository,
      {
        provide: CrearPedidoUseCase,
        inject: [PedidoOrmRepository],
        useFactory: (repo: PedidoOrmRepository) => new CrearPedidoUseCase(repo),
      },
    ],
  })
  export class PedidosModule {}
  ```

---

## 3. Lo que la IA TIENE PROHIBIDO hacer en el Backend
1. **PROHIBIDO** acoplar los controladores HTTP de NestJS directamente a los repositorios de bases de datos. Siempre deben llamar a un Caso de Uso.
2. **PROHIBIDO** filtrar excepciones de negocio en el controlador de forma manual. Se debe delegar en filtros de excepción globales de NestJS (Exception Filters).
3. **PROHIBIDO** retornar modelos de base de datos directos (ORM) hacia la UI. Siempre se debe mapear la entidad de ORM a la Entidad de Dominio en el repositorio, y luego exponer DTOs limpios desde los controladores.
4. **PROHIBIDO** usar tipos laxos (`any` o `unknown` sin validar). Todo debe tener interfaces fuertemente tipadas.
