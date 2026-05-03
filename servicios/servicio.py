from abc import ABC, abstractmethod
from modelos.entidad import Entidad

class Servicio(Entidad):
    """Clase abstracta para todos los servicios"""
    
    def __init__(self, nombre, precio_base):
        super().__init__()
        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = True
    
    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):
        """Calcula el costo del servicio (método abstracto)"""
        pass
    
    @abstractmethod
    def describir_servicio(self):
        """Describe el servicio (método abstracto)"""
        pass
    
    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Valida parámetros específicos del servicio"""
        pass
    
    # Métodos sobrecargados para calcular costos
    def calcular_costo_con_impuesto(self, duracion, impuesto=0.19):
        """Calcula costo con impuesto incluido"""
        costo_base = self.calcular_costo(duracion)
        return costo_base * (1 + impuesto)
    
    def calcular_costo_con_descuento(self, duracion, descuento=0.10):
        """Calcula costo con descuento"""
        costo_base = self.calcular_costo(duracion)
        return costo_base * (1 - descuento)
    
    def calcular_costo_personalizado(self, duracion, impuesto=0.19, descuento=0.0):
        """Calcula costo con impuesto y descuento personalizados"""
        costo_base = self.calcular_costo(duracion)
        costo_con_impuesto = costo_base * (1 + impuesto)
        return costo_con_impuesto * (1 - descuento)
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def disponible(self):
        return self._disponible
    
    @disponible.setter
    def disponible(self, valor):
        self._disponible = valor
    
    def mostrar_info(self):
        return f"Servicio: {self._nombre} (Precio base: ${self._precio_base:.2f})"
    
    def validar(self):
        return self._precio_base > 0