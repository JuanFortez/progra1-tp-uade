from time import sleep
from datetime import datetime

from datos.persistencia import cargar_datos, guardar_datos
from consultas.validacion.index import validar_entero
from consultas.visualizacion.index import mostrar_estacionamiento, contar_plazas_ocupadas, es_plaza_real
from gestion.index import (
    buscar_vehiculo,
    crear_estacionamiento,
    modificar_estado_plaza,
    modificar_estacionamiento,
    registrar_ingreso_vehiculo,
    registrar_salida_vehiculo,
    login,
)
from gestion.reservas import (
    asignar_plaza,
    buscar_fecha,
    cancelar_reserva,
    crear_reserva_administrador,
    crear_reserva_cliente,
    lista_reservas_activas,
    lista_reservas_clientes,
    modificar_reserva,
    buscar_reserva_por_cliente,
)
from ui.index import (
    encabezado_principal,
    limpiar_pantalla,
    lista_menu_principal,
    lista_panel_administracion,
    lista_panel_cliente,
    lista_reservas_admin,
)


def interfaz_inicio():
    """
    Muestra el menú principal de la aplicación Parking Control.
    Permite al usuario seleccionar entre el panel de administrador, panel de cliente o salir del programa.
    """
    limpiar_pantalla()
    print("🚗" * 19)
    print(" " * 5 + "BIENVENIDO A PARKING CONTROL")
    print("🚗" * 19)

    try:
        datos = cargar_datos()
    except Exception as e:
        print(f"\nNo se pudieron cargar los datos guardados ({e}).")
        print("Se iniciará con datos vacíos.\n")
        datos = {
            "matriz": None,
            "reservas": [],
            "reservas_clientes": [],
            "registros": {},
            "historial": [],
            "clientes": [],
            "admin": None,
        }

    reservas = datos["reservas"]
    reservas_clientes = datos["reservas_clientes"]
    registros = datos["registros"]
    matriz = datos["matriz"]
    historial = datos["historial"]
    clientes = datos["clientes"]

    while True:
        lista_menu_principal()

        opcion = validar_entero("Seleccione una opción: ", 1, 3)

        match opcion:
            case 1:
                print("Accediendo a panel de administración...")
                admin = login(datos["admin"])
                datos["admin"] = admin

                if matriz is None:
                    matriz = crear_estacionamiento()

                guardar_datos(
                    matriz,
                    reservas,
                    reservas_clientes,
                    registros,
                    historial,
                    clientes,
                    admin,
                )
                interfaz_admin(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 2:
                if matriz is None:
                    print("\nPrimero el administrador debe crear el estacionamiento.")
                else:
                    print("Accediendo a panel de cliente...")
                    interfaz_cliente(
                        matriz,
                        reservas,
                        reservas_clientes,
                        registros,
                        historial,
                        clientes,
                        datos["admin"],
                    )
            case 3:
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, datos["admin"]
                )
                print("\n👋 ¡Gracias por usar Parking Control!")
                print("🚗 ¡Hasta la próxima!")
                sleep(2)
                break


