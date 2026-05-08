# Software FJ - Gestión de Reservas (Fase 4)

Este proyecto es un sistema de gestión de reservas modular desarrollado bajo el paradigma de **Programación Orientada a Objetos (POO)**. Se ha refactorizado para cumplir con los requerimientos de la Fase 4, enfocándose en la modularidad y el encapsulamiento.

## 🚀 Mejoras Implementadas (Fase 4)

### 1. Seguridad y Validación (Módulo Cliente)
- **Validación con Regex:** Se incorporó el uso de expresiones regulares (`re.match`) para validar el formato de los correos electrónicos de los clientes.
- **Encapsulamiento:** Se aplicó el pilar de encapsulamiento utilizando atributos protegidos (`_nombre`, `_correo`) y el decorador `@property` para la gestión de datos.

### 2. Flexibilidad en Reservas (Módulo Reserva)
- **Uso de \*\*kwargs:** Se implementó el paso de argumentos variables en la clase `Reserva`. Esto permite que el sistema sea flexible y pueda procesar diferentes tipos de servicios (como salas o asesorías) sin modificar la estructura principal.
- **Manejo de Excepciones:** Se incluyó un bloque `try/except/finally` en el procesamiento de reservas para gestionar errores de parámetros y asegurar el cierre de las operaciones.

## 🛠️ Cómo ejecutar
Ejecuta el archivo principal desde la terminal:
```bash
python main.py
```
