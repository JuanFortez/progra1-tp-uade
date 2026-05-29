from functools import reduce
from ui.index import limpiar_pantalla
from consultas.constantes.index import ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_VACIO, ESTADO_RESERVADA

def mostrar_estacionamiento(matriz):
    """
    Muestra el estado actual del estacionamiento en formato de grilla.
    """
    limpiar_pantalla()

    print("")

    for fila in matriz:
        for valor in fila:
            if valor == ESTADO_LIBRE:
                print("🟩", end=" ")
            elif valor == ESTADO_PASILLO:
                print(" ", end=" ")
            elif valor == ESTADO_VACIO:
                print("  ", end=" ")
            elif valor == ESTADO_RESERVADA:
                print("🟧", end=" ")
            else:
                print("🟥", end=" ")
        print()

    print("\nLeyenda: 🟩 Libre  🟥 Ocupada  🟧 Reservada  ⬛ Pasillo")
    mostrar_plazas_ocupadas(matriz)
    mostrar_plazas_disponibles(matriz)

def es_plaza_real(valor):
    """
    Indica si una celda de la matriz representa una plaza real del estacionamiento.

    No son plazas reales:
    - PASILLO
    - VACIO

    Sí son plazas reales:
    - LIBRE
    - Una patente registrada
    """
    return valor != ESTADO_PASILLO and valor != ESTADO_VACIO


def contar_plazas_ocupadas(matriz):
    """
    Cuenta y retorna el número de plazas ocupadas en el estacionamiento.
    """
    matriz_plana = [col for fila in matriz for col in fila]

    return reduce(
        lambda acc, col: acc + (1 if es_plaza_real(col) and col != ESTADO_LIBRE else 0),
        matriz_plana,
        0,
    )


def mostrar_plazas_ocupadas(matriz):
    """
    Muestra por pantalla el número de plazas ocupadas.
    """
    ocupadas = contar_plazas_ocupadas(matriz)
    print(f"\nPlacas ocupadas: {ocupadas}")


def contar_plazas_disponibles(matriz):
    """
    Cuenta y retorna el número de plazas libres en el estacionamiento.
    """
    matriz_plana = [col for fila in matriz for col in fila]

    return reduce(
        lambda acc, col: acc + (1 if col == ESTADO_LIBRE else 0), matriz_plana, 0
    )


def mostrar_plazas_disponibles(matriz):
    """
    Muestra por pantalla el número de plazas disponibles.
    """
    disponibles = contar_plazas_disponibles(matriz)
    print(f"\nPlacas disponibles: {disponibles}")
