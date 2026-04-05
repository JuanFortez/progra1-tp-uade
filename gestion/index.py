

def crear_matriz_estacionamiento():
    
    print("\nIngrese las filas y columnas del estacionamiento: \n")
    
    filas = int(input("Filas: "))
    columnas = int(input("Columnas: "))
    
    matriz = []
    
    for fila in range(filas):
        matriz.append([])
        for columna in range(columnas):
            matriz[fila].append(0)
    
    return matriz