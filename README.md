📌 Software FJ – Sistema de gestión - detalles finales


Este proyecto empezó con el código base de mi compañero de curso YEYSON JAVIER MARTINEZ MARTINEZ, al que le hice varias mejoras para cumplir con todo lo que pedía el enunciado de la tarea. La lógica de negocio y los precios originales se mantuvieron, solo se agregaron y ajustaron funcionalidades para que el sistema sea más robusto y completo.


¿Qué cambios hay actualmente?

1. Logs más útiles y ordenados
Antes solo se guardaban errores, ahora también se registran eventos importantes (cuando se crea un cliente, una reserva, etc.).

Le puse un formato de fecha más legible (año-mes-día hora:minuto:segundo) y el archivo pasó a llamarse sistema.log.

2. Nueva excepción personalizada
Agregué ServicioNoDisponibleError para manejar casos donde un servicio tenga datos incorrectos (precio negativo, nombre vacío, etc.).

3. Cliente ahora más inteligente
El ID del cliente se genera automáticamente, ya no hay que enviarlo a mano.

Se validan mejor los correos usando expresiones regulares (así evitamos cosas como "usuario@" o "sinformato").

Cuando se crea un cliente, se escribe un mensaje en el log.

4. Servicios con más onda
Cada servicio ahora tiene su propio código único (se incrementa solo).

Agregué el método descripcion() que todos los servicios están obligados a tener, así se puede mostrar una frase bonita de lo que ofrecen.

El método calcular_costo ahora acepta parámetros extra con **kwargs, lo que permite pasar cosas como descuentos, impuestos o la opción "premium" sin tener que tocar toda la fórmula.

5. Ajustes en los servicios concretos (sala, equipo, asesoría)
Reserva de sala: ya no explota si no le mandas las horas; por defecto asigna 1 hora.

Alquiler de equipos: ahora sí multiplica por los días (antes solo por la cantidad).

Asesoría especializada: también tiene horas=1 por defecto para evitar errores.

Todos tienen su propia descripcion().

6. Reserva con confirmar, cancelar y manejo fino de errores
La clase Reserva ahora tiene métodos confirmar() y cancelar(), tal como pedía el enunciado.

Se implementó encadenamiento de excepciones (raise ... from e) para que no se pierda el rastro del error original.

Se agregó un bloque else en el procesamiento, que se ejecuta solo si todo sale bien.

Además, cada reserva tiene su propio ID autoincremental y se registran eventos importantes en el log.

7. Simulación de 10 casos mejorada y sin que se rompa
Los clientes ya no necesitan ID externo, así que simplifiqué la creación.

Envolví la reserva con cliente inválido en un try/except para que el programa no se detenga.

Ajusté la asesoría premium para que sí reciba las horas (antes faltaba).

Puse un ejemplo claro del try/except/else/finally al final de la simulación.

También muestro las descripciones de los servicios usando polimorfismo, que es una forma elegante de demostrar que cada servicio responde diferente a su método descripcion().



¿Qué requisitos del trabajo se cumplen ahora?
Clases abstractas: Entidad y Servicio.

Herencia y polimorfismo: cada servicio hereda y se comporta distinto.

Encapsulación: atributos internos con propiedades y validaciones.

Métodos sobrecargados: usando **kwargs para aceptar distintos parámetros.

Confirmar y cancelar reservas.

Manejo avanzado de excepciones: try/except/else/finally, encadenamiento, excepciones personalizadas.

Registro de todo (eventos y errores) en sistema.log con nivel INFO.

Simulación de 10 operaciones (algunas válidas, otras con errores esperados) y el programa no se cae.

### Cómo ejecutar

```bash
python main.py
