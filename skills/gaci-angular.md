# Angular — Gaci

## Propósito
Definir cómo diseñar, implementar y revisar componentes, servicios y módulos Angular en Gaci.

## Cuándo usar
Activar para cualquier cambio Angular, especialmente vistas, directivas, servicios, estado reactivo o acceso HTTP.

## Entradas esperadas
Versión de Angular, objetivo funcional, estructura existente, contratos de API y restricciones de UI/estado.

## Reglas obligatorias
- Las nuevas vistas, directivas y componentes deben ser standalone, con `standalone: true` e imports explícitos.
- Preferir `inject()` para dependencias.
- Preferir `toSignal` cuando el componente necesite exponer el estado de un Observable como Signal y combinarlo con estado local.
- Usar `async` para consumos simples directamente en el template cuando no sea necesario transformar ni componer ese estado; una suscripción manual requiere `DestroyRef` y `takeUntilDestroyed`.
- Mantener RxJS para composición de streams, eventos o integraciones complejas donde los Observables sean la abstracción natural.
- Encapsular HTTP en servicios `@Injectable()` y tipar requests/responses.
- No manipular el DOM con JavaScript nativo; usar binding o `@ViewChild`.

## Procedimiento
1. Identificar la responsabilidad de la vista y sus contratos.
2. Crear el componente standalone e importar solo lo necesario.
3. Extraer acceso HTTP y lógica a servicios; modelar tipos.
4. Elegir Signals o RxJS según el flujo y garantizar la liberación de recursos.
5. Revisar estados de carga, error y éxito, y probar el comportamiento.

## Salida esperada
Código Angular modular, tipado, reactivo, sin fugas de memoria y con la lógica de infraestructura fuera de la vista.

## Restricciones
No usar `subscribe()` sin desuscripción garantizada ni llamadas `HttpClient` directas desde componentes.

## Ejemplos

Este módulo define las directrices y estándares de codificación para cualquier componente, servicio o módulo desarrollado en **Angular** dentro de los proyectos de Gaci.

---

## Referencia de implementación
El siguiente ejemplo muestra la aplicación de las reglas de inyección y componentes standalone:

---

## 2. Ejemplo de inyección de dependencias con `inject()`
```typescript
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PedidoService } from '../../../services/pedido.service';

@Component({
  selector: 'app-pedido-detalle',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="pedido(); as ped">
      <h3>Pedido #{{ ped.id }}</h3>
      <p>Total: {{ ped.total }}</p>
    </div>
  `
})
export class PedidoDetalleComponent implements OnInit {
  // Inyección limpia usando inject()
  private readonly pedidoService = inject(PedidoService);
  
  public readonly pedido = this.pedidoService.pedidoSignal;

  ngOnInit(): void {
    this.pedidoService.cargarPedido('12345');
  }
}
```

---

## 3. Ejemplo de suscripción manual segura con RxJS
Cuando la composición de streams o una integración requiera una suscripción manual, asegurar su ciclo de vida con `DestroyRef` y `takeUntilDestroyed`:

```typescript
import { Component, OnInit, inject, DestroyRef } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { LogisticaService } from '../../services/logistica.service';

@Component({...})
export class EnvioComponent implements OnInit {
  private readonly logisticaService = inject(LogisticaService);
  private readonly destroyRef = inject(DestroyRef); // Inyectamos el manejador de destrucción

  ngOnInit(): void {
    this.logisticaService.obtenerEnvios()
      .pipe(takeUntilDestroyed(this.destroyRef)) // Desuscripción automática al destruir el componente
      .subscribe((envios) => {
        console.log('Envíos recibidos:', envios);
      });
  }
}
```

---
