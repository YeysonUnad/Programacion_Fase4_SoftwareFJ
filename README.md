# Software FJ - Sistema de Gestión de Clientes, Servicios y Reservas

## Versión mejorada

Este repositorio es una evolución del código base original. Se han implementado una serie de mejoras y correcciones para cumplir completamente con todos los requisitos del enunciado de la tarea, enfatizando la robustez, el manejo avanzado de excepciones y la calidad del código.

### Cambios realizados respecto a la versión anterior

A continuación se describen las principales mejoras incorporadas:

1. **Configuración de logging**  
   - Se cambió el nivel de `ERROR` a `INFO`, permitiendo registrar no solo errores sino también eventos exitosos (creación de clientes, reservas, etc.).  
   - Se añadió `datefmt='%Y-%m-%d %H:%M:%S'` para un formato de fecha más legible.  
   - El archivo de log ahora se llama `sistema.log` (antes `sistema_errores.log`).

2. **Excepciones personalizadas**  
   - Se mantuvieron las excepciones originales (`DatosInvalidosError`, `ReservaInvalidaError`).  
   - Se agregó una nueva excepción `ServicioNoDisponibleError` para manejar errores específicos de los servicios.

3. **Mejora de la clase `Cliente`**  
   - Ahora el ID se genera automáticamente (autoincremental), sin necesidad de pasarlo como parámetro.  
   - Se implementó encapsulación con propiedades (`@property`) y validaciones en los setters (nombre no vacío, email con formato regex).  
   - Se agregó registro de log (`logging.info`) al crear un cliente exitosamente.

4. **Mejora de la clase abstracta `Servicio`**  
   - Se añadió un código único autoincremental para cada servicio (`_contador_codigo`).  
   - Se incorporó el método abstracto `descripcion()` para que cada servicio proporcione una descripción textual.  
   - El método `calcular_costo` ahora acepta parámetros opcionales mediante `**kwargs`, permitiendo sobrecarga (descuentos, impuestos, días, horas, etc.).  
   - Se agregó registro de log al crear un servicio.

5. **Correcciones y enriquecimiento de los servicios concretos**  
   - **`ReservaSalas`**: se añadió valor por defecto `horas=1` para evitar errores cuando no se especifica.  
   - **`AlquilerEquipo`**: ahora el costo considera tanto `cantidad` como `dias` (antes solo cantidad). Se agregaron valores por defecto y validaciones.  
   - **`AsesoriaEspecializada`**: se añadió valor por defecto `horas=1` y el parámetro `es_premium`.  
   - Todos los servicios implementan el método `descripcion()`.

6. **Mejora de la clase `Reserva`**  
   - Se añadió un contador de ID autoincremental para cada reserva.  
   - Se implementaron los métodos `confirmar()` y `cancelar()`, que cambian el estado de la reserva y lanzan excepciones si no es posible.  
   - En `procesar_reserva` se agregó:  
     - Bloque `else` que se ejecuta si no hay excepción.  
     - Encadenamiento de excepciones (`raise ... from e`) para errores inesperados.  
     - Registro de eventos exitosos y errores en el log.  
   - Se ajustó la lógica para que, al procesar una reserva, automáticamente se confirme (se llama a `confirmar()`).

7. **Ajustes en la simulación (`iniciar_simulacion`)**  
   - Se corrigió la creación de clientes (ya no se pasa ID externo).  
   - Se envolvió la reserva con cliente inválido en un `try/except` para que el programa no se detenga.  
   - Se ajustaron los parámetros de los casos de prueba (por ejemplo, añadiendo `dias` en alquileres y `horas` en asesorías).  
   - Se agregó una demostración explícita de `try/except/else/finally` al final para cubrir el requisito.  
   - Se incluyó la impresión de las descripciones de los servicios para evidenciar el polimorfismo.

8. **Corrección de errores y estabilidad general**  
   - Se solucionó un problema donde el caso de cliente inválido generaba una excepción no capturada, deteniendo la ejecución.  
   - Se normalizó el nombre de la función `iniciar_simulacion` (antes se había escrito `iniciar_simulation` en algunos fragmentos).  
   - Se aseguró que todos los bloques `try/except` manejen las excepciones específicas y dejen el sistema en un estado estable.

### Resultado final

El sistema ahora cumple con **todos** los requisitos de la tarea:
- Abstracción, herencia, polimorfismo, encapsulación.
- Manejo avanzado de excepciones (`try/except/else/finally`, excepciones personalizadas, encadenamiento).
- Métodos sobrecargados (uso de `**kwargs`).
- Confirmación y cancelación de reservas.
- Registro de eventos y errores en `sistema.log`.
- Simulación robusta de 10 operaciones (válidas e inválidas) que no se detiene ante errores.

### Cómo ejecutar

```bash
python main.py