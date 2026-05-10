import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime

# CONFIGURACIÓN DE LOGS
# Crea un archivo llamado 'sistema_errores.log' para registrar fallos
# MEJORA: Cambiamos a nivel INFO y agregamos datefmt, también cambiamos el nombre del archivo
logging.basicConfig(
    filename='sistema.log',          # MEJORA: nombre más genérico
    level=logging.INFO,              # MEJORA: ahora registra también eventos exitosos
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'      # MEJORA: formato de fecha limpio
)

# =================================================================
# EXCEPCIONES PERSONALIZADAS
# Implementación de jerarquía de errores para un manejo 
# robusto y específico según la lógica del negocio.
# =================================================================
class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del sistema FJ."""
    pass

class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los datos de entrada (nombres, correos) son erróneos."""
    pass

class ReservaInvalidaError(SoftwareFJError):
    """Se lanza ante fallos específicos en el proceso de reserva."""
    pass

# MEJORA: Agregamos una nueva excepción para servicios no disponibles
class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio tiene parámetros inválidos o no está disponible."""
    pass

# =================================================================
# CLASES BASE Y ABSTRACCIÓN (Pilar POO: Abstracción)
# Uso de clases abstractas para definir contratos obligatorios.
# =================================================================
class Entidad(ABC):
    """Representa una entidad general. Define el contrato base."""
    def __init__(self, id_entidad):
        # Corrección: Uso de __init__ (doble guion bajo) para el constructor
        self.id_entidad = id_entidad

    @abstractmethod
    def mostrar_detalle(self):
        """Método obligatorio que deben implementar las subclases."""
        pass

# MEJORA: Clase Cliente reescrita con autoincremento, validaciones mejoradas y logging
class Cliente(Entidad):
    _contador_id = 1  # MEJORA: generación automática de ID

    def __init__(self, nombre: str, correo: str):  # MEJORA: ya no recibe id_cliente externo
        self._id = Cliente._contador_id
        Cliente._contador_id += 1
        super().__init__(self._id)
        
        # MEJORA: Validación con Expresiones Regulares (Regex)
        # Evita correos mal formados como "usuario@" o "@@.com"
        patron_correo = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if not nombre or not re.match(patron_correo, correo.lower()):
            raise DatosInvalidosError(f"Datos de cliente inválidos: {nombre}, {correo}")
        
        # MEJORA: Atributos protegidos (Convención Pythonic '_')
        self._nombre = nombre  
        self._correo = correo
        logging.info(f"Cliente creado: {self.mostrar_detalle()}")  # MEJORA: registro de evento exitoso

    def mostrar_detalle(self):
        return f"Cliente: {self._nombre} (ID: {self.id_entidad})"

    @property
    def nombre(self):
        """Getter para acceder al nombre cumpliendo el Encapsulamiento."""
        return self._nombre


# =================================================================
# SERVICIOS Y POLIMORFISMO (Pilares POO: Herencia y Polimorfismo)
# Implementación de métodos sobrescritos para cálculos específicos.
# =================================================================
# MEJORA: Clase Servicio mejorada con autoincremento de código y método descripcion()
class Servicio(ABC):
    """Define la estructura base para cualquier servicio del sistema."""
    _contador_codigo = 1000  # MEJORA: código único por servicio

    def __init__(self, nombre_servicio, costo_base):
        self._codigo = Servicio._contador_codigo
        Servicio._contador_codigo += 1
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
        logging.info(f"Servicio creado: {self.nombre_servicio} (Código {self._codigo})")  # MEJORA: log

    @abstractmethod
    def calcular_costo(self, **kwargs):  # MEJORA: ahora acepta parámetros opcionales con **kwargs
        """Método polimórfico para el cálculo de tarifas."""
        pass

    @abstractmethod
    def descripcion(self):  # MEJORA: nuevo método abstracto exigido por el enunciado
        """Retorna una breve descripción del servicio."""
        pass

    # MEJORA: método auxiliar para mostrar resumen
    def mostrar_resumen(self):
        return f"Código {self._codigo}: {self.nombre_servicio} (${self.costo_base:,.0f})"

# MEJORA: Servicios concretos con parámetros por defecto y **kwargs
class ReservaSala(Servicio):
    # CORRECCIÓN: se agregó horas=1 por defecto
    def calcular_costo(self, horas=1, **kwargs):
        if horas <= 0:
            raise DatosInvalidosError("La duración en horas debe ser positiva.")
        return self.costo_base * horas

    # MEJORA: implementación del método descripcion
    def descripcion(self):
        return f"Sala {self.nombre_servicio}: ${self.costo_base:,.0f} por hora"

class AlquilerEquipo(Servicio):
    # CORRECCIÓN: se agregó 'dias' y valores por defecto
    def calcular_costo(self, cantidad=1, dias=1, **kwargs):
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad de equipos debe ser mayor a cero.")
        if dias <= 0:
            raise DatosInvalidosError("Los días deben ser positivos.")
        # CORRECCIÓN: multiplicar también por días
        return self.costo_base * cantidad * dias

    def descripcion(self):
        return f"Equipo {self.nombre_servicio}: ${self.costo_base:,.0f} por unidad al día"

class AsesoriaEspecializada(Servicio):
    # CORRECCIÓN: se agregó horas=1 por defecto
    def calcular_costo(self, horas=1, es_premium=False, **kwargs):
        if horas <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser positivas.")
        iva = 1.19
        total = (self.costo_base * horas) * iva
        if es_premium:
            total += 50000
        return total

    def descripcion(self):
        return f"Asesoría {self.nombre_servicio}: ${self.costo_base:,.0f}/hora + IVA (19%)"

# =================================================================
# GESTIÓN DE RESERVAS (Mejora: Inyección de Dependencias)
# =================================================================
# MEJORA: Reserva ahora con confirmar, cancelar, encadenamiento de excepciones y logging de eventos
class Reserva:
    """Clase que integra Cliente y Servicio de forma flexible."""
    
    _contador_reserva = 1  # MEJORA: autoincremento de ID de reserva

    def __init__(self, cliente: Cliente, servicio: Servicio, **configuracion_servicio):
        self._id = Reserva._contador_reserva
        Reserva._contador_reserva += 1
        self.cliente = cliente
        self.servicio = servicio
        self.configuracion = configuracion_servicio
        self.estado = "Pendiente"
        
        # MEJORA: validaciones en el constructor
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("No se puede procesar una reserva sin un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio proporcionado no es válido.")
        
        logging.info(f"Reserva #{self._id} creada para {cliente.nombre}")

    # MEJORA: método confirmar (exigido por el enunciado)
    def confirmar(self):
        if self.estado == "Cancelada":
            raise ReservaInvalidaError("No se puede confirmar una reserva cancelada.")
        self.estado = "Confirmada"
        logging.info(f"Reserva #{self._id} confirmada.")

    # MEJORA: método cancelar (exigido por el enunciado)
    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaInvalidaError("La reserva ya está cancelada.")
        self.estado = "Cancelada"
        logging.info(f"Reserva #{self._id} cancelada.")

    def procesar_reserva(self):
        """Ejecuta la lógica con control de errores por parámetros."""
        try:
            if not self.cliente:
                raise DatosInvalidosError("No se puede procesar sin un cliente válido.")
            
            # Desempaquetado dinámico: pasa los argumentos correctos al servicio
            costo = self.servicio.calcular_costo(**self.configuracion)
            
            # MEJORA: automáticamente confirmamos la reserva al procesarla
            self.confirmar()
            
            # MEJORA: Formato monetario profesional con separador de miles
            print(f"ÉXITO: {self.servicio.nombre_servicio} para {self.cliente.nombre}. Total: ${costo:,.0f}")
            logging.info(f"Reserva #{self._id} procesada - Costo: ${costo:,.0f}")
        
        except (DatosInvalidosError, ReservaInvalidaError) as e:
            logging.error(f"Error en proceso de reserva: {e}")
            print(f"ERROR CONTROLADO: {e}")
            self.estado = "Fallida"
        
        except Exception as e:
            # MEJORA: Encadenamiento de excepciones (requerido)
            logging.error(f"Error crítico inesperado: {e}")
            self.estado = "Fallida"
            print("Ha ocurrido un error inesperado en el sistema.")
            raise ReservaInvalidaError("Fallo inesperado en el sistema") from e
        
        else:
            # MEJORA: Bloque else - se ejecuta si no hubo excepción
            print("   Operación completada sin errores.")
        
        finally:
            fecha = datetime.now().strftime("%H:%M:%S")
            print(f"Resultado: {self.estado} | Registro: {fecha}\n")

# =================================================================
# SIMULACIÓN DE OPERACIONES (10 Casos de Prueba)
# Demostración de robustez y registro de logs ante datos diversos.
# =================================================================
def iniciar_simulacion():
    print("=== SOFTWARE FJ - SISTEMA DE GESTIÓN PROFESIONAL ===\n")
    
    # 1. Definición de Catálogo de Servicios
    sala_vip = ReservaSala("Sala de Juntas VIP", 80000)
    laptops = AlquilerEquipo("Pack Laptops", 50000)
    consultoria = AsesoriaEspecializada("Consultoría IT", 150000)

    # 2. Creación de clientes (Casos 1, 2 y 3)
    try:
        # MEJORA: ahora no se pasa id_cliente (se genera automáticamente)
        c1 = Cliente("Yeyson Martínez", "yeyson@correo.com")
        c2 = Cliente("Ana Luz", "ana@correo.com")
        
        # Caso de ERROR: Cliente con correo inválido (Detección por Regex)
        print("--- Prueba Seguridad: Validación Regex ---")
        c_error = Cliente("Error User", "correo_falso")  # Esto lanza excepción
    except DatosInvalidosError as e:
        logging.error(f"Fallo en validación de seguridad: {e}")
        print(f"Resultado esperado (ERROR CONTROLADO): {e}\n")
        c_error = None

    # --- SIMULACIÓN DE LOS 10 CASOS ---
    
    # Caso 1: Reserva de sala exitosa
    Reserva(c1, sala_vip, horas=3).procesar_reserva()

    # Caso 2: Alquiler de equipos exitoso
    Reserva(c2, laptops, cantidad=2, dias=5).procesar_reserva()

    # Caso 3: Asesoría premium con horas especificadas
    Reserva(c1, consultoria, horas=2, es_premium=True).procesar_reserva()

    # Caso 4: Intento de reserva con cliente inválido (c_error = None)
    try:
        Reserva(c_error, sala_vip, horas=2).procesar_reserva()
    except ReservaInvalidaError as e:
        logging.error(f"Error esperado en reserva con cliente nulo: {e}")
        print(f"ERROR CONTROLADO (cliente inválido): {e}\n")

    # Caso 5: Horas negativas en sala
    Reserva(c2, sala_vip, horas=-5).procesar_reserva()

    # Caso 6: Cantidad cero en equipos
    Reserva(c1, laptops, cantidad=0, dias=1).procesar_reserva()

    # Caso 7: Sala por tiempo prolongado (12 horas)
    Reserva(c2, sala_vip, horas=12).procesar_reserva()

    # Caso 8: Alquiler masivo de equipos
    Reserva(c1, laptops, cantidad=10, dias=3).procesar_reserva()

    # Caso 9: Asesoría estándar (sin premium)
    Reserva(c2, consultoria, horas=5, es_premium=False).procesar_reserva()

    # Caso 10: Parámetro incorrecto (minutos en lugar de horas)
    print("--- Prueba Robustez: Parámetros incorrectos ---")
    Reserva(c1, sala_vip, minutos=30).procesar_reserva()

    # Demostración extra de try/except/else
    print("\n--- Demostración de try/except/else ---")
    try:
        test = Reserva(c1, sala_vip, horas=1)
        test.procesar_reserva()
    except Exception:
        print("Excepción capturada")
    else:
        print("El bloque else se ejecuta porque no hubo error.")
    finally:
        print("Bloque finally siempre se ejecuta.\n")

    # Mostrar descripciones de servicios (polimorfismo)
    print("--- Descripciones de servicios ---")
    for s in [sala_vip, laptops, consultoria]:
        print(s.descripcion())

    print("\n=== FIN SIMULACIÓN ===")
    print("Revise 'sistema.log' para detalles de eventos y errores.")

if __name__ == "__main__":
    iniciar_simulacion()