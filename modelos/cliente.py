from modelos.entidad import Entidad
from excepciones.errores import ClienteInvalidoError
import re

class Cliente(Entidad):
    """Cliente del sistema que hereda de Entidad"""
    
    def __init__(self, cedula, nombre, correo):
        super().__init__(id_entidad=cedula)            # Usa la cédula como ID único
        self._cedula = self._validar_cedula(cedula)    # Valida antes de guardar
        self._nombre = self._validar_nombre(nombre)
        self._correo = self._validar_correo(correo)
        self._historial_reservas = []                  # Historial de reservas del cliente
    
    # Solo se definen setters para nombre y correo (la cédula no cambia)
    @property
    def cedula(self):
        return self._cedula
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = self._validar_nombre(nuevo_nombre)  # Revalida al cambiar
    
    @property
    def correo(self):
        return self._correo
    
    @correo.setter
    def correo(self, nuevo_correo):
        self._correo = self._validar_correo(nuevo_correo)
    
    def _validar_cedula(self, cedula):
        """Convierte a entero y verifica que sea positivo y no mayor a 10 dígitos"""
        try:
            cedula_int = int(cedula)
            if cedula_int <= 0 or cedula_int > 9999999999:
                raise ClienteInvalidoError("Cédula inválida")
            return cedula_int
        except ValueError:
            raise ClienteInvalidoError("La cédula debe contener solo números")
    
    def _validar_nombre(self, nombre):
        """Verifica longitud (3-100) y que solo tenga letras y espacios"""
        if not nombre or len(nombre.strip()) < 3 or len(nombre) > 100:
            raise ClienteInvalidoError("Nombre inválido")
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre.strip()):
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios")
        return nombre.strip()
    
    def _validar_correo(self, correo):
        """Verifica formato usuario@dominio.extensión"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, correo):
            raise ClienteInvalidoError("Formato de correo inválido")
        return correo.lower()  # Guarda en minúsculas
    
    def agregar_reserva(self, reserva):
        """Añade una reserva al historial"""
        self._historial_reservas.append(reserva)
    
    def mostrar_info(self):
        """Método requerido por la clase abstracta Entidad"""
        return f"Cliente: {self._nombre} (CC: {self._cedula}, Email: {self._correo})"
    
    def validar(self):
        """Revalida todos los campos, retorna True si todo está correcto"""
        try:
            self._validar_cedula(self._cedula)
            self._validar_nombre(self._nombre)
            self._validar_correo(self._correo)
            return True
        except Exception:
            return False
    
    def __str__(self):
        return self.mostrar_info()