def interfaz_admin(matriz, reservas, reservas_clientes, registros, historial, clientes, admin):
    """
    Muestra el panel de administración del estacionamiento.
    Permite al administrador registrar ingresos y salidas de vehículos, ver la ocupación actual y buscar vehículos.
    """
    limpiar_pantalla()
    encabezado_principal()

    while True:
        lista_panel_administracion()

        opcion = validar_entero("Seleccione una opción: ", 1, 10)

        match opcion:
            case 1:
                print("Ingreso de vehiculo...")
                registrar_ingreso_vehiculo(matriz, registros, historial)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 2:
                print("Salida de vehiculo...")
                registrar_salida_vehiculo(matriz, registros, historial)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 3:
                print("Estado de estacionamiento...")
                mostrar_estacionamiento(matriz)

            case 4:
                print("Búsqueda de vehículo...")
                buscar_vehiculo(matriz, registros)

            case 5:
                modificar_estado_plaza(matriz, registros)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 6:
                interfaz_reservas_admin(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 7:
                mostrar_historial(historial)

            case 8:
                modificar_estacionamiento(matriz, registros, reservas)
                guardar_datos(
                    matriz,
                    reservas,
                    reservas_clientes,
                    registros,
                    historial,
                    clientes,
                    admin,
                )

            case 9:
                mostrar_estadisticas(historial, matriz)

            case 10:
                print("\n👋 Saliendo del panel de administración...")
                sleep(2)
                break


def interfaz_cliente(
    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
):
    """
    Muestra el panel de cliente.
    Permite al cliente solicitar una reserva o salir del panel.
    """
    limpiar_pantalla()
    encabezado_principal()

    while True:
        lista_panel_cliente()

        opcion = validar_entero("Seleccione una opción: ", 1, 2)
        if opcion == 1:
            print("Solicitud de reserva...")
            crear_reserva_cliente(reservas_clientes)
            guardar_datos(
                matriz, reservas, reservas_clientes, registros, historial, clientes, admin
            )

        elif opcion == 2:
            print("\n👋 ¡Gracias por usar Parking Control!")
            print("🚗 Saliendo del panel de cliente...")
            sleep(2)
            break


def interfaz_reservas_admin(
    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
):
    """
    Muestra el submenú de gestión de reservas para el administrador.
    Permite crear, cancelar, modificar y listar reservas actuales.
    """
    limpiar_pantalla()

    while True:
        lista_reservas_admin()

        opcion = validar_entero("Seleccione una opción: ", 1, 9)

        match opcion:
            case 1:
                print("Creación de reserva...")
                crear_reserva_administrador(reservas, matriz, clientes)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 2:
                print("Cancelación de reserva...")
                cancelar_reserva(reservas)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 3:
                print("Modificación de reserva...")
                modificar_reserva(reservas, matriz)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 4:
                print("Listado de reservas activas...")
                lista_reservas_activas(reservas, matriz)

            case 5:
                print("Listado de reservas de clientes...")
                lista_reservas_clientes(reservas_clientes)

            case 6:
                print("Búsqueda de reservas por fecha...")
                buscar_fecha(reservas, matriz)

            case 7:
                buscar_reserva_por_cliente(
                    reservas, reservas_clientes, clientes, matriz
                )

            case 8:
                print("Asignación de plaza...")
                asignar_plaza(reservas_clientes, reservas, matriz)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin
                )

            case 9:
                print("Volviendo al panel de administración...")
                sleep(1)
                break

            case _:
                print("Opción inválida.")


def mostrar_historial(historial):
    """
    Muestra el historial de ingresos y egresos del estacionamiento.
    """
    if len(historial) == 0:
        print("\nNo hay movimientos registrados.")
        return

    print("\nHistorial de movimientos:\n")

    for movimiento in historial:
        print(f"Acción: {movimiento['accion']}")
        print(f"Patente: {movimiento['patente']}")
        print(f"Tipo: {movimiento['tipo_vehiculo']}")

        if "fecha_hora" in movimiento:
            print(f"Fecha y hora: {formatear_fecha_hora(movimiento['fecha_hora'])}")

        if "hora_ingreso" in movimiento:
            print(f"Hora ingreso: {formatear_fecha_hora(movimiento['hora_ingreso'])}")

        if "hora_salida" in movimiento:
            print(f"Hora salida: {formatear_fecha_hora(movimiento['hora_salida'])}")

        if "tiempo_estacionado" in movimiento:
            print(f"Tiempo estacionado: {movimiento['tiempo_estacionado']}")

        if "tarifa" in movimiento:
            print(f"Tarifa: ${movimiento['tarifa']:.2f}")

        print("-" * 30)


def formatear_fecha_hora(fecha_hora):
    """
    Convierte una fecha/hora guardada en un formato mas legible.
    """

    if isinstance(fecha_hora, str):
        fecha_hora = datetime.fromisoformat(fecha_hora)

    return fecha_hora.strftime("%d/%m/%Y %H:%M:%S")


def mostrar_estadisticas(historial, matriz):
    """
    Muestra estadísticas del estacionamiento:
    - Total recaudado (suma de tarifas del historial)
    - Porcentaje de ocupación promedio de la matriz actual
    """
    print("\n" + "=" * 40)
    print(" " * 10 + "ESTADÍSTICAS")
    print("=" * 40)

    # --- Total recaudado ---
    total_recaudado = 0.0
    cantidad_pagos = 0

    for movimiento in historial:
        if "tarifa" in movimiento and movimiento["tarifa"] is not None:
            total_recaudado += movimiento["tarifa"]
            cantidad_pagos += 1

    print(f"\n💰 Total recaudado: ${total_recaudado:.2f}")
    print(f"Pagos registrados: {cantidad_pagos}")

    # --- Ocupación actual ---
    if matriz is None:
        print("\n🅿️  Ocupación actual: No hay estacionamiento creado.")
    else:
        total_plazas = sum(1 for fila in matriz for celda in fila if es_plaza_real(celda))
        plazas_ocupadas = contar_plazas_ocupadas(matriz)

        if total_plazas > 0:
            porcentaje = (plazas_ocupadas / total_plazas) * 100
            print(f"\n🅿️  Ocupación actual: {plazas_ocupadas}/{total_plazas} plazas ocupadas ({porcentaje:.1f}%)")
        else:
            print("\n🅿️  Ocupación actual: Sin plazas disponibles.")

    print("\n" + "=" * 40)
    input("\nPresione Enter para continuar...")