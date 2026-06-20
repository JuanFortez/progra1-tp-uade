from time import sleep
from datetime import datetime
from unittest import case
from datos.persistencia import cargar_datos, guardar_datos
from consultas.validacion.index import validar_entero, validar_patente, validar_fecha
from consultas.visualizacion.index import mostrar_estacionamiento, contar_plazas_ocupadas, es_plaza_real
from login.index import login, crear_admin
from gestion.index import (
    buscar_vehiculo,
    crear_estacionamiento,
    modificar_estado_plaza,
    modificar_estacionamiento,
    registrar_ingreso_vehiculo,
    registrar_salida_vehiculo,
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
from gestion.abonos import (
    crear_abono_administrador,
    crear_abono_cliente,
    listar_abonos,
)
from ui.index import (
    encabezado_principal,
    limpiar_pantalla,
    lista_menu_principal,
    lista_panel_administracion,
    lista_panel_cliente,
    lista_reservas_admin,
    lista_abonos_admin,
    tabla_tarifas_abono,
    lista_historial,
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
    abonos = datos["abonos"]
    abonos_clientes = datos["abonos_clientes"]

    while True:
        lista_menu_principal()

        opcion = validar_entero("Seleccione una opción: ", 1, 3)
        
        match opcion:
            case 1:
                print("Accediendo a panel de administración...")

                if datos["admin"] is None:
                    admin = crear_admin()
                else:
                    if not login(datos["admin"]):
                        continue
                    admin = datos["admin"]

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
                    abonos,
                    abonos_clientes,
                )
                interfaz_admin(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
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
                        abonos,
                        abonos_clientes,
                    )
            case 3:
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, datos["admin"], abonos, abonos_clientes
                )
                print("\n👋 ¡Gracias por usar Parking Control!")
                print("🚗 ¡Hasta la próxima!")
                sleep(2)
                break


def interfaz_admin(matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes):
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
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
                )

            case 2:
                print("Salida de vehiculo...")
                registrar_salida_vehiculo(matriz, registros, historial)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
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
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
                )

            case 6:
                interfaz_reservas_admin(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
                )
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
                )

            case 7:
                menu_historial(historial)

            case 8:
                modificar_estacionamiento(matriz, registros, reservas, reservas_clientes)
                guardar_datos(
                    matriz,
                    reservas,
                    reservas_clientes,
                    registros,
                    historial,
                    clientes,
                    admin,
                    abonos,
                    abonos_clientes,
                )

            case 9:
                mostrar_estadisticas(historial, matriz)

            case 10:
                print("\n👋 Saliendo del panel de administración...")
                sleep(2)
                break


def interfaz_cliente(
    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
):
    """
    Muestra el panel de cliente.
    Permite al cliente solicitar una reserva, un abono o salir del panel.
    """
    limpiar_pantalla()
    encabezado_principal()

    while True:
        lista_panel_cliente()

        opcion = validar_entero("Seleccione una opción: ", 1, 3)
        if opcion == 1:
            print("Solicitud de reserva...")
            crear_reserva_cliente(reservas_clientes)
            guardar_datos(
                matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
            )

        elif opcion == 2:
            print("Solicitud de abono...")
            crear_abono_cliente(abonos_clientes)
            guardar_datos(
                matriz, reservas, reservas_clientes, registros, historial, clientes, abonos, abonos_clientes
            )

        elif opcion == 3:
            print("\n👋 ¡Gracias por usar Parking Control!")
            print("🚗 Saliendo del panel de cliente...")
            sleep(2)
            break


def interfaz_reservas_admin(
    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
):
    """
    Muestra el submenú de gestión de reservas para el administrador.
    Permite crear, cancelar, modificar y listar reservas y abonos.
    """
    limpiar_pantalla()

    while True:
        lista_reservas_admin()

        opcion = validar_entero("Seleccione una opción: ", 1, 10)

        match opcion:
            case 1:
                print("Creación de reserva...")
                crear_reserva_administrador(reservas, reservas_clientes, matriz, clientes)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
                )

            case 2:
                print("Cancelación de reserva...")
                cancelar_reserva(reservas, matriz)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
                )

            case 3:
                print("Modificación de reserva...")
                modificar_reserva(reservas, reservas_clientes, matriz)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
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
                    matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos, abonos_clientes
                )

            case 9:
                interfaz_abonos_admin(matriz, reservas, reservas_clientes, registros, historial, clientes, abonos, abonos_clientes)

            case 10:
                print("Volviendo al panel de administración...")
                sleep(1)
                break

            case _:
                print("Opción inválida.")


