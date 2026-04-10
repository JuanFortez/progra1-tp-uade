from consultas.visualizacion.index import mostrar_estacionamiento

def crear_estacionamiento():
    
    print("\nIngrese las filas y columnas del estacionamiento: \n")
    
    filas = int(input("Filas: "))
    columnas = int(input("Columnas: "))
    
    matriz = []
    
    for fila in range(filas):
        matriz.append([])
        for columna in range(columnas):
            matriz[fila].append("LIBRE")
    
    return matriz

def agregar_vehiculo_plaza(matriz):

    patente = input("\nIngrese la patente del vehículo: ").upper()

    fila = int(input("Ingrese fila: ")) - 1
    columna = int(input("Ingrese columna: ")) - 1

    if fila < 0 or fila >= len(matriz) or columna < 0 or columna >= len(matriz[0]):
        print("La plaza no existe")
        return

    if matriz[fila][columna] != "LIBRE":
        print("La plaza está ocupada")
        return

    matriz[fila][columna] = patente

    print("\nVehículo agregado correctamente\n")
    
    