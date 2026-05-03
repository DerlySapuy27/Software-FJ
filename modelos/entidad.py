# Importación para crear clases abstractas
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase base de la que heredarán todas las entidades del sistema"""

    def __init__(self, id_entidad=None):
        self._id = id_entidad  # ID único de la entidad (opcional al crear)
        self._estado = "activo"  # Por defecto, toda entidad nueva está activa

    @abstractmethod
    def mostrar_info(self):
        """Obliga a las clases hijas a implementar este método"""
        pass  # No tiene implementación, solo define la interfaz

    @abstractmethod
    def validar(self):
        """Obliga a las clases hijas a tener validación de datos"""
        pass  # Cada entidad definirá sus propias reglas

    @property
    def estado(self):
        """Getter: permite leer el estado como si fuera un atributo normal"""
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado):
        """Setter: controla que solo se asignen estados válidos"""
        estados_validos = ["activo", "inactivo", "suspendido"]
        if nuevo_estado in estados_validos:
            self._estado = nuevo_estado  # Asigna el estado si es válido
        else:
            raise ValueError(
                f"Estado no válido. Use: {estados_validos}"
            )  # Error si no es válido
