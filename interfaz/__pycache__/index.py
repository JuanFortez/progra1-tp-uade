from gestion.index import crear_estacionamiento, agregar_vehiculo_plaza
from consultas.visualización.index import mostrar_estacionamiento


def interfaz_inicio():
    print("=" * 50)
    print(" " * 5 + "Bienvenido al sistema de Parking Control")
    print("=" * 50)

    matriz = crear_estacionamiento()
    mostrar_estacionamiento(matriz)
    agregar_vehiculo_plaza(matriz)
    reservas = []
