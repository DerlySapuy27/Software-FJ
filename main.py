from gestor import GestorSistema
from servicios.reserva_sala import ReservaSala
from servicios.alquiler_equipo import AlquilerEquipo
from servicios.asesoria import Asesoria
from logs.logger import configurar_logger, registrar_log
import re

# Configurar logger al inicio
logger = configurar_logger()

# -------- FUNCIONES HELPER (VALIDACIONES) --------


def input_cedula(prompt="Cédula: "):
    """Valida que la cédula sea numérica"""
    while True:
        cedula = input(prompt).strip()
        if cedula.isdigit():
            return cedula
        print("⚠ La cédula solo debe contener números")


def input_texto(prompt="Texto: ", min_len=2, max_len=50):
    """Valida texto solo con letras y espacios"""
    while True:
        valor = input(prompt).strip()
        if len(valor) < min_len or len(valor) > max_len:
            print(f"⚠ Debe tener entre {min_len} y {max_len} caracteres")
            continue
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", valor):
            print("⚠ Solo se permiten letras y espacios")
            continue
        return valor


def input_correo(prompt="Correo: "):
    """Valida formato de correo electrónico"""
    while True:
        valor = input(prompt).strip()
        if re.match(r"^[^@]+@[^@]+\.[^@]+$", valor):
            return valor
        print("⚠ Correo inválido (formato esperado: usuario@dominio.com)")


def input_duracion(prompt="Horas: ", min_val=1, max_val=1000):
    """Valida duración numérica"""
    while True:
        valor = input(prompt).strip()
        if not valor.isdigit():
            print("⚠ La duración debe ser numérica")
            continue
        duracion = int(valor)
        if duracion < min_val or duracion > max_val:
            print(f"⚠ Ingrese un valor entre {min_val} y {max_val}")
            continue
        return duracion


# -------- MENÚS --------


def menu_principal():
    """Menú principal del sistema"""
    print("\n" + "=" * 50)
    print("   SOFTWARE FJ - SISTEMA DE GESTIÓN")
    print("=" * 50)
    print("1. Gestionar Clientes")
    print("2. Realizar Reserva")
    print("3. Gestionar Reservas (Ver/Cancelar/Modificar)")
    print("4. Ver Estadísticas")
    print("5. Simular Operaciones (Demo)")
    print("6. Salir")
    print("=" * 50)


def menu_servicios():
    """Menú para seleccionar tipo de servicio"""
    print("\n--- TIPOS DE SERVICIO ---")
    print("1. Reserva de Sala")
    print("2. Alquiler de Equipo")
    print("3. Asesoría Especializada")
    print("4. Volver")


