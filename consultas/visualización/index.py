
def mostrar_estacionamiento(matriz):
    for fila in matriz:
        for valor in fila:
            print(valor, end=" ")
        print()
        

def contar_placas_ocupadas(matriz):
    contador = 0
    for fila in matriz:
        for columna in fila:
            if columna != "LIBRE":
                contador = contador + 1
    return contador

def mostrar_placas_ocupadas(matriz):
    ocupadas = contar_placas_ocupadas(matriz)
    print(f"Placas ocupadas: {ocupadas}")

def contar_placas_disponibles(matriz):
    contador = 0
    for fila in matriz:
        for columna in fila:
            if columna == "LIBRE":
                contador = contador + 1
    return contador

def mostrar_placas_disponibles(matriz):
    disponibles = contar_placas_disponibles(matriz)
    print(f"Placas disponibles: {disponibles}")