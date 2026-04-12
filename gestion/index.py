from consultas.visualización.index import mostrar_estacionamiento
from datetime import datetime

registros = {}

def crear_estacionamiento():
    """
    Crea y retorna una matriz que representa un estacionamiento.

    Solicita al usuario el número de filas y columnas mediante entrada estándar,
    luego construye una matriz bidimensional donde cada celda está inicializada
    con el valor "LIBRE", indicando que todos los espacios están disponibles.
    """
    
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

    patente = input("\nIngrese la patente del vehículo: ").upper()

    if patente in registros:
        print("Ese vehículo ya está en el estacionamiento.")
        return

    fila = int(input("Ingrese fila de la plaza: ")) - 1
    columna = int(input("Ingrese columna de la plaza: ")) - 1

    if fila < 0 or fila >= len(matriz) or columna < 0 or columna >= len(matriz[0]):
        print("La plaza no existe.")
        return

    if matriz[fila - 1][columna - 1] != "LIBRE":
        print("La plaza está ocupada.")
        return

    matriz[fila][columna] = patente
    registros[patente] = datetime.now()

    print(f"\nIngreso registrado. Hora: {registros[patente].strftime('%H:%M:%S')}\n")


def registrar_salida_vehiculo(matriz):
    """
    Registra la salida de un vehículo y libera su plaza en el estacionamiento.
    Valida que la patente tenga ingreso registrado y busca su ubicación en la matriz.
    """

    patente = input("\nIngrese la patente del vehículo: ").upper()

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

    matriz[fila_encontrada][columna_encontrada] = "LIBRE"
    del registros[patente]