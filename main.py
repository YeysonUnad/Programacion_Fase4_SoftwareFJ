import logging
from abc import ABC, abstractmethod
from datetime import datetime

# =================================================================
# CONFIGURACIÓN DE LOGS (Requerimiento de la Fase 4)
# Se encarga de registrar errores en un archivo externo para 
# garantizar la estabilidad y trazabilidad del sistema.
# =================================================================
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
    """Servicio 1: Cálculo basado en horas de uso."""
    def calcular_costo(self, horas):
        if horas <= 0:
            raise DatosInvalidosError("La duración en horas debe ser positiva.")
        return self.costo_base * horas

class AlquilerEquipo(Servicio):
    """Servicio 2: Cálculo basado en cantidad de dispositivos."""
    def calcular_costo(self, cantidad):
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad de equipos debe ser mayor a cero.")
        return self.costo_base * cantidad

class AsesoriaEspecializada(Servicio):
    """Servicio 3: Cálculo con aplicación de impuestos (IVA)."""
    def calcular_costo(self, horas):
        if horas <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser positivas.")
        iva = 1.19
        return (self.costo_base * horas) * iva

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
            logging.error(f"Error crítico: {e}")
            self.estado = "Fallida"
            print("Ha ocurrido un error inesperado en el sistema.")
        
        finally:
            fecha = datetime.now().strftime("%H:%M:%S")
            print(f"Resultado: {self.estado} | Registro: {fecha}\n")


# =================================================================
# SIMULACIÓN DE OPERACIONES (10 Casos de Prueba)
# Demostración de robustez ante datos válidos e inválidos.
# =================================================================
def iniciar_simulacion():
    print("=== SOFTWARE FJ - SISTEMA DE GESTIÓN PROFESIONAL ===\n")
    
    # 1. Definición de Catálogo de Servicios
    sala_vip = ReservaSala("Sala de Juntas VIP", 80000)
    laptops = AlquilerEquipo("Pack Laptops", 50000)
    consultoria = AsesoriaEspecializada("Consultoría IT", 150000)

    # 2. Creación de clientes (Casos 1, 2 y 3)
    try:
        c1 = Cliente("001", "Yeyson Martínez", "yeyson@correo.com") # Válido
        c2 = Cliente("002", "Ana Luz", "ana@correo.com")           # Válido
        # Caso 4: Cliente con datos inválidos (Lanzará excepción)
        c_error = Cliente("003", "", "correo_falso") 
    except DatosInvalidosError as e:
        print(f"CASO 4 (Validación): {e}\n")
        c_error = None

    # Caso 1: Reserva de sala exitosa
    Reserva(c1, sala_vip, 4).procesar_reserva()

    # Caso 2: Alquiler de equipos exitoso
    Reserva(c2, laptops, 3).procesar_reserva()

    # Caso 3: Asesoría especializada con IVA exitosa
    Reserva(c1, consultoria, 2).procesar_reserva()

    # Caso 5: Error por horas negativas en sala
    Reserva(c2, sala_vip, -5).procesar_reserva()

    # Caso 6: Error por cantidad cero en equipos
    Reserva(c1, laptops, 0).procesar_reserva()

    # Caso 7: Intento de reserva con cliente inválido (None)
    Reserva(c_error, sala_vip, 2).procesar_reserva()

    # Caso 8: Reserva de sala por tiempo prolongado
    Reserva(c2, sala_vip, 12).procesar_reserva()

    # Caso 9: Alquiler masivo de equipos
    Reserva(c1, laptops, 20).procesar_reserva()

    # Caso 10: Asesoría de una sola hora
    Reserva(c2, consultoria, 1).procesar_reserva()

if __name__ == "__main__":
    iniciar_simulacion()
