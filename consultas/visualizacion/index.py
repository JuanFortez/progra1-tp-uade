from ui.index import limpiar_pantalla

def mostrar_estacionamiento(matriz):
    """
    Muestra el estado actual del estacionamiento en formato de grilla.
    """
    limpiar_pantalla()
    
    print("")
    for fila in matriz:
        for valor in fila:
            print(valor, end=" ")
        print()
    
    mostrar_placas_ocupadas(matriz)
    mostrar_placas_disponibles(matriz)
        

def contar_placas_ocupadas(matriz):
    """
    Cuenta y retorna el número de plazas ocupadas en el estacionamiento.
    """
    contador = 0
    for fila in matriz:
        for columna in fila:
            if columna != "LIBRE":
                contador = contador + 1
    return contador

def mostrar_placas_ocupadas(matriz):
    """
    Muestra por pantalla el número de plazas ocupadas.
    """
    ocupadas = contar_placas_ocupadas(matriz)
    print(f"\nPlacas ocupadas: {ocupadas}")

def contar_placas_disponibles(matriz):
    """
    Cuenta y retorna el número de plazas libres en el estacionamiento.
    """
    contador = 0
    for fila in matriz:
        for columna in fila:
            if columna == "LIBRE":
                contador = contador + 1
    return contador

def mostrar_placas_disponibles(matriz):
    """
    Muestra por pantalla el número de plazas disponibles.
    """
    disponibles = contar_placas_disponibles(matriz)
    print(f"\nPlacas disponibles: {disponibles}")