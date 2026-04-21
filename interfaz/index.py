from time import sleep

from consultas.validacion.index import validar_entero
from consultas.visualizacion.index import mostrar_estacionamiento
from gestion.index import (
    buscar_vehiculo,
    crear_estacionamiento,
    modificar_estado_plaza,
    registrar_ingreso_vehiculo,
    registrar_salida_vehiculo,
)
from gestion.reservas import (
    buscar_fecha,
    cancelar_reserva,
    crear_reserva,
    lista_reservas_activas,
    modificar_reserva,
)
from ui.index import encabezado_principal, limpiar_pantalla


def interfaz_inicio():
    """
    Muestra el menú principal de la aplicación Parking Control.
    Permite al usuario seleccionar entre el panel de administrador, panel de cliente o salir del programa.
    """
    limpiar_pantalla()
    print("🚗" * 19)
    print(" " * 5 + "BIENVENIDO A PARKING CONTROL")
    print("🚗" * 19)

    reservas = []
    matriz = None

    while True:
        print("\n" + "=" * 40)
        print(" " * 13 + "MENÚ PRINCIPAL")
        print("=" * 40)
        print("\n  1 - Panel Administrador")
        print("  2 - Panel Cliente")
        print("  3 - Salir\n")

        opcion = validar_entero("Seleccione una opción: ", 1, 3)

        match opcion:
            case 1:
                print("Accediendo a panel de administración...")

                if matriz is None:
                    matriz = crear_estacionamiento()

                interfaz_admin(matriz, reservas)

            case 2:
                if matriz is None:
                    print("\nPrimero el administrador debe crear el estacionamiento.")
                else:
                    print("Accediendo a panel de cliente...")
                    interfaz_cliente(matriz, reservas)

            case 3:
                print("\n👋 ¡Gracias por usar Parking Control!")
                print("🚗 ¡Hasta la próxima!")
                sleep(2)
                break


def interfaz_admin(matriz, reservas):
    """
    Muestra el panel de administración del estacionamiento.
    Permite al administrador registrar ingresos y salidas de vehículos, ver la ocupación actual y buscar vehículos.
    """
    limpiar_pantalla()
    encabezado_principal()

    while True:
        print("\n" + "=" * 39)
        print(" " * 8 + "PANEL DE ADMINISTRACIÓN")
        print("=" * 39)

        print("\n  1 - Registrar ingreso de vehículo")
        print("  2 - Registrar egreso de vehículo")
        print("  3 - Ver ocupación actual")
        print("  4 - Buscar vehículo")
        print("  5 - Modificar plaza")
        print("  6 - Gestionar reservas")
        print("  9 - Volver\n")

        opcion = validar_entero("Seleccione una opción: ", 1, 9)

        if opcion in [7, 8]:
            print("Opción no válida.")
            continue

        match opcion:
            case 1:
                print("Ingreso de vehiculo...")
                registrar_ingreso_vehiculo(matriz)

            case 2:
                print("Salida de vehiculo...")
                registrar_salida_vehiculo(matriz)

            case 3:
                print("Estado de estacionamiento...")
                mostrar_estacionamiento(matriz)

            case 4:
                print("Búsqueda de vehículo...")
                buscar_vehiculo(matriz)

            case 5:
                modificar_estado_plaza(matriz)

            case 6:
                interfaz_reservas_admin(matriz, reservas)

            case 9:
                print("\n👋 Saliendo del panel de administración...")
                sleep(2)
                break


def interfaz_cliente(matriz, reservas):
    """
    Muestra el panel de cliente.
    Permite al cliente solicitar una reserva o salir del panel.
    """
    limpiar_pantalla()
    encabezado_principal()

    while True:
        print("\n=== PANEL DE CLIENTE ===\n")
        print("  1 - Solicitar reserva")
        print("  2 - Salir\n")

        opcion = validar_entero("Seleccione una opción: ", 1, 2)
        if opcion == 1:
            print("Solicitud de reserva...")
            crear_reserva(reservas, matriz)

        elif opcion == 2:
            print("\n👋 ¡Gracias por usar Parking Control!")
            print("🚗 Saliendo del panel de cliente...")
            sleep(2)
            break


def interfaz_reservas_admin(matriz, reservas):
    """
    Muestra el submenú de gestión de reservas para el administrador.
    Permite crear, cancelar, modificar y listar reservas actuales.
    """
    limpiar_pantalla()

    while True:
        print("\n" + "=" * 40)
        print(" " * 10 + "Gestión de Reservas")
        print("=" * 40)
        print("\n  1 - Crear reserva")
        print("  2 - Cancelar reserva")
        print("  3 - Modificar reserva")
        print("  4 - Ver reservas activas")
        print("  5 - Buscar reservas por fecha")
        print("  9 - Volver\n")

        opcion = validar_entero("Seleccione una opción: ", 1, 9)

        if opcion in [6, 7, 8]:
            print("Opción no válida.")
            continue

        match opcion:
            case 1:
                print("Creación de reserva...")
                crear_reserva(reservas, matriz)

            case 2:
                print("Cancelación de reserva...")
                cancelar_reserva(reservas)

            case 3:
                print("Modificación de reserva...")
                modificar_reserva(reservas, matriz)

            case 4:
                print("Listado de reservas activas...")
                lista_reservas_activas(reservas)

            case 5:
                print("Búsqueda de reservas por fecha...")
                buscar_fecha(reservas)

            case 9:
                print("Volviendo al panel de administración...")
                break

            case _:
                print("Opción inválida.")
