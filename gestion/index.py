from datetime import datetime
import math
from consultas.constantes.index import TIPO_VEHICULO, MULTIPLICADORES_TARIFA, ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_VACIO, ESTADO_OCUPADO, ESTADO_RESERVADA
from consultas.validacion.index import validar_entero, validar_patente
from consultas.visualizacion.index import mostrar_estacionamiento
from ui.index import (
    limpiar_pantalla,
    lista_crear_estacionamiento,
    lista_modificar_estado_plaza,
)


def crear_estacionamiento():
    """
    Permite crear un estacionamiento eligiendo entre distintos planos predeterminados.

    El administrador puede crear:
    1. Un estacionamiento rectangular clásico.
    2. Dos columnas de plazas con un pasillo central.
    3. Un estacionamiento con doble pasillo.
    4. Un estacionamiento en forma de U.

    Retorna una matriz que representa visualmente el estacionamiento.
    """
    limpiar_pantalla()

    lista_crear_estacionamiento()

    opcion = validar_entero("Seleccione una opción: ", 1, 4)

    match opcion:
        case 1:
            return crear_estacionamiento_rectangular()

        case 2:
            cantidad_plazas = validar_entero("\nCantidad de plazas: ", 1)
            return crear_estacionamiento_dos_columnas(cantidad_plazas)

        case 3:
            cantidad_plazas = validar_entero("\nCantidad de plazas: ", 1)
            return crear_estacionamiento_doble_pasillo(cantidad_plazas)

        case 4:
            cantidad_plazas = validar_entero("\nCantidad de plazas: ", 1)
            return crear_estacionamiento_en_u(cantidad_plazas)


def crear_estacionamiento_rectangular():
    """
    Crea un estacionamiento rectangular tradicional usando filas y columnas.

    Todas las posiciones de la matriz son plazas libres.
    """
    print("\nIngrese las filas y columnas del estacionamiento:\n")

    filas = validar_entero("Filas: ", 1)
    columnas = validar_entero("Columnas: ", 1)

    matriz = []

    for fila in range(filas):
        matriz.append([])

        for columna in range(columnas):
            matriz[fila].append(ESTADO_LIBRE)

    return matriz


def crear_estacionamiento_dos_columnas(cantidad_plazas):
    """
    Crea un estacionamiento con dos columnas de plazas y un pasillo central.

    Ejemplo visual:

    LIBRE  PASILLO  LIBRE
    LIBRE  PASILLO  LIBRE
    LIBRE  PASILLO  LIBRE

    Si la cantidad de plazas es impar, la última fila queda con una sola plaza
    y un espacio vacío del otro lado.
    """
    matriz = []
    plazas_creadas = 0

    while plazas_creadas < cantidad_plazas:
        fila = []

        fila.append(ESTADO_LIBRE)
        plazas_creadas += 1

        fila.append(ESTADO_PASILLO)

        if plazas_creadas < cantidad_plazas:
            fila.append(ESTADO_LIBRE)
            plazas_creadas += 1
        else:
            fila.append(ESTADO_VACIO)

        matriz.append(fila)

    return matriz


def crear_estacionamiento_doble_pasillo(cantidad_plazas):
    """
    Crea un estacionamiento con cuatro columnas de plazas y dos pasillos.

    Ejemplo visual:

    LIBRE  PASILLO  LIBRE  LIBRE  PASILLO  LIBRE
    LIBRE  PASILLO  LIBRE  LIBRE  PASILLO  LIBRE

    Cada fila puede contener hasta cuatro plazas reales.
    """
    matriz = []
    plazas_creadas = 0

    while plazas_creadas < cantidad_plazas:
        fila = []

        for posicion in range(6):
            if posicion == 1 or posicion == 4:
                fila.append(ESTADO_PASILLO)
            else:
                if plazas_creadas < cantidad_plazas:
                    fila.append(ESTADO_LIBRE)
                    plazas_creadas += 1
                else:
                    fila.append(ESTADO_VACIO)

        matriz.append(fila)

    return matriz