def interfaz_abonos_admin(
    matriz, reservas, reservas_clientes, registros, historial, clientes, abonos, abonos_clientes
):
    """
    Submenú de gestión de abonos para el administrador.
    """
    limpiar_pantalla()

    while True:
        lista_abonos_admin()

        opcion = validar_entero("Seleccione una opción: ", 1, 5)

        match opcion:
            case 1:
                print("Creación de abono...")
                crear_abono_administrador(abonos, reservas, matriz, clientes)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, abonos, abonos_clientes
                )

            case 2:
                listar_abonos(abonos)
                input("\nPresione Enter para continuar...")

            case 3:
                print("Cancelación de abono...")
                cancelar_reserva(abonos)
                guardar_datos(
                    matriz, reservas, reservas_clientes, registros, historial, clientes, abonos, abonos_clientes
                )

            case 4:
                tabla_tarifas_abono()
                input("\nPresione Enter para continuar...")

            case 5:
                print("Volviendo a gestión de reservas...")
                sleep(1)
                break

def menu_historial(historial):
    """
    Muestra el menú del historial y ejecuta la opción elegida.
    """
    while True:
        lista_historial()

        opcion = validar_entero("Seleccione una opción: ", 1, 5)

        if opcion == 1:
            mostrar_historial_completo(historial)

        elif opcion == 2:
            buscar_historial_por_patente(historial)

        elif opcion == 3:
            buscar_historial_por_fecha(historial)

        elif opcion == 4:
            mostrar_historial_ordenado_por_monto(historial)

        elif opcion == 5:
            print("Volviendo al panel de administración...")
            sleep(1)
            break

def mostrar_historial_completo(historial):
    """
    Muestra todos los movimientos guardados en el historial.
    """
    if len(historial) == 0:
        mostrar_mensaje_sin_movimientos()
    else:
        mostrar_lista_movimientos(historial)


def buscar_historial_por_patente(historial):
    """
    Busca movimientos del historial usando una patente.
    """
    patente = pedir_patente_historial()
    movimientos = filtrar_por_patente(historial, patente)

    mostrar_resultado_historial(movimientos)

def pedir_patente_historial():
    """
    Pide una patente válida para buscar en el historial.
    """
    patente = input("Ingrese la patente: ").upper().strip()

    while not validar_patente(patente):
        print("Patente inválida. Formato esperado: ABC123 o AB123CD")
        patente = input("Ingrese la patente: ").upper().strip()

    return patente


def filtrar_por_patente(historial, patente):
    """
    Devuelve los movimientos que coinciden con la patente ingresada.
    """
    movimientos_filtrados = []

    for movimiento in historial:
        if movimiento["patente"] == patente:
            movimientos_filtrados.append(movimiento)

    return movimientos_filtrados

def buscar_historial_por_fecha(historial):
    """
    Busca movimientos del historial usando una fecha.
    """
    fecha = pedir_fecha_historial()
    movimientos = filtrar_por_fecha(historial, fecha)

    mostrar_resultado_historial(movimientos)


def pedir_fecha_historial():
    """
    Pide una fecha válida en formato AAAA-MM-DD.
    """
    fecha = input("Ingrese la fecha AAAA-MM-DD: ").strip()

    while not validar_fecha(fecha):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha = input("Ingrese la fecha AAAA-MM-DD: ").strip()

    return fecha


def filtrar_por_fecha(historial, fecha_buscada):
    """
    Devuelve los movimientos que coinciden con la fecha ingresada.
    """
    movimientos_filtrados = []

    for movimiento in historial:
        fecha_movimiento = obtener_fecha_movimiento(movimiento)

        if fecha_movimiento[:10] == fecha_buscada:
            movimientos_filtrados.append(movimiento)

    return movimientos_filtrados

def obtener_fecha_movimiento(movimiento):
    """
    Devuelve la fecha del movimiento según el dato disponible.
    """
    if "fecha_hora" in movimiento:
        return movimiento["fecha_hora"]

    if "hora_salida" in movimiento:
        return movimiento["hora_salida"]

    if "hora_ingreso" in movimiento:
        return movimiento["hora_ingreso"]

    return ""


