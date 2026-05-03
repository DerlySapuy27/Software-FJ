from servicios.servicio import Servicio
from excepciones.errores import ServicioNoDisponibleError, ParametroInvalidoError

class ReservaSala(Servicio):
    """Servicio de reserva de salas"""
    
    def __init__(self, nombre, precio_base):
        super().__init__(nombre, precio_base)
        self._capacidad_maxima = 30
        self._salas_disponibles = ["Sala VIP", "Sala Ejecutiva", "Sala Básica"]
    
    def calcular_costo(self, duracion, **kwargs):
        """Calcula costo de reserva de sala"""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio {self._nombre} no está disponible")
        
        if duracion <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor a 0")
        
        # Costo base por hora + cargo adicional según tipo de sala
        costo_base = self._precio_base * duracion
        
        # Si se especifica capacidad, puede tener costo extra
        if 'capacidad' in kwargs and kwargs['capacidad'] > 20:
            costo_base *= 1.2  # 20% extra para grupos grandes
        
        return costo_base
    
    def describir_servicio(self):
        return f"Reserva de {self._nombre} - Capacidad: {self._capacidad_maxima} personas"
    
    def validar_parametros(self, **kwargs):
        """Valida parámetros específicos para reserva de sala"""
        if 'capacidad' in kwargs:
            if kwargs['capacidad'] > self._capacidad_maxima:
                raise ParametroInvalidoError(
                    f"La capacidad máxima es {self._capacidad_maxima} personas"
                )
        return True
    
    def verificar_disponibilidad(self, fecha=None):
        """Verifica disponibilidad de la sala"""
        # Simulación de verificación
        return self._disponible
    
    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base} - Tipo: Sala - Capacidad: {self._capacidad_maxima}"