def crear_estacionamiento_en_u(cantidad_plazas):
    """
    Crea un estacionamiento en forma de U.

    Una fila horizontal en la parte superior (3 o 5 plazas) y luego
    dos columnas en los costados con pasillo central.

    Ejemplo con ancho 5:
    LIBRE LIBRE LIBRE LIBRE LIBRE
    LIBRE PASILLO PASILLO PASILLO LIBRE
    LIBRE PASILLO PASILLO PASILLO LIBRE
    """
    print("\nAncho de la fila superior:")
    print("  1 - 3 plazas")
    print("  2 - 5 plazas")
    opcion_ancho = validar_entero("Seleccione una opción: ", 1, 2)
    ancho = 3 if opcion_ancho == 1 else 5
    centro = ancho - 2

    matriz = []
    plazas_creadas = 0

    # Fila superior horizontal (las esquinas quedan vacías porque
    # quedarían bloqueadas por los laterales cuando el parking está lleno)
    fila_top = []
    for i in range(ancho):
        if i == 0 or i == ancho - 1:
            fila_top.append(ESTADO_VACIO)
        elif plazas_creadas < cantidad_plazas:
            fila_top.append(ESTADO_LIBRE)
            plazas_creadas += 1
        else:
            fila_top.append(ESTADO_VACIO)
    matriz.append(fila_top)

    # Filas laterales: columna izquierda + pasillo central + columna derecha
    while plazas_creadas < cantidad_plazas:
        fila = []

        if plazas_creadas < cantidad_plazas:
            fila.append(ESTADO_LIBRE)
            plazas_creadas += 1
        else:
            fila.append(ESTADO_VACIO)

        for _ in range(centro):
            fila.append(ESTADO_PASILLO)

        if plazas_creadas < cantidad_plazas:
            fila.append(ESTADO_LIBRE)
            plazas_creadas += 1
        else:
            fila.append(ESTADO_VACIO)

        matriz.append(fila)

    return matriz


def generar_mapa_plazas(matriz):
    """
    Genera un diccionario que relaciona códigos de plaza con coordenadas reales.

    Ejemplo:
    {
        "P1": (0, 0),
        "P2": (0, 2),
        "P3": (1, 0)
    }
    """
    mapa_plazas = {}
    numero_plaza = 1

    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if (
                matriz[fila][columna] != ESTADO_PASILLO
                and matriz[fila][columna] != ESTADO_VACIO
            ):
                codigo = f"P{numero_plaza}"
                mapa_plazas[codigo] = (fila, columna)
                numero_plaza += 1

    return mapa_plazas


def mostrar_codigos_plazas(matriz):
    """
    Muestra el estacionamiento usando códigos de plaza.

    Las plazas reales se muestran como P1, P2, P3, etc.
    Los pasillos se muestran como PASILLO.
    Los espacios vacíos se muestran como VACIO.
    """
    mapa_plazas = generar_mapa_plazas(matriz)

    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            codigo_encontrado = None

            for codigo, coordenadas in mapa_plazas.items():
                if coordenadas == (fila, columna):
                    codigo_encontrado = codigo

            if codigo_encontrado is not None:
                print(codigo_encontrado, end=" ")
            else:
                print(matriz[fila][columna], end=" ")

        print()


def seleccionar_plaza_por_codigo(matriz):
    """
    Permite seleccionar una plaza ingresando un código como P1, P2 o P3.

    Retorna la fila y columna correspondiente.
    Si el código no existe, retorna None.
    """
    mapa_plazas = generar_mapa_plazas(matriz)

    print("\nCódigos de plazas disponibles:\n")
    mostrar_codigos_plazas(matriz)

    codigo = input("\nIngrese el código de plaza: ").upper().strip()

    if codigo not in mapa_plazas:
        print("El código de plaza ingresado no existe.")
        return None

    return mapa_plazas[codigo]


def registrar_ingreso_vehiculo(matriz, registros, historial):
    """
    Registra el ingreso de un vehículo a una plaza libre del estacionamiento.
    Valida que la patente no esté ya registrada, que la plaza exista y esté libre.
    """
    limpiar_pantalla()

    patente = input("\nIngrese la patente del vehículo: ").upper()

    if not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        return

    if patente in registros:
        print("Ese vehículo ya está en el estacionamiento.")
        return

    plaza = seleccionar_plaza_por_codigo(matriz)

    if plaza is None:
        return

    fila, columna = plaza

    if matriz[fila][columna] == ESTADO_RESERVADA:
        print("La plaza seleccionada está reservada.")
        return

    if matriz[fila][columna] != ESTADO_LIBRE:
        print("La plaza seleccionada está ocupada.")
        return

    tipo_vehiculo = (
        input("\nIngrese el tipo de vehículo (AUTO, MOTO O CAMIONETA): ")
        .upper()
        .strip()
    )

    while tipo_vehiculo not in TIPO_VEHICULO:
        print("Tipo inválido. Opciones válidas: AUTO, MOTO, CAMIONETA")
        tipo_vehiculo = (
            input("\nIngrese el tipo de vehículo (AUTO, MOTO o CAMIONETA): ")
            .upper()
            .strip()
        )

    matriz[fila][columna] = ESTADO_OCUPADO
    registros[patente] = {
        "patente": patente,
        "plaza": (fila, columna),
        "hora_ingreso": datetime.now(),
        "tipo_vehiculo": tipo_vehiculo,
        "estado": "OCUPADO",
    }

    historial.append(
        {
            "accion": "INGRESO",
            "patente": patente,
            "tipo_vehiculo": tipo_vehiculo,
            "plaza": (fila, columna),
            "fecha_hora": datetime.now(),
        }
    )

    print(
        f"\nIngreso registrado. Hora: {registros[patente]['hora_ingreso'].strftime('%H:%M:%S')}\n"
    )


def calcular_tiempo_estacionado(patente, registros):
    """
    Calcula y retorna el tiempo que lleva estacionado un vehículo.

    Recibe la patente del vehículo, busca su hora de ingreso en el
    diccionario de registros y calcula la diferencia con la hora actual.
    Retorna un objeto timedelta con el tiempo transcurrido, o None si
    la patente no tiene ingreso registrado.
    """

    if patente not in registros:
        return None

    hora_ingreso = registros[patente]["hora_ingreso"]
    hora_actual = datetime.now()
    tiempo = hora_actual - hora_ingreso

    return tiempo


def calcular_tarifa(tiempo, tipo_vehiculo):
    """
    Calcula y retorna la tarifa a cobrar según el tiempo estacionado.
    Recibe un objeto timedelta con el tiempo estacionado. Cobra una tarifa
    base por la primera hora y un valor adicional por cada
    fracción de hora. Retorna el monto total a pagar como número flotante.
    """

    TARIFA_BASE = 1000.0
    TARIFA_POR_FRACCION = 250.0

    total_segundos = int(tiempo.total_seconds())

    if total_segundos <= 3600:
        return TARIFA_BASE

    segundos_extra = total_segundos - 3600
    fracciones = math.ceil(segundos_extra / 900)
    multiplicador = MULTIPLICADORES_TARIFA[tipo_vehiculo]
    return TARIFA_BASE + (fracciones * TARIFA_POR_FRACCION) * multiplicador