def simular_operaciones(sistema):
    """Simula 10+ operaciones para demostrar el sistema"""
    registrar_log("Iniciando simulación de operaciones")

    print("\n" + "=" * 50)
    print("   INICIANDO SIMULACIÓN DE 10+ OPERACIONES")
    print("=" * 50)

    servicios_disponibles = [
        ReservaSala("Sala VIP", 100),
        AlquilerEquipo("Laptop HP", 50, "Computación"),
        Asesoria("Consultoría Python", 150, "Avanzado"),
    ]

    # 1. Cliente válido
    try:
        print("\n1. Creando cliente válido (12345, Juan Pérez)...")
        cliente = sistema.agregar_cliente("12345", "Juan Pérez", "juan@email.com")
        print(f"   ✓ ÉXITO: {cliente.mostrar_info()}")
        registrar_log(f"Cliente creado: {cliente.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")
        registrar_log(f"Error: {e}", "error")

    # 2. Cliente válido 2
    try:
        print("\n2. Creando cliente válido (67890, María García)...")
        cliente2 = sistema.agregar_cliente("67890", "María García", "maria@email.com")
        print(f"   ✓ ÉXITO: {cliente2.mostrar_info()}")
        registrar_log(f"Cliente creado: {cliente2.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 3. Cliente con cédula inválida (debe fallar)
    try:
        print("\n3. Intentando crear cliente con cédula inválida (abc)...")
        sistema.agregar_cliente("abc", "Ana López", "ana@email.com")
        print("   ⚠ INESPERADO: Se creó un cliente con datos inválidos")
    except Exception as e:
        print(f"   ✓ ERROR ESPERADO: {e}")
        registrar_log(f"Error esperado: {e}", "info")

    # 4. Cliente con correo inválido (debe fallar)
    try:
        print("\n4. Intentando crear cliente con correo inválido (correo_malo)...")
        sistema.agregar_cliente("11111", "Pedro Ruiz", "correo_malo")
        print("   ⚠ INESPERADO: Se creó un cliente con correo inválido")
    except Exception as e:
        print(f"   ✓ ERROR ESPERADO: {e}")

    # 5. Cliente duplicado (debe fallar)
    try:
        print("\n5. Intentando crear cliente duplicado (12345)...")
        sistema.agregar_cliente("12345", "Juan Copia", "copia@email.com")
        print("   ⚠ INESPERADO: Se creó un cliente duplicado")
    except Exception as e:
        print(f"   ✓ ERROR ESPERADO: {e}")

    # 6. Reserva de sala PENDIENTE (NO confirmada - se deja para modificar después)
    try:
        print("\n6. Creando reserva de sala PENDIENTE (Juan Pérez, Sala VIP, 3h) - PARA MODIFICAR...")
        cliente = sistema.buscar_cliente("12345")
        servicio = servicios_disponibles[0]  # Sala VIP
        reserva = sistema.crear_reserva(cliente, servicio, 3)
        # NO se confirma, se deja como "pendiente" para probar modificación
        print(f"   ✓ ÉXITO: Reserva creada en estado PENDIENTE (Estado: {reserva.estado})")
        registrar_log(f"Reserva pendiente creada: {reserva.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 7. Alquiler de equipo válido (se procesa - completada)
    try:
        print("\n7. Creando alquiler de equipo válido (María García, Laptop, 5h)...")
        cliente2 = sistema.buscar_cliente("67890")
        servicio = servicios_disponibles[1]  # Laptop HP
        reserva = sistema.crear_reserva(cliente2, servicio, 5)
        reserva.confirmar()
        costo = reserva.procesar()
        print(f"   ✓ ÉXITO: Alquiler confirmado y procesado - Costo: ${costo:.2f}")
        registrar_log(f"Alquiler exitoso: {reserva.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 8. Reserva con cliente inexistente (debe fallar)
    try:
        print("\n8. Intentando reservar con cliente inexistente (99999)...")
        cliente = sistema.buscar_cliente("99999")
        servicio = servicios_disponibles[0]
        reserva = sistema.crear_reserva(cliente, servicio, 2)
        print("   ⚠ INESPERADO: Se creó reserva para cliente inexistente")
    except Exception as e:
        print(f"   ✓ ERROR ESPERADO: {e}")

    # 9. Reserva con duración inválida (debe fallar)
    try:
        print("\n9. Intentando reservar con duración negativa (-1h)...")
        cliente = sistema.buscar_cliente("12345")
        servicio = servicios_disponibles[0]
        reserva = sistema.crear_reserva(cliente, servicio, -1)
        reserva.confirmar()
        print("   ⚠ INESPERADO: Se creó reserva con duración inválida")
    except Exception as e:
        print(f"   ✓ ERROR ESPERADO: {e}")

    # 10. Asesoría especializada (se procesa - completada)
    try:
        print("\n10. Creando asesoría especializada (Juan Pérez, Python Avanzado, 4h)...")
        cliente = sistema.buscar_cliente("12345")
        servicio = servicios_disponibles[2]  # Consultoría Python
        reserva = sistema.crear_reserva(cliente, servicio, 4)
        reserva.confirmar()
        costo = reserva.procesar()
        print(f"   ✓ ÉXITO: Asesoría confirmada y procesada - Costo: ${costo:.2f}")
        registrar_log(f"Asesoría exitosa: {reserva.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 11. Reserva CONFIRMADA pero NO procesada (para probar cancelación)
    try:
        print("\n11. Creando reserva CONFIRMADA (María García, Sala VIP, 2h) - PARA CANCELAR...")
        cliente2 = sistema.buscar_cliente("67890")
        servicio = servicios_disponibles[0]  # Sala VIP
        reserva = sistema.crear_reserva(cliente2, servicio, 2)
        reserva.confirmar()
        # NO se procesa, se deja como "confirmada" para probar cancelación
        print(f"   ✓ ÉXITO: Reserva creada y confirmada (Estado: {reserva.estado})")
        registrar_log(f"Reserva confirmada creada: {reserva.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 12. CANCELAR una reserva (la que dejamos confirmada en el paso 11)
    try:
        print("\n12. CANCELANDO la reserva confirmada del paso 11...")
        # Buscar la reserva confirmada que no sea la pendiente
        reserva_a_cancelar = None
        for r in sistema.reservas:
            if r.estado == "confirmada" and r._servicio.nombre == "Sala VIP" and r._cliente.cedula == 67890:
                reserva_a_cancelar = r
                break

        if reserva_a_cancelar:
            print(
                f"    Reserva encontrada: Cliente={reserva_a_cancelar._cliente.nombre}, Estado={reserva_a_cancelar.estado}"
            )
            try:
                resultado = reserva_a_cancelar.cancelar("Cancelación de prueba en simulación")
            except Exception as e:
                print(f"   ✖ Error al cancelar: {e}")
                registrar_log(f"Error cancelando: {e}", "error")
            else:
                print(f"   ✓ ÉXITO: Reserva cancelada correctamente")
                print(f"    Nuevo estado: {reserva_a_cancelar.estado}")
                registrar_log(
                    f"Reserva cancelada en simulación: {reserva_a_cancelar.mostrar_info()}"
                )
            finally:
                print("    [Operación de cancelación finalizada]")
        else:
            print("   ⚠ No se encontraron reservas para cancelar")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")
        registrar_log(f"Error en cancelación: {e}", "error")

    # 13. Intentar cancelar reserva ya COMPLETADA (debe fallar)
    try:
        print("\n13. Intentando cancelar una reserva ya COMPLETADA...")
        reserva_completada = None
        for r in sistema.reservas:
            if r.estado == "completada":
                reserva_completada = r
                break

        if reserva_completada:
            print(f"    Reserva encontrada: Estado={reserva_completada.estado}")
            try:
                reserva_completada.cancelar("Intento de cancelación tardía")
                print("   ⚠ INESPERADO: Se canceló una reserva ya completada")
            except Exception as e:
                print(f"   ✓ ERROR ESPERADO: {e}")
                registrar_log(f"Error esperado al cancelar completada: {e}", "info")
        else:
            print("   ℹ No se encontraron reservas completadas para probar")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 14. Probar modificación de reserva PENDIENTE (la del paso 6)
    try:
        print("\n14. Probando MODIFICACIÓN de la reserva PENDIENTE...")
        reserva_a_modificar = None
        for r in sistema.reservas:
            if r.estado == "pendiente":
                reserva_a_modificar = r
                break
        
        if reserva_a_modificar:
            duracion_original = reserva_a_modificar.duracion
            servicio_original = reserva_a_modificar._servicio.nombre
            print(f"    Reserva encontrada: Estado={reserva_a_modificar.estado}")
            print(f"    Duración original: {duracion_original}h")
            print(f"    Servicio original: {servicio_original}")
            
            try:
                # Modificar duración
                resultado = reserva_a_modificar.modificar(nueva_duracion=duracion_original + 2)
                if resultado:
                    print(f"   ✓ ÉXITO: Duración modificada: {duracion_original} → {reserva_a_modificar.duracion} horas")
                    registrar_log(f"Reserva modificada (duración) en simulación")
            except Exception as e:
                print(f"   ✖ Error al modificar duración: {e}")
            
            # Probar modificación de servicio también
            try:
                nuevo_servicio = servicios_disponibles[1]  # Laptop HP
                print(f"    Intentando cambiar servicio a: {nuevo_servicio.nombre}")
                resultado2 = reserva_a_modificar.modificar(nuevo_servicio=nuevo_servicio)
                if resultado2:
                    print(f"   ✓ ÉXITO: Servicio modificado: {servicio_original} → {nuevo_servicio.nombre}")
                    registrar_log(f"Reserva modificada (servicio) en simulación")
            except Exception as e:
                print(f"   ✖ Error al modificar servicio: {e}")
            
            print("    [Operación de modificación finalizada]")
        else:
            print("   ℹ No se encontraron reservas pendientes para modificar")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 15. Mostrar todos los clientes
    try:
        print("\n15. LISTADO DE CLIENTES REGISTRADOS:")
        print(f"    Total: {len(sistema.clientes)}")
        for i, c in enumerate(sistema.clientes, 1):
            print(f"    {i}. {c.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 16. Mostrar estado final de todas las reservas
    try:
        print("\n16. ESTADO FINAL DE RESERVAS:")
        print(f"    Total: {len(sistema.reservas)}")
        estado_emoji = {
            "pendiente": "⏳",
            "confirmada": "✅",
            "cancelada": "❌",
            "completada": "🎉",
        }
        for i, r in enumerate(sistema.reservas, 1):
            emoji = estado_emoji.get(r.estado, "❓")
            print(
                f"    {emoji} [{i}] {r.estado.upper()} | Cliente: {r._cliente.nombre} | Servicio: {r._servicio.nombre} | Duración: {r.duracion}h | Costo: ${r.costo_total:.2f}"
            )
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    registrar_log("Simulación completada exitosamente")
    print("\n" + "=" * 50)
    print("   ✓ SIMULACIÓN COMPLETADA (16 operaciones)")
    print("   Incluye: creación, validación, reservas, cancelación y modificación")
    print("   NOTA: Queda 1 reserva PENDIENTE para que pueda probar modificación")
    print("   Revise el archivo logs/sistema_*.log")
    print("=" * 50)


def main():
    """Función principal del sistema"""
    sistema = GestorSistema()

    # Crear servicios disponibles
    servicios = {
        "1": ReservaSala("Sala Ejecutiva", 120),
        "2": AlquilerEquipo("Proyector 4K", 80, "Audiovisual"),
        "3": Asesoria("Desarrollo Web", 200, "Intermedio"),
    }

    while True:
        try:
            menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                # Gestionar clientes
                while True:
                    print("\n--- GESTIÓN DE CLIENTES ---")
                    print("1. Agregar cliente")
                    print("2. Buscar cliente")
                    print("3. Listar clientes")
                    print("4. Volver")
                    sub_opcion = input("Opción: ").strip()

                    if sub_opcion == "1":
                        try:
                            print("\n--- NUEVO CLIENTE ---")
                            cedula = input_cedula("Cédula: ")
                            nombre = input_texto("Nombre: ")
                            correo = input_correo("Correo: ")

                            cliente = sistema.agregar_cliente(cedula, nombre, correo)
                            print(f"\n✓ Cliente creado exitosamente:")
                            print(f"  {cliente.mostrar_info()}")
                            registrar_log(f"Cliente creado: {cliente.mostrar_info()}")
                        except Exception as e:
                            print(f"\n✖ Error: {e}")
                            registrar_log(f"Error creando cliente: {e}", "error")

                    elif sub_opcion == "2":
                        try:
                            cedula = input_cedula("Cédula a buscar: ")
                            cliente = sistema.buscar_cliente(cedula)
                            print(f"\n✓ Cliente encontrado:")
                            print(f"  {cliente.mostrar_info()}")
                        except Exception as e:
                            print(f"\n✖ {e}")

                    elif sub_opcion == "3":
                        if not sistema.clientes:
                            print("\n⚠ No hay clientes registrados")
                        else:
                            print(f"\n--- LISTADO DE CLIENTES ---")
                            print(f"Total: {len(sistema.clientes)}")
                            for i, c in enumerate(sistema.clientes, 1):
                                print(f"  {i}. {c.mostrar_info()}")

                    elif sub_opcion == "4":
                        break
                    else:
                        print("Opción no válida")

            elif opcion == "2":
                # Realizar reserva
                if not sistema.clientes:
                    print("\n⚠ Primero debe registrar clientes")
                    continue

                menu_servicios()
                tipo_servicio = input("Seleccione servicio: ").strip()

                if tipo_servicio == "4":
                    continue

                if tipo_servicio not in servicios:
                    print("Opción no válida")
                    continue

                try:
                    # Mostrar clientes disponibles
                    print("\nClientes disponibles:")
                    for i, c in enumerate(sistema.clientes, 1):
                        print(f"  {i}. {c.mostrar_info()}")

                    cedula = input_cedula("\nCédula del cliente: ")
                    cliente = sistema.buscar_cliente(cedula)

                    duracion = input_duracion("Duración (horas): ")

                    servicio = servicios[tipo_servicio]
                    reserva = sistema.crear_reserva(cliente, servicio, duracion)

                    # Preguntar si desea confirmar la reserva o dejarla pendiente
                    print("\n¿Desea confirmar la reserva ahora?")
                    print("1. Sí, confirmar y procesar")
                    print("2. No, dejarla pendiente (podrá modificarla después)")
                    confirmar_opcion = input("Opción: ").strip()
                    
                    if confirmar_opcion == "1":
                        reserva.confirmar()
                        costo = reserva.procesar()
                        print(f"\n✓ Reserva exitosa (COMPLETADA)!")
                    else:
                        print(f"\n✓ Reserva creada en estado PENDIENTE")
                        print("  Puede modificarla o confirmarla más tarde desde Gestión de Reservas")
                    
                    print(reserva.mostrar_info())
                    registrar_log(f"Reserva creada: {reserva.mostrar_info()}")

                except Exception as e:
                    print(f"\n✖ Error en reserva: {e}")
                    registrar_log(f"Error en reserva: {e}", "error")

            # ==================== SECCIÓN MODIFICADA: GESTIÓN DE RESERVAS ====================
            elif opcion == "3":
                # Gestionar Reservas (Ver/Cancelar/Modificar)
                while True:
                    print("\n--- GESTIÓN DE RESERVAS ---")
                    print("1. Ver todas las reservas")
                    print("2. Cancelar una reserva")
                    print("3. Modificar una reserva")
                    print("4. Confirmar una reserva pendiente")
                    print("5. Volver")
                    sub_opcion = input("Opción: ").strip()

                    if sub_opcion == "1":
                        # Ver reservas
                        if not sistema.reservas:
                            print("\n⚠ No hay reservas registradas")
                        else:
                            print(f"\n--- LISTADO DE RESERVAS ---")
                            print(f"Total: {len(sistema.reservas)}")
                            estado_emoji = {
                                "pendiente": "⏳",
                                "confirmada": "✅",
                                "cancelada": "❌",
                                "completada": "🎉",
                            }
                            for i, r in enumerate(sistema.reservas, 1):
                                emoji = estado_emoji.get(r.estado, "❓")
                                print(f"\n  {emoji} [{i}]")
                                print(f"  {r.mostrar_info()}")

                    elif sub_opcion == "2":
                        # Cancelar reserva
                        if not sistema.reservas:
                            print("\n⚠ No hay reservas para cancelar")
                            continue

                        # Mostrar solo reservas que se pueden cancelar
                        reservas_cancelables = [
                            (i, r)
                            for i, r in enumerate(sistema.reservas, 1)  
                            if r.estado in ["pendiente", "confirmada"]
                        ]

                        if not reservas_cancelables:
                            print("\n⚠ No hay reservas que se puedan cancelar")
                            print("  Solo se pueden cancelar reservas 'pendientes' o 'confirmadas'")
                            continue

                        print("\n--- RESERVAS QUE PUEDEN CANCELARSE ---")
                        for idx, r in reservas_cancelables:
                            print(f"\n  [{idx}] {r.mostrar_info()}")

                        try:
                            num_reserva = input(
                                "\nNúmero de reserva a cancelar (0 para volver): "
                            ).strip()

                            if num_reserva == "0":
                                continue

                            if not num_reserva.isdigit():
                                print("⚠ Debe ingresar un número válido")
                                continue

                            num_reserva = int(num_reserva)

                            if num_reserva < 1 or num_reserva > len(sistema.reservas):
                                print("⚠ Número de reserva no válido")
                                continue

                            reserva = sistema.reservas[num_reserva - 1]

                            if reserva.estado not in ["pendiente", "confirmada"]:
                                print(
                                    f"⚠ Esta reserva está en estado '{reserva.estado}' y no se puede cancelar"
                                )
                                print("  Solo se pueden cancelar reservas 'pendientes' o 'confirmadas'")
                                continue

                            print(f"\n¿Está seguro de cancelar esta reserva?")
                            print(reserva.mostrar_info())

                            motivo = input("\nMotivo de cancelación (opcional): ").strip()
                            confirmacion = input("Escriba 'SI' para confirmar cancelación: ").strip().upper()

                            if confirmacion == "SI":
                                try:
                                    resultado = reserva.cancelar(motivo if motivo else "")
                                except Exception as e:
                                    print(f"\n✖ Error al cancelar: {e}")
                                    registrar_log(f"Error cancelando reserva: {e}", "error")
                                else:
                                    print(f"\n✓ Reserva cancelada exitosamente")
                                    print(reserva.mostrar_info())
                                    registrar_log(f"Reserva cancelada: {reserva.mostrar_info()}")
                                finally:
                                    print("Operación de cancelación finalizada")
                            else:
                                print("Cancelación abortada por el usuario")

                        except Exception as e:
                            print(f"✖ Error: {e}")
                            registrar_log(f"Error en cancelación: {e}", "error")

                    # ==================== MODIFICAR RESERVA ====================
                    elif sub_opcion == "3":
                        # MODIFICAR RESERVA
                        if not sistema.reservas:
                            print("\n⚠ No hay reservas para modificar")
                            continue

                        # Mostrar solo reservas que se pueden modificar (pendientes o confirmadas)
                        reservas_modificables = [
                            (i, r)
                            for i, r in enumerate(sistema.reservas, 1)
                            if r.estado in ["pendiente", "confirmada"]
                        ]

                        if not reservas_modificables:
                            print("\n⚠ No hay reservas que se puedan modificar")
                            print("  Solo se pueden modificar reservas 'pendientes' o 'confirmadas'")
                            print("  Puede crear una nueva reserva y dejarla pendiente para modificarla")
                            continue

                        print("\n--- RESERVAS QUE PUEDEN MODIFICARSE ---")
                        for idx, r in reservas_modificables:
                            estado_icon = "⏳" if r.estado == "pendiente" else "✅"
                            print(f"\n  {estado_icon} [{idx}]")
                            print(f"    Cliente: {r._cliente.nombre}")
                            print(f"    Servicio: {r._servicio.nombre}")
                            print(f"    Duración: {r.duracion} horas")
                            print(f"    Estado: {r.estado}")

                        try:
                            num_reserva = input("\nNúmero de reserva a modificar (0 para volver): ").strip()

                            if num_reserva == "0":
                                continue

                            if not num_reserva.isdigit():
                                print("⚠ Debe ingresar un número válido")
                                continue

                            num_reserva = int(num_reserva)

                            if num_reserva < 1 or num_reserva > len(sistema.reservas):
                                print("⚠ Número de reserva no válido")
                                continue

                            reserva = sistema.reservas[num_reserva - 1]

                            if reserva.estado not in ["pendiente", "confirmada"]:
                                print(f"⚠ Esta reserva está en estado '{reserva.estado}' y no se puede modificar")
                                continue

                            print(f"\n--- MODIFICANDO RESERVA #{num_reserva} ---")
                            print("Datos actuales:")
                            print(f"  Estado: {reserva.estado}")
                            print(f"  Duración actual: {reserva.duracion} horas")
                            print(f"  Servicio actual: {reserva._servicio.nombre}")

                            print("\n¿Qué desea modificar?")
                            print("1. Duración")
                            print("2. Tipo de servicio (solo si está PENDIENTE)")
                            print("3. Ambos")
                            print("4. Cancelar modificación")

                            opc_mod = input("Opción: ").strip()

                            if opc_mod == "4":
                                print("Modificación cancelada")
                                continue

                            nueva_duracion = None
                            nuevo_servicio = None

                            # Modificar duración
                            if opc_mod in ["1", "3"]:
                                print(f"\nDuración actual: {reserva.duracion} horas")
                                nueva_duracion = input_duracion("Nueva duración (horas): ")
                                print(f"  ✓ Nueva duración: {nueva_duracion} horas")

                            # Modificar servicio
                            if opc_mod in ["2", "3"]:
                                if reserva.estado != "pendiente":
                                    print("\n⚠ Solo se puede cambiar el servicio en reservas PENDIENTES")
                                    print(f"  Esta reserva está {reserva.estado.upper()}")
                                    if opc_mod == "2":
                                        continue
                                else:
                                    print(f"\nServicio actual: {reserva._servicio.nombre}")
                                    print("\nServicios disponibles:")
                                    for key, serv in servicios.items():
                                        print(f"  {key}. {serv.nombre} (${serv._precio_base}/hora)")

                                    opc_serv = input("Seleccione nuevo servicio (1-3): ").strip()
                                    if opc_serv in servicios:
                                        nuevo_servicio = servicios[opc_serv]
                                        print(f"  ✓ Nuevo servicio: {nuevo_servicio.nombre}")
                                    else:
                                        print("⚠ Opción no válida, se mantendrá el servicio actual")

                            # Confirmar modificación
                            print("\n--- RESUMEN DE MODIFICACIÓN ---")
                            if nueva_duracion:
                                print(f"  Duración: {reserva.duracion} → {nueva_duracion} horas")
                            if nuevo_servicio:
                                print(f"  Servicio: {reserva._servicio.nombre} → {nuevo_servicio.nombre}")

                            confirmacion = input("\n¿Confirmar modificación? (SI/NO): ").strip().upper()

                            if confirmacion == "SI":
                                try:
                                    modificado = reserva.modificar(
                                        nueva_duracion=nueva_duracion,
                                        nuevo_servicio=nuevo_servicio
                                    )
                                except Exception as e:
                                    print(f"\n✖ Error al modificar: {e}")
                                    registrar_log(f"Error modificando reserva: {e}", "error")
                                else:
                                    if modificado:
                                        print(f"\n✓ Reserva modificada exitosamente")
                                        if reserva.estado == "pendiente" and nueva_duracion:
                                            print("  La reserva sigue en estado PENDIENTE")
                                            reconfirmar = input("¿Desea confirmar la reserva ahora? (SI/NO): ").strip().upper()
                                            if reconfirmar == "SI":
                                                try:
                                                    reserva.confirmar()
                                                    print("  ✓ Reserva confirmada")
                                                    procesar = input("¿Desea procesar/completar la reserva? (SI/NO): ").strip().upper()
                                                    if procesar == "SI":
                                                        costo = reserva.procesar()
                                                        print(f"  ✓ Reserva completada - Costo: ${costo:.2f}")
                                                except Exception as e:
                                                    print(f"  ⚠ Error al confirmar: {e}")
                                        elif reserva.estado == "confirmada" and nueva_duracion:
                                            print("  Nota: La reserva estaba confirmada y se ha cambiado a PENDIENTE")
                                            print("  Deberá reconfirmarla para procesarla")
                                        print("\nDatos actualizados:")
                                        print(reserva.mostrar_info())
                                        registrar_log(f"Reserva modificada: {reserva.mostrar_info()}")
                                    else:
                                        print("\n⚠ No se realizaron cambios")
                                finally:
                                    print("Operación de modificación finalizada")
                            else:
                                print("Modificación abortada por el usuario")

                        except Exception as e:
                            print(f"✖ Error: {e}")
                            registrar_log(f"Error en modificación: {e}", "error")

                    # ==================== NUEVO: CONFIRMAR RESERVA PENDIENTE ====================
                    elif sub_opcion == "4":
                        # Confirmar una reserva pendiente
                        if not sistema.reservas:
                            print("\n⚠ No hay reservas registradas")
                            continue

                        reservas_pendientes = [
                            (i, r)
                            for i, r in enumerate(sistema.reservas, 1)
                            if r.estado == "pendiente"
                        ]

                        if not reservas_pendientes:
                            print("\n⚠ No hay reservas en estado PENDIENTE")
                            continue

                        print("\n--- RESERVAS PENDIENTES ---")
                        for idx, r in reservas_pendientes:
                            print(f"\n  [{idx}]")
                            print(f"    Cliente: {r._cliente.nombre}")
                            print(f"    Servicio: {r._servicio.nombre}")
                            print(f"    Duración: {r.duracion} horas")

                        try:
                            num_reserva = input("\nNúmero de reserva a confirmar (0 para volver): ").strip()

                            if num_reserva == "0":
                                continue

                            if not num_reserva.isdigit():
                                print("⚠ Debe ingresar un número válido")
                                continue

                            num_reserva = int(num_reserva)

                            if num_reserva < 1 or num_reserva > len(sistema.reservas):
                                print("⚠ Número de reserva no válido")
                                continue

                            reserva = sistema.reservas[num_reserva - 1]

                            if reserva.estado != "pendiente":
                                print(f"⚠ Esta reserva está en estado '{reserva.estado}', no es pendiente")
                                continue

                            print(f"\nReserva a confirmar:")
                            print(reserva.mostrar_info())

                            confirmacion = input("\n¿Confirmar esta reserva? (SI/NO): ").strip().upper()

                            if confirmacion == "SI":
                                try:
                                    reserva.confirmar()
                                    print(f"\n✓ Reserva confirmada exitosamente")
                                    
                                    procesar = input("¿Desea procesar/completar la reserva ahora? (SI/NO): ").strip().upper()
                                    if procesar == "SI":
                                        costo = reserva.procesar()
                                        print(f"✓ Reserva completada - Costo total: ${costo:.2f}")
                                    else:
                                        print("La reserva queda en estado CONFIRMADA")
                                    
                                    print(reserva.mostrar_info())
                                    registrar_log(f"Reserva confirmada: {reserva.mostrar_info()}")
                                except Exception as e:
                                    print(f"✖ Error al confirmar: {e}")
                                    registrar_log(f"Error confirmando reserva: {e}", "error")
                        except Exception as e:
                            print(f"✖ Error: {e}")

                    elif sub_opcion == "5":
                        break
                    else:
                        print("Opción no válida")

            elif opcion == "4":
                # Estadísticas
                print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
                print(f"Total clientes: {len(sistema.clientes)}")
                print(f"Total reservas: {len(sistema.reservas)}")

                if sistema.reservas:
                    completadas = sum(1 for r in sistema.reservas if r.estado == "completada")
                    canceladas = sum(1 for r in sistema.reservas if r.estado == "cancelada")
                    pendientes = sum(1 for r in sistema.reservas if r.estado == "pendiente")
                    confirmadas = sum(1 for r in sistema.reservas if r.estado == "confirmada")
                    ingresos = sum(r.costo_total for r in sistema.reservas if r.estado == "completada")

                    print(f"  Completadas: {completadas}")
                    print(f"  Confirmadas (sin procesar): {confirmadas}")
                    print(f"  Canceladas: {canceladas}")
                    print(f"  Pendientes: {pendientes}")
                    print(f"  Ingresos totales: ${ingresos:.2f}")

            elif opcion == "5":
                # Simular operaciones demo
                simular_operaciones(sistema)

            elif opcion == "6":
                print("\n¡Gracias por usar Software FJ!")
                registrar_log("Sistema cerrado por el usuario")
                break

            else:
                print("\n⚠ Opción no válida")

        except KeyboardInterrupt:
            print("\n\nSistema interrumpido por el usuario")
            registrar_log("Sistema interrumpido (KeyboardInterrupt)", "warning")
            break

        except Exception as e:
            print(f"\n✖ Error inesperado: {e}")
            registrar_log(f"Error general en main: {e}", "error")


if __name__ == "__main__":
    main()