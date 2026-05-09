import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

# CONFIGURACIÓN DE LOGS
# Crea un archivo llamado 'sistema_errores.log' para registrar fallos
logging.basicConfig(
    filename='sistema_errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
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

class Cliente(Entidad):
    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)
        
        # MEJORA: Validación con Expresiones Regulares (Regex)
        # Evita correos mal formados como "usuario@" o "@@.com"
        patron_correo = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if not nombre or not re.match(patron_correo, correo.lower()):
            raise DatosInvalidosError(f"Datos de cliente inválidos: {nombre}, {correo}")
        
        # MEJORA: Atributos protegidos (Convención Pythonic '_')
        # Facilita las pruebas unitarias y sigue el estándar de la industria
        self._nombre = nombre  
        self._correo = correo

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
class Servicio(ABC):
    """Define la estructura base para cualquier servicio del sistema."""
    def __init__(self, nombre_servicio, costo_base):
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, unidad):
        """Método polimórfico para el cálculo de tarifas."""
        pass

class ReservaSala(Servicio):
    def calcular_costo(self, horas, **kwargs): # Agregado **kwargs
        if horas <= 0:
            raise DatosInvalidosError("La duración en horas debe ser positiva.")
        return self.costo_base * horas

class AlquilerEquipo(Servicio):
    def calcular_costo(self, cantidad, **kwargs): # Cambiado a 'cantidad' y **kwargs
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad de equipos debe ser mayor a cero.")
        # Si pasas 'dias' en la simulación, puedes usarlo aquí o ignorarlo con **kwargs
        return self.costo_base * cantidad

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, horas, es_premium=False, **kwargs): # Agregado es_premium y **kwargs
        if horas <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser positivas.")
        iva = 1.19
        total = (self.costo_base * horas) * iva
        if es_premium:
            total += 50000
        return total

# =================================================================
# GESTIÓN DE RESERVAS (Mejora: Inyección de Dependencias)
# =================================================================
class Reserva:
    """Clase que integra Cliente y Servicio de forma flexible."""
    
    # MEJORA: Uso de **configuracion_servicio (**kwargs)
    # POR QUÉ: Permite que la Reserva funcione con cualquier servicio
    # sin importar si pide 'horas', 'cantidad' o 'es_premium'.
    def __init__(self, cliente: Cliente, servicio: Servicio, **configuracion_servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.configuracion = configuracion_servicio
        self.estado = "Pendiente"

    def procesar_reserva(self):
        """Ejecuta la lógica con control de errores por parámetros."""
        try:
            if not self.cliente:
                raise DatosInvalidosError("No se puede procesar sin un cliente válido.")
            
            # MEJORA: Desempaquetado dinámico
            # Pasa automáticamente los argumentos correctos al servicio.
            costo = self.servicio.calcular_costo(**self.configuracion)
            
            self.estado = "Confirmada"
            # MEJORA: Formato monetario profesional con separador de miles
            print(f"ÉXITO: {self.servicio.nombre_servicio} para {self.cliente.nombre}. Total: ${costo:,.0f}")
        
        except TypeError as e:
            # MEJORA: Captura de errores si faltan o sobran parámetros
            logging.error(f"Error de parámetros en {self.servicio.nombre_servicio}: {e}")
            print(f"ERROR: Los datos proporcionados no coinciden con el tipo de servicio.")
            self.estado = "Fallida"
        
        except Exception as e:
            logging.error(f"Error crítico inesperado: {e}")
            self.estado = "Fallida"
            print("Ha ocurrido un error inesperado en el sistema.")

        
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
        c1 = Cliente("001", "Yeyson Martínez", "yeyson@correo.com")
        c2 = Cliente("002", "Ana Luz", "ana@correo.com")
        
        # Caso de ERROR: Cliente con correo inválido (Detección por Regex)
        print("--- Prueba Seguridad: Validación Regex ---")
        c_error = Cliente("003", "Error User", "correo_falso")
    except DatosInvalidosError as e:
        logging.error(f"Fallo en validación de seguridad: {e}")
        print(f"Resultado esperado (ERROR CONTROLADO): {e}\n")
        c_error = None

    # --- SIMULACIÓN DE LOS 10 CASOS ---
    
    # Caso 1: Reserva de sala exitosa (Uso de horas)
    Reserva(c1, sala_vip, horas=3).procesar_reserva()

    # Caso 2: Alquiler de equipos exitoso (Uso de cantidad y días)
    Reserva(c2, laptops, cantidad=2, dias=5).procesar_reserva()

    # Caso 3: Asesoría especializada con IVA exitosa (Uso de es_premium)
    Reserva(c1, consultoria, es_premium=True).procesar_reserva()

    # Caso 4: Intento de reserva con cliente inválido (Captura None)
    Reserva(c_error, sala_vip, horas=2).procesar_reserva()

    # Caso 5: Error por horas negativas en sala (Validación de lógica)
    Reserva(c2, sala_vip, horas=-5).procesar_reserva()

    # Caso 6: Error por cantidad cero en equipos
    Reserva(c1, laptops, cantidad=0, dias=1).procesar_reserva()

    # Caso 7: Reserva de sala por tiempo prolongado
    Reserva(c2, sala_vip, horas=12).procesar_reserva()

    # Caso 8: Alquiler masivo de equipos
    Reserva(c1, laptops, cantidad=10).procesar_reserva()

    # Caso 9: Asesoría estándar (No premium)
    # Agregamos 'horas=5' para que el cálculo sea correcto
    Reserva(c2, consultoria, horas=5, es_premium=False).procesar_reserva()

    # Caso 10: Prueba de parámetros incorrectos (Dispara TypeError y Log)
    print("--- Prueba Robustez: Parámetros incorrectos ---")
    Reserva(c1, sala_vip, minutos=30).procesar_reserva()

if __name__ == "__main__":
    iniciar_simulacion()