def registrar_salida_vehiculo(matriz, registros, historial):
    """
    Registra la salida de un vehículo y libera su plaza en el estacionamiento.
    Calcula el tiempo estacionado y la tarifa a cobrar antes de liberar la plaza.
    Valida que la patente tenga ingreso registrado y busca su ubicación en la matriz.
    """
    limpiar_pantalla()

    mostrar_estacionamiento(matriz)

    patente = input("\nIngrese la patente del vehículo: ").upper()

    if not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        return

    if patente not in registros:
        print("Ese vehículo no tiene ingreso registrado.")
        return

    fila, columna = registros[patente]["plaza"]

    tiempo = calcular_tiempo_estacionado(patente, registros)
    tarifa = calcular_tarifa(tiempo, registros[patente]["tipo_vehiculo"])

    horas = int(tiempo.total_seconds() // 3600)
    minutos = int((tiempo.total_seconds() % 3600) // 60)
    segundos = int(tiempo.total_seconds() % 60)

    print(f"Patente:            {patente}")
    print(
        f"Hora de ingreso:    {registros[patente]['hora_ingreso'].strftime('%H:%M:%S')}"
    )
    print(f"Hora de salida:     {datetime.now().strftime('%H:%M:%S')}")
    print(f"Tiempo estacionado: {horas}h {minutos}m {segundos}s")
    print(f"Tarifa a cobrar:    ${tarifa:.2f}")

    historial.append(
        {
            "accion": "EGRESO",
            "patente": patente,
            "tipo_vehiculo": registros[patente]["tipo_vehiculo"],
            "plaza": (fila, columna),
            "hora_ingreso": registros[patente]["hora_ingreso"],
            "hora_salida": datetime.now(),
            "tiempo_estacionado": f"{horas}h {minutos}m {segundos}s",
            "tarifa": tarifa,
        }
    )

    matriz[fila][columna] = ESTADO_LIBRE
    del registros[patente]


def buscar_vehiculo(matriz, registros):
    """
    Busca un vehículo por patente dentro del estacionamiento.
    Si lo encuentra, muestra la fila y la columna en la que está ubicado.
    """
    limpiar_pantalla()

    patente = input("\nIngrese la patente a buscar: ").upper()

    if not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        return

    if patente not in registros:
        print("El vehículo no se encuentra en el estacionamiento.")
        return

    fila, columna = registros[patente]["plaza"]
    mapa_plazas = generar_mapa_plazas(matriz)
    codigo_plaza = None

    for codigo, coordenadas in mapa_plazas.items():
        if coordenadas == (fila, columna):
            codigo_plaza = codigo

    print(f"\nVehículo encontrado en la plaza {codigo_plaza}.")
    print(f"Hora de ingreso del vehículo: {registros[patente]['hora_ingreso']}")
    print(f"Tipo de vehículo: {registros[patente]['tipo_vehiculo']}")
    print(f"Estado del vehículo: {registros[patente]['estado']}")


def modificar_estacionamiento(matriz, registros, reservas):
    """
    Permite recrear el estacionamiento con un nuevo tipo o número de plazas.
    Bloquea la operación si hay vehículos actualmente estacionados.
    Advierte si hay reservas activas, ya que sus coordenadas
    quedarán inválidas.
    """
    limpiar_pantalla()

    if registros:
        print("\nNo se puede modificar el estacionamiento "
              "mientras hay vehículos estacionados.")
        print(f"Vehículos actualmente estacionados: {len(registros)}")
        return

    reservas_activas = [r for r in reservas if r["estado"] == "ACTIVA"]
    if reservas_activas:
        print(f"\nAtención: hay {len(reservas_activas)} reserva(s) activa(s).")
        print("Si modifica el estacionamiento, las reservas activas "
              "quedarán con coordenadas inválidas.")
        confirmacion = input(
            "¿Desea continuar de todas formas? (S/N): "
        ).upper().strip()
        if confirmacion != "S":
            print("Modificación cancelada.")
            return

    nueva_matriz = crear_estacionamiento()

    if nueva_matriz is None:
        return

    matriz.clear()
    matriz.extend(nueva_matriz)

    print("\nEstacionamiento modificado correctamente.")
    mostrar_estacionamiento(matriz)


def modificar_estado_plaza(matriz, registros):
    """
    Modifica el estado o patente de una plaza específica en el estacionamiento.
    Permite cambiar la patente (actualizando registros de ingreso) o el estado general.
    """
    limpiar_pantalla()

    print("\nIndique la plaza a modificar.")

    plaza = seleccionar_plaza_por_codigo(matriz)

    if plaza is None:
        return

    fila, columna = plaza

    estado_actual = matriz[fila][columna]

    if estado_actual == ESTADO_PASILLO or estado_actual == ESTADO_VACIO:
        print("La posición seleccionada no es una plaza modificable.")
        return

    if estado_actual == ESTADO_LIBRE:
        print("La plaza está libre, no hay registro para modificar.")
        return

    if estado_actual == ESTADO_OCUPADO:
        patente_actual = None
        for pat, datos in registros.items():
            if datos["plaza"] == (fila, columna):
                patente_actual = pat
                break
        if patente_actual is None:
            print("No se encontró registro para esta plaza.")
            return
    else:
        patente_actual = estado_actual

    while True:
        lista_modificar_estado_plaza()

        opcion = validar_entero("Seleccione la modificación a realizar: ", 1, 4)

        match opcion:
            case 1:
                nueva_patente = (
                    input("Ingrese nueva patente (deje vacío para liberar plaza): ")
                    .upper()
                    .strip()
                )

                if nueva_patente == "":
                    if patente_actual in registros:
                        del registros[patente_actual]
                    matriz[fila][columna] = ESTADO_LIBRE
                    print("Plaza liberada correctamente")
                    return

                if not validar_patente(nueva_patente):
                    print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
                    return

                if nueva_patente in registros and nueva_patente != patente_actual:
                    print("Esa patente ya está registrada en el estacionamiento.")
                    continue

                if patente_actual in registros:
                    registros[nueva_patente] = registros.pop(patente_actual)
                    registros[nueva_patente]["patente"] = nueva_patente

                matriz[fila][columna] = nueva_patente
                patente_actual = nueva_patente
                print(f"Patente modificada correctamente a {nueva_patente}.")

            case 2:
                nuevo_tipo = (
                    input("\nIngrese el tipo de vehículo (AUTO, MOTO O CAMIONETA): ")
                    .upper()
                    .strip()
                )
                if nuevo_tipo not in TIPO_VEHICULO:
                    print("Tipo invalido. Opciones validas: AUTO, MOTO, CAMIONETA")
                    continue

                if patente_actual in registros:
                    registros[patente_actual]["tipo_vehiculo"] = nuevo_tipo
                print("Tipo de vehículo modificado correctamente.")

            case 3:
                nuevo_estado = (
                    input("Ingrese el nuevo estado (LIBRE u OCUPADO): ").upper().strip()
                )

                if nuevo_estado not in ["LIBRE", "OCUPADO"]:
                    print("Estado no válido. Solo se permite LIBRE u OCUPADO.")
                    continue

                if nuevo_estado == "LIBRE":
                    if patente_actual in registros:
                        del registros[patente_actual]
                    matriz[fila][columna] = ESTADO_LIBRE
                    print("Plaza liberada correctamente.")
                    return
                else:
                    if patente_actual in registros:
                        registros[patente_actual]["estado"] = nuevo_estado
                    print(f"Estado modificado correctamente a {nuevo_estado}.")

            case 4:
                break
            
            case _:
                print("Opción inválida.")

def login(admin):
    if admin is None:
        usuario = input("Ingrese su nuevo usuario: ")
        clave = input("Ingrese su nueva clave: ")
        admin = {
        "usuario": usuario,
        "clave": clave
        }
        return admin
    else:
        while True:
            usuario = input("Ingrese su usuario: ")
            clave = input("Ingrese su clave: ")
            if usuario == admin["usuario"] and clave == admin["clave"]:
                return admin
            else:
                print("Credenciales incorrectas. Intente de nuevo.")