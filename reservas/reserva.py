from excepciones.errores import ReservaError, ServicioNoDisponibleError
from datetime import datetime

class Reserva:
    """Clase que gestiona las reservas del sistema"""
    
    ESTADOS = ["pendiente", "confirmada", "cancelada", "completada"]
    
    def __init__(self, cliente, servicio, duracion):
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "pendiente"
        self._fecha_creacion = datetime.now()
        self._costo_total = 0
        self._id_reserva = id(self)
    
    def confirmar(self):
        """Confirma la reserva con validaciones"""
        try:
            if self._estado != "pendiente":
                raise ReservaError(f"No se puede confirmar una reserva en estado '{self._estado}'")
            
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError("El servicio solicitado no está disponible")
            
            # Validar parámetros del servicio
            self._servicio.validar_parametros()
            
            self._estado = "confirmada"
            return True
            
        except Exception as e:
            self._estado = "cancelada"
            raise ReservaError(f"Error al confirmar reserva: {str(e)}")
    
    def cancelar(self):
        """Cancela la reserva"""
        try:
            if self._estado == "completada":
                raise ReservaError("No se puede cancelar una reserva ya completada")
            
            self._estado = "cancelada"
            return True
            
        except Exception as e:
            raise ReservaError(f"Error al cancelar reserva: {str(e)}")
    
    def procesar(self):
        """Procesa la reserva y calcula costos"""
        try:
            if self._estado != "confirmada":
                raise ReservaError("Solo se pueden procesar reservas confirmadas")
            
            # Calcular costo con diferentes métodos (sobrecarga)
            try:
                costo_base = self._servicio.calcular_costo(self._duracion)
            except Exception:
                raise ReservaError("Error al calcular costo base")
            
            try:
                costo_con_impuesto = self._servicio.calcular_costo_con_impuesto(self._duracion)
            except Exception:
                costo_con_impuesto = costo_base * 1.19  # Valor por defecto
            
            try:
                costo_final = self._servicio.calcular_costo_personalizado(
                    self._duracion, impuesto=0.19, descuento=0.05
                )
            except Exception:
                costo_final = costo_con_impuesto * 0.95  # 5% descuento por defecto
            
            self._costo_total = costo_final
            self._estado = "completada"
            
            # Agregar al historial del cliente
            self._cliente.agregar_reserva(self)
            
            return self._costo_total
            
        except Exception as e:
            raise ReservaError(f"Error al procesar reserva: {str(e)}")
    
    def mostrar_info(self):
        """Muestra información de la reserva"""
        return (
            f"Reserva #{self._id_reserva}\n"
            f"  Cliente: {self._cliente.nombre}\n"
            f"  Servicio: {self._servicio.nombre}\n"
            f"  Duración: {self._duracion} horas\n"
            f"  Estado: {self._estado}\n"
            f"  Costo Total: ${self._costo_total:.2f}\n"
            f"  Fecha: {self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def costo_total(self):
        return self._costo_total
    
    def __str__(self):
        return f"Reserva {self._id_reserva} - {self._estado}"