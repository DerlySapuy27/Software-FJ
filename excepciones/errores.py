class SistemaFJError(Exception):
    """Clase base para excepciones del sistema"""
    def __init__(self, mensaje="Error en el sistema Software FJ"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ClienteInvalidoError(SistemaFJError):
    """Excepción para errores relacionados con clientes"""
    def __init__(self, mensaje="Datos de cliente inválidos"):
        super().__init__(f"Error de Cliente: {mensaje}")

class ServicioNoDisponibleError(SistemaFJError):
    """Excepción cuando un servicio no está disponible"""
    def __init__(self, mensaje="Servicio no disponible"):
        super().__init__(f"Servicio No Disponible: {mensaje}")

class ParametroInvalidoError(SistemaFJError):
    """Excepción para parámetros inválidos"""
    def __init__(self, mensaje="Parámetro inválido"):
        super().__init__(f"Parámetro Inválido: {mensaje}")

class ReservaError(SistemaFJError):
    """Excepción para errores en reservas"""
    def __init__(self, mensaje="Error en la reserva"):
        super().__init__(f"Error de Reserva: {mensaje}")

class CalculoInvalidoError(SistemaFJError):
    """Excepción para errores en cálculos"""
    def __init__(self, mensaje="Error en cálculo de costo"):
        super().__init__(f"Error de Cálculo: {mensaje}")