def mostrar_historial_ordenado_por_monto(historial):
    """
    Muestra los movimientos con monto ordenados de mayor a menor.
    """
    movimientos = obtener_movimientos_con_monto(historial)
    ordenar_por_monto(movimientos)

    mostrar_resultado_historial(movimientos)


def obtener_movimientos_con_monto(historial):
    """
    Devuelve solamente los movimientos que tienen tarifa.
    """
    movimientos_con_monto = []

    for movimiento in historial:
        if "tarifa" in movimiento:
            movimientos_con_monto.append(movimiento)

    return movimientos_con_monto


def ordenar_por_monto(movimientos):
    """
    Ordena los movimientos por tarifa de mayor a menor usando burbujeo.
    """
    cantidad = len(movimientos)

    for i in range(cantidad):
        for j in range(0, cantidad - 1):
            monto_actual = movimientos[j]["tarifa"]
            monto_siguiente = movimientos[j + 1]["tarifa"]

            if monto_actual < monto_siguiente:
                auxiliar = movimientos[j]
                movimientos[j] = movimientos[j + 1]
                movimientos[j + 1] = auxiliar


def mostrar_resultado_historial(movimientos):
    """
    Muestra el resultado de una búsqueda del historial.
    """
    if len(movimientos) == 0:
        mostrar_mensaje_sin_movimientos()
    else:
        mostrar_lista_movimientos(movimientos)


def mostrar_mensaje_sin_movimientos():
    """
    Muestra un mensaje cuando no hay movimientos.
    """
    print("\nNo se encontraron movimientos.")
    input("\nPresione Enter para continuar...")


def mostrar_lista_movimientos(movimientos):
    """
    Muestra una lista de movimientos del historial.
    """
    for movimiento in movimientos:
        mostrar_un_movimiento(movimiento)

    input("\nPresione Enter para continuar...")


def mostrar_un_movimiento(movimiento):
    """
    Muestra un movimiento del historial.
    """
    print("\nAcción:", movimiento["accion"])
    print("Patente:", movimiento["patente"])
    print("Tipo de vehículo:", movimiento["tipo_vehiculo"])

    mostrar_fecha_movimiento(movimiento)
    mostrar_tiempo_estacionado(movimiento)
    mostrar_tarifa_movimiento(movimiento)

    print("-" * 30)


def mostrar_fecha_movimiento(movimiento):
    """
    Muestra la fecha del movimiento.
    """
    fecha = obtener_fecha_movimiento(movimiento)

    if fecha != "":
        print("Fecha:", fecha[:10])


def mostrar_tiempo_estacionado(movimiento):
    """
    Muestra el tiempo estacionado si existe.
    """
    if "tiempo_estacionado" in movimiento:
        print("Tiempo estacionado:", movimiento["tiempo_estacionado"])


def mostrar_tarifa_movimiento(movimiento):
    """
    Muestra la tarifa si existe.
    """
    if "tarifa" in movimiento:
        print("Tarifa: $", movimiento["tarifa"])

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

    total_recaudado = 0.0
    cantidad_pagos = 0

    for movimiento in historial:
        if "tarifa" in movimiento and movimiento["tarifa"] is not None:
            total_recaudado += movimiento["tarifa"]
            cantidad_pagos += 1

    print(f"\n💰 Total recaudado: ${total_recaudado:.2f}")
    print(f"Pagos registrados: {cantidad_pagos}")

    if matriz is None:
        print("\n🅿️ Ocupación actual: No hay estacionamiento creado.")
    else:
        total_plazas = 0
        plazas_ocupadas = 0

        for fila in matriz:
            for plaza in fila:
                if plaza is None:
                    continue
                if isinstance(plaza, dict):
                    estado = plaza.get("estado", "")
                else: 
                    estado = plaza
                    
                if estado not in ("  ", ""):
                    total_plazas += 1
                    if estado == "🟥":
                        plazas_ocupadas += 1

        if total_plazas > 0:
            porcentaje = (plazas_ocupadas / total_plazas) * 100
            print(f"\n🅿️  Ocupación actual: {plazas_ocupadas}/{total_plazas} plazas ocupadas ({porcentaje:.1f}%)")
        else:
            print("\n🅿️  Ocupación actual: Sin plazas disponibles.")

    print("\n" + "=" * 40)
    input("\nPresione Enter para continuar...")
