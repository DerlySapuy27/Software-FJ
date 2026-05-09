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
        self._motivo_cancelacion = None  # Nuevo: almacenar motivo
    
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
    
    def cancelar(self, motivo=""):
        """Cancela la reserva con motivo opcional"""
        try:
            if self._estado == "completada":
                raise ReservaError("No se puede cancelar una reserva ya completada")
            
            if self._estado == "cancelada":
                raise ReservaError("La reserva ya está cancelada")
            
            self._estado = "cancelada"
            self._motivo_cancelacion = motivo if motivo else "No especificado"
            return True
            
        except Exception as e:
            raise ReservaError(f"Error al cancelar reserva: {str(e)}")
    
    def modificar(self, nueva_duracion=None, nuevo_servicio=None):
        """
        Modifica la reserva (solo si está pendiente o confirmada)
        Retorna True si se modificó exitosamente
        """
        try:
            # Solo se pueden modificar reservas no completadas ni canceladas
            if self._estado == "completada":
                raise ReservaError("No se puede modificar una reserva ya completada")
            
            if self._estado == "cancelada":
                raise ReservaError("No se puede modificar una reserva cancelada")
            
            modificado = False
            
            # Modificar duración
            if nueva_duracion is not None:
                if nueva_duracion <= 0:
                    raise ReservaError("La duración debe ser mayor a 0")
                self._duracion = nueva_duracion
                modificado = True
            
            # Modificar servicio (solo si está pendiente)
            if nuevo_servicio is not None:
                if self._estado != "pendiente":
                    raise ReservaError("Solo se puede cambiar el servicio en reservas pendientes")
                self._servicio = nuevo_servicio
                modificado = True
            
            # Si se modificó, recalcular costo si estaba confirmada
            if modificado and self._estado == "confirmada":
                self._costo_total = 0  # Resetear costo para recalcular después
                # Opcional: marcar como pendiente para reconfirmar
                self._estado = "pendiente"
            
            return modificado
            
        except Exception as e:
            raise ReservaError(f"Error al modificar reserva: {str(e)}")
    
    def recalcular_costo(self):
        """Recalcula el costo de la reserva (si está confirmada)"""
        if self._estado == "confirmada":
            try:
                costo_base = self._servicio.calcular_costo(self._duracion)
                costo_con_impuesto = self._servicio.calcular_costo_con_impuesto(self._duracion)
                costo_final = self._servicio.calcular_costo_personalizado(
                    self._duracion, impuesto=0.19, descuento=0.05
                )
                self._costo_total = costo_final
                return self._costo_total
            except Exception:
                raise ReservaError("Error al recalcular costo")
        return self._costo_total
    
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
        info = (
            f"Reserva #{self._id_reserva}\n"
            f"  Cliente: {self._cliente.nombre}\n"
            f"  Servicio: {self._servicio.nombre}\n"
            f"  Duración: {self._duracion} horas\n"
            f"  Estado: {self._estado}\n"
            f"  Costo Total: ${self._costo_total:.2f}\n"
            f"  Fecha: {self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        if self._motivo_cancelacion:
            info += f"\n  Motivo cancelación: {self._motivo_cancelacion}"
        return info
    
    @property
    def estado(self):
        return self._estado
    
    @property
    def costo_total(self):
        return self._costo_total
    
    @property
    def duracion(self):
        return self._duracion
    
    @property
    def servicio(self):
        return self._servicio
    
    def __str__(self):
        return f"Reserva {self._id_reserva} - {self._estado}"