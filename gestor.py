from modelos.cliente import Cliente
from excepciones.errores import ClienteInvalidoError
from reservas.reserva import Reserva

class GestorSistema:
    def __init__(self):
        self.clientes = []
        self.reservas = []

    def agregar_cliente(self, cedula, nombre, correo):
        # Normalizar a int
        if isinstance(cedula, str):
            if not cedula.isdigit():
                raise ClienteInvalidoError("La cédula solo debe contener números")
            cedula = int(cedula)

        if any(c.cedula == cedula for c in self.clientes):
            raise ClienteInvalidoError("Ya existe un cliente con esa cédula")

        cliente = Cliente(cedula, nombre, correo)
        self.clientes.append(cliente)
        return cliente

    def buscar_cliente(self, cedula):
        if isinstance(cedula, str):
            if not cedula.isdigit():
                raise ClienteInvalidoError("La cédula debe ser numérica")
            cedula = int(cedula)

        for c in self.clientes:
            if c.cedula == cedula:
                return c

        raise ClienteInvalidoError("Cliente no encontrado")

    def crear_reserva(self, cliente, servicio, duracion):
        reserva = Reserva(cliente, servicio, duracion)
        self.reservas.append(reserva)
        return reserva