from servicios.servicio import Servicio
from excepciones.errores import ServicioNoDisponibleError, ParametroInvalidoError

class Asesoria(Servicio):
    """Servicio de asesorías especializadas"""
    
    NIVELES = ["Básico", "Intermedio", "Avanzado", "Experto"]
    
    def __init__(self, nombre, precio_base, nivel="Básico"):
        super().__init__(nombre, precio_base)
        self._nivel = nivel if nivel in self.NIVELES else "Básico"
        self._consultores_disponibles = 3
    
    def calcular_costo(self, duracion, **kwargs):
        """Calcula costo de asesoría según nivel"""
        if not self._disponible:
            raise ServicioNoDisponibleError("El consultor no está disponible")
        
        if duracion <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor a 0")
        
        # Multiplicador por nivel
        multiplicadores = {
            "Básico": 1.0,
            "Intermedio": 1.3,
            "Avanzado": 1.6,
            "Experto": 2.0
        }
        
        multiplicador = multiplicadores.get(self._nivel, 1.0)
        costo = self._precio_base * duracion * multiplicador
        
        # Costo extra si es urgente
        if kwargs.get('urgente', False):
            costo *= 1.5
        
        return costo
    
    def describir_servicio(self):
        return f"Asesoría {self._nivel}: {self._nombre}"
    
    def validar_parametros(self, **kwargs):
        """Valida parámetros para asesoría"""
        if self._consultores_disponibles <= 0:
            raise ServicioNoDisponibleError("No hay consultores disponibles")
        
        if 'nivel_requerido' in kwargs:
            if kwargs['nivel_requerido'] not in self.NIVELES:
                raise ParametroInvalidoError(
                    f"Nivel no válido. Use: {self.NIVELES}"
                )
        return True
    
    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base} - Nivel: {self._nivel} - Consultores: {self._consultores_disponibles}"