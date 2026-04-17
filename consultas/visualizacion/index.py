from functools import reduce
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
    matriz_plana = [col for fila in matriz for col in fila]
    return reduce(lambda acc, col: acc + (1 if col != "LIBRE" else 0), matriz_plana, 0)

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
    matriz_plana = [col for fila in matriz for col in fila]
    return reduce(lambda acc, col: acc + (0 if col != "LIBRE" else 1), matriz_plana, 0)

def mostrar_placas_disponibles(matriz):
    """
    Muestra por pantalla el número de plazas disponibles.
    """
    disponibles = contar_placas_disponibles(matriz)
    print(f"\nPlacas disponibles: {disponibles}")