from consultas.validacion.index import validar_patente
from consultas.visualizacion.index import mostrar_estacionamiento
from ui.index import limpiar_pantalla
from datetime import datetime

registros = {}


def crear_estacionamiento():
    """
    Crea y retorna una matriz que representa un estacionamiento.

    Solicita al usuario el número de filas y columnas mediante entrada estándar,
    luego construye una matriz bidimensional donde cada celda está inicializada
    con el valor "LIBRE", indicando que todos los espacios están disponibles.
    """
    limpiar_pantalla()
    
    print("\nIngrese las filas y columnas del estacionamiento: \n")

    filas = int(input("Filas: "))
    columnas = int(input("Columnas: "))

    matriz = []

    for fila in range(filas):
        matriz.append([])
        for columna in range(columnas):
            matriz[fila].append("LIBRE")

    return matriz


def registrar_ingreso_vehiculo(matriz):
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

    fila = int(input("Ingrese fila de la plaza: ")) - 1
    columna = int(input("Ingrese columna de la plaza: ")) - 1

    if fila < 0 or fila >= len(matriz) or columna < 0 or columna >= len(matriz[0]):
        print("La plaza no existe.")
        return

    if matriz[fila][columna] != "LIBRE":
        print("La plaza está ocupada.")
        return

    matriz[fila][columna] = patente
    registros[patente] = datetime.now()

    print(f"\nIngreso registrado. Hora: {registros[patente].strftime('%H:%M:%S')}\n")


def calcular_tiempo_estacionado(patente):
    """
    Calcula y retorna el tiempo que lleva estacionado un vehículo.

    Recibe la patente del vehículo, busca su hora de ingreso en el
    diccionario de registros y calcula la diferencia con la hora actual.
    Retorna un objeto timedelta con el tiempo transcurrido, o None si
    la patente no tiene ingreso registrado.
    """

    if patente not in registros:
        return None

    hora_ingreso = registros[patente]
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

    TARIFA_BASE = 1000.0        # Precio por la primera hora
    TARIFA_POR_HORA = 500.0    # Precio por cada hora adicional o fracción

    total_segundos = tiempo.total_seconds()
    horas = total_segundos / 3600

    if horas <= 1:
        return TARIFA_BASE

    horas_extra = horas - 1
    import math
    horas_extra_enteras = math.ceil(horas_extra)

    tarifa = TARIFA_BASE + (horas_extra_enteras * TARIFA_POR_HORA)

    return tarifa


def registrar_salida_vehiculo(matriz):
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

    fila_encontrada = -1
    columna_encontrada = -1

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == patente:
                fila_encontrada = i
                columna_encontrada = j

    if fila_encontrada == -1:
        print("No se encontró el vehículo en el estacionamiento.")
        return

    tiempo = calcular_tiempo_estacionado(patente)
    tarifa = calcular_tarifa(tiempo)

    horas = int(tiempo.total_seconds() // 3600)
    minutos = int((tiempo.total_seconds() % 3600) // 60)
    segundos = int(tiempo.total_seconds() % 60)

    print(f"Patente:            {patente}")
    print(f"Hora de ingreso:    {registros[patente].strftime('%H:%M:%S')}")
    print(f"Hora de salida:     {datetime.now().strftime('%H:%M:%S')}")
    print(f"Tiempo estacionado: {horas}h {minutos}m {segundos}s")
    print(f"Tarifa a cobrar:    ${tarifa:.2f}")

    matriz[fila_encontrada][columna_encontrada] = "LIBRE"
    del registros[patente]


def buscar_vehiculo(matriz):
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
                print(f"Vehículo encontrado en fila {i + 1}, columna {j + 1}.")
                return

    print("El vehículo no se encuentra en el estacionamiento.")

def modificar_estado_plaza(matriz):
    """
    Modifica el estado o patente de una plaza específica en el estacionamiento.
    Permite cambiar la patente (actualizando registros de ingreso) o el estado general.
    """
    limpiar_pantalla()
    
    print("\nIndique la fila y columna de la plaza a modificar ")
    fila = int(input("\nIngrese fila de la plaza: ")) - 1
    columna = int(input("Ingrese columna de la plaza: ")) - 1
    
    if fila < 0 or fila >= len(matriz) or columna < 0 or columna >= len(matriz[0]):
        print("La plaza no existe.")
        return
    
    while True:
        print("\nModificaciones:")
        print("  1 - Cambiar patente")
        print("  2 - Cambiar estado")
        print("  3 - Volver")

        opcion = int(input("Seleccione la modificación a realizar: "))

        if opcion == 1:
            nueva_patente = input("Ingrese nueva patente (deje vacío para liberar plaza): ").upper().strip()
            
            if not validar_patente(nueva_patente):
                print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
                return
            
            estado_anterior = matriz[fila][columna]

            if estado_anterior in registros:
                del registros[estado_anterior]
                
            if nueva_patente:
                if nueva_patente in registros:
                    print("Esa patente ya está registrada en el estacionamiento.")
                    continue
                matriz[fila][columna] = nueva_patente
                registros[nueva_patente] = datetime.now()
                print(f"Patente cambiada a {nueva_patente}. Ingreso registrado.")
            else:
                matriz[fila][columna] = "LIBRE"
                print("Plaza liberada.")

        elif opcion == 2:
            nuevo_estado = input("Ingrese el nuevo estado (LIBRE, OCUPADO, etc.): ").upper().strip()
            if nuevo_estado:
                if nuevo_estado == "LIBRE" and matriz[fila][columna] in registros:
                    del registros[matriz[fila][columna]]
                matriz[fila][columna] = nuevo_estado
                print(f"Estado cambiado a {nuevo_estado}.")
            else:
                print("Estado no válido.")

        elif opcion == 3:
            break
        else:
            print("Opción no válida. Intente nuevamente.")
