from datetime import datetime
from consultas.validacion.index import validar_entero, validar_patente
from consultas.visualizacion.index import mostrar_estacionamiento
from ui.index import limpiar_pantalla

tipos_validos = {"AUTO", "MOTO", "CAMIONETA"}

def crear_estacionamiento():
    """
    Crea y retorna una matriz que representa un estacionamiento.

    Solicita al usuario el número de filas y columnas mediante entrada estándar,
    luego construye una matriz bidimensional donde cada celda está inicializada
    con el valor "LIBRE", indicando que todos los espacios están disponibles.
    """
    limpiar_pantalla()

    print("\nIngrese las filas y columnas del estacionamiento: \n")

    filas = validar_entero("Filas: ", 1)
    columnas = validar_entero("Columnas: ", 1)

    matriz = []

    for fila in range(filas):
        matriz.append([])
        for columna in range(columnas):
            matriz[fila].append("LIBRE")

    return matriz


def registrar_ingreso_vehiculo(matriz, registros):
    """
    Registra el ingreso de un vehículo a una plaza libre del estacionamiento.
    Valida que la patente no esté ya registrada, que la plaza exista y esté libre.
    """
    limpiar_pantalla()

    mostrar_estacionamiento(matriz)

    patente = input("\nIngrese la patente del vehículo: ").upper()

    if not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        return

    if patente in registros:
        print("Ese vehículo ya está en el estacionamiento.")
        return

    fila = validar_entero("Ingrese fila de la plaza: ", 1, len(matriz)) - 1
    columna = validar_entero("Ingrese columna de la plaza: ", 1, len(matriz[0])) - 1

    if matriz[fila][columna] != "LIBRE":
        print("La plaza está ocupada.")
        return

    tipo = input("\nIngrese el tipo de vehículo (AUTO, MOTO O CAMIONETA): ").upper().strip()

    while tipo not in tipos_validos:
        print("Tipo inválido. Opciones válidas: AUTO, MOTO, CAMIONETA")
        tipo = input("\nIngrese el tipo de vehículo (AUTO, MOTO o CAMIONETA): ").upper().strip()

    matriz[fila][columna] = patente
    registros[patente] = {
        "patente": patente,
        "plaza": (fila, columna),
        "hora_ingreso": datetime.now(),
        "tipo": tipo,
        "estado": "OCUPADO"
    }

    print(f"\nIngreso registrado. Hora: {registros[patente]["hora_ingreso"].strftime('%H:%M:%S')}\n")


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

    hora_ingreso = registros[patente]['hora_ingreso']
    hora_actual = datetime.now()
    tiempo = hora_actual - hora_ingreso

    return tiempo


def calcular_tarifa(tiempo):
    """
    Calcula y retorna la tarifa a cobrar según el tiempo estacionado.

    Recibe un objeto timedelta con el tiempo estacionado. Cobra una tarifa
    base por la primera hora y un valor adicional por cada hora extra o
    fracción. Retorna el monto total a pagar como número flotante.
    """

    TARIFA_BASE = 1000.0  # Precio por la primera hora
    TARIFA_POR_HORA = 500.0  # Precio por cada hora adicional o fracción

    total_segundos = tiempo.total_seconds()
    horas = total_segundos / 3600

    if horas <= 1:
        return TARIFA_BASE

    horas_extra = horas - 1
    import math

    horas_extra_enteras = math.ceil(horas_extra)

    tarifa = TARIFA_BASE + (horas_extra_enteras * TARIFA_POR_HORA)

    return tarifa


def registrar_salida_vehiculo(matriz, registros):
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
    tarifa = calcular_tarifa(tiempo)

    horas = int(tiempo.total_seconds() // 3600)
    minutos = int((tiempo.total_seconds() % 3600) // 60)
    segundos = int(tiempo.total_seconds() % 60)

    print(f"Patente:            {patente}")
    print(f"Hora de ingreso:    {registros[patente]['hora_ingreso'].strftime('%H:%M:%S')}")
    print(f"Hora de salida:     {datetime.now().strftime('%H:%M:%S')}")
    print(f"Tiempo estacionado: {horas}h {minutos}m {segundos}s")
    print(f"Tarifa a cobrar:    ${tarifa:.2f}")

    matriz[fila][columna] = "LIBRE"
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

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == patente:
                print(f"\nVehículo encontrado en fila {i + 1}, columna {j + 1}.")
                if patente in registros:
                    print(f"Hora de ingreso del vehículo: {registros[patente]['hora_ingreso']}")
                    print(f"Tipo de vehículo: {registros[patente]["tipo"]}")
                    print(f"Estado del vehículo: {registros[patente]["estado"]}")
                return

    print("El vehículo no se encuentra en el estacionamiento.")


def modificar_estado_plaza(matriz, registros):
    """
    Modifica el estado o patente de una plaza específica en el estacionamiento.
    Permite cambiar la patente (actualizando registros de ingreso) o el estado general.
    """
    limpiar_pantalla()

    print("\nIndique la fila y columna de la plaza a modificar ")

    fila = validar_entero("\nIngrese fila de la plaza: ", 1, len(matriz)) - 1
    columna = validar_entero("Ingrese columna de la plaza: ", 1, len(matriz[0])) - 1
    
    patente_actual = matriz[fila][columna]

    if patente_actual == "LIBRE":
        print("La plaza está libre, no hay registro para modificar.")
        return
    
    while True:
        print("\nModificaciones:")
        print("  1 - Cambiar patente")
        print("  2 - Cambiar tipo de vehículo")
        print("  3 - Cambiar estado")
        print("  4 - Volver")

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
                    matriz[fila][columna] = "LIBRE"
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
                nuevo_tipo = input("\nIngrese el tipo de vehículo (AUTO, MOTO O CAMIONETA): ").upper().strip()
                if patente_actual in registros:
                    registros[patente_actual]["tipo"] = nuevo_tipo
                print("Tipo de vehículo modificado correctamente.")
                
            case 3:
                nuevo_estado = (
                    input("Ingrese el nuevo estado (LIBRE u OCUPADO): ").upper().strip()
                )

                if nuevo_estado not in ["LIBRE", "OCUPADO"]:
                    print("Estado no válido. Solo se permite LIBRE u OCUPADO.")
                    continue

                if matriz[fila][columna] in registros:
                    del registros[matriz[fila][columna]]

                if patente_actual in registros:
                    registros[patente_actual]["estado"] = nuevo_estado
                    
                print(f"Estado modificado correctamente a {nuevo_estado}.")

            case 4:
                break
