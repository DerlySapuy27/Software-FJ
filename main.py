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
    print("3. Gestionar Reservas (Ver/Cancelar)")
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

    # 6. Reserva de sala válida (PENDIENTE - no se procesa aún)
    try:
        print(
            "\n6. Creando reserva de sala válida (Juan Pérez, Sala VIP, 3h) - SIN PROCESAR..."
        )
        cliente = sistema.buscar_cliente("12345")
        servicio = servicios_disponibles[0]  # Sala VIP
        reserva = sistema.crear_reserva(cliente, servicio, 3)
        reserva.confirmar()
        # NO se procesa, se deja como "confirmada" para probar cancelación después
        print(f"   ✓ ÉXITO: Reserva creada y confirmada (Estado: {reserva.estado})")
        registrar_log(f"Reserva creada: {reserva.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 7. Alquiler de equipo válido
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

    # 10. Asesoría especializada
    try:
        print(
            "\n10. Creando asesoría especializada (Juan Pérez, Python Avanzado, 4h)..."
        )
        cliente = sistema.buscar_cliente("12345")
        servicio = servicios_disponibles[2]  # Consultoría Python
        reserva = sistema.crear_reserva(cliente, servicio, 4)
        reserva.confirmar()
        costo = reserva.procesar()
        print(f"   ✓ ÉXITO: Asesoría confirmada y procesada - Costo: ${costo:.2f}")
        registrar_log(f"Asesoría exitosa: {reserva.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 11. CANCELAR una reserva (la que dejamos sin procesar en el paso 6)
    try:
        print("\n11. CANCELANDO la reserva de sala del paso 6...")
        # Buscar la primera reserva que esté confirmada pero no completada
        reserva_a_cancelar = None
        for r in sistema.reservas:
            if r.estado == "confirmada":
                reserva_a_cancelar = r
                break

        if reserva_a_cancelar:
            print(
                f"    Reserva encontrada: Cliente={reserva_a_cancelar._cliente.nombre}, Estado={reserva_a_cancelar.estado}"
            )
            # Usar try/except/else/finally como pide el requisito
            try:
                resultado = reserva_a_cancelar.cancelar("Cliente cambió de opinión")
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

    # 12. Intentar cancelar reserva ya COMPLETADA (debe fallar)
    try:
        print("\n12. Intentando cancelar una reserva ya COMPLETADA...")
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

    # 13. Mostrar todos los clientes
    try:
        print("\n13. LISTADO DE CLIENTES REGISTRADOS:")
        print(f"    Total: {len(sistema.clientes)}")
        for i, c in enumerate(sistema.clientes, 1):
            print(f"    {i}. {c.mostrar_info()}")
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    # 14. Mostrar estado final de todas las reservas
    try:
        print("\n14. ESTADO FINAL DE RESERVAS:")
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
                f"    {emoji} [{i}] {r.estado.upper()} | Cliente: {r._cliente.nombre} | Costo: ${r.costo_total:.2f}"
            )
    except Exception as e:
        print(f"   ✖ ERROR: {e}")

    registrar_log("Simulación completada exitosamente")
    print("\n" + "=" * 50)
    print("   ✓ SIMULACIÓN COMPLETADA (14 operaciones)")
    print("   Incluye: creación, validación, reservas y cancelación")
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

                    # Confirmar y procesar
                    reserva.confirmar()
                    costo = reserva.procesar()

                    print(f"\n✓ Reserva exitosa!")
                    print(reserva.mostrar_info())
                    registrar_log(f"Reserva exitosa: {reserva.mostrar_info()}")

                except Exception as e:
                    print(f"\n✖ Error en reserva: {e}")
                    registrar_log(f"Error en reserva: {e}", "error")

            elif opcion == "3":
                # Gestionar Reservas (Ver/Cancelar)
                while True:
                    print("\n--- GESTIÓN DE RESERVAS ---")
                    print("1. Ver todas las reservas")
                    print("2. Cancelar una reserva")
                    print("3. Volver")
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
                            print(
                                "  Solo se pueden cancelar reservas 'pendientes' o 'confirmadas'"
                            )
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
                                print(
                                    "  Solo se pueden cancelar reservas 'pendientes' o 'confirmadas'"
                                )
                                continue

                            # Pedir confirmación
                            print(f"\n¿Está seguro de cancelar esta reserva?")
                            print(reserva.mostrar_info())

                            motivo = input(
                                "\nMotivo de cancelación (opcional): "
                            ).strip()
                            confirmacion = (
                                input("Escriba 'SI' para confirmar cancelación: ")
                                .strip()
                                .upper()
                            )

                            if confirmacion == "SI":
                                # Usar try/except/else/finally como pide el requisito
                                try:
                                    resultado = reserva.cancelar(
                                        motivo if motivo else ""
                                    )
                                except Exception as e:
                                    print(f"\n✖ Error al cancelar: {e}")
                                    registrar_log(
                                        f"Error cancelando reserva: {e}", "error"
                                    )
                                else:
                                    # Se ejecuta si NO hubo excepción
                                    print(f"\n✓ Reserva cancelada exitosamente")
                                    print(reserva.mostrar_info())
                                    registrar_log(
                                        f"Reserva cancelada: {reserva.mostrar_info()}"
                                    )
                                finally:
                                    # Se ejecuta SIEMPRE
                                    print("Operación de cancelación finalizada")
                            else:
                                print("Cancelación abortada por el usuario")

                        except Exception as e:
                            print(f"✖ Error: {e}")
                            registrar_log(f"Error en cancelación: {e}", "error")

                    elif sub_opcion == "3":
                        break
                    else:
                        print("Opción no válida")

            elif opcion == "4":
                # Estadísticas
                print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
                print(f"Total clientes: {len(sistema.clientes)}")
                print(f"Total reservas: {len(sistema.reservas)}")

                if sistema.reservas:
                    completadas = sum(
                        1 for r in sistema.reservas if r.estado == "completada"
                    )
                    canceladas = sum(
                        1 for r in sistema.reservas if r.estado == "cancelada"
                    )
                    pendientes = sum(
                        1 for r in sistema.reservas if r.estado == "pendiente"
                    )
                    confirmadas = sum(
                        1 for r in sistema.reservas if r.estado == "confirmada"
                    )
                    ingresos = sum(
                        r.costo_total
                        for r in sistema.reservas
                        if r.estado == "completada"
                    )

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
