from servicios.servicio import Servicio
from excepciones.errores import ServicioNoDisponibleError, ParametroInvalidoError

class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos"""
    
    def __init__(self, nombre, precio_base, tipo_equipo="General"):
        super().__init__(nombre, precio_base)
        self._tipo_equipo = tipo_equipo
        self._equipos_disponibles = 10
        self._costo_deposito = precio_base * 0.5
    
    def calcular_costo(self, duracion, **kwargs):
        """Calcula costo de alquiler de equipo"""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El equipo {self._nombre} no está disponible")
        
        if duracion <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor a 0")
        
        # Costo base + depósito de seguridad
        costo = self._precio_base * duracion + self._costo_deposito
        
        # Descuento por larga duración
        if duracion > 24:
            costo *= 0.9  # 10% descuento
        
        return costo
    
    def describir_servicio(self):
        return f"Alquiler de {self._nombre} - Tipo: {self._tipo_equipo}"
    
    def validar_parametros(self, **kwargs):
        """Valida parámetros para alquiler de equipo"""
        if self._equipos_disponibles <= 0:
            raise ServicioNoDisponibleError("No hay equipos disponibles")
        
        if 'cantidad' in kwargs and kwargs['cantidad'] > self._equipos_disponibles:
            raise ParametroInvalidoError(
                f"Solo hay {self._equipos_disponibles} equipos disponibles"
            )
        return True
    
    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base} - Equipos disponibles: {self._equipos_disponibles}"