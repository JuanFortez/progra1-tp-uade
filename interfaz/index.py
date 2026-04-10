from gestion.index import crear_estacionamiento, agregar_vehiculo_plaza
from consultas.visualizacion.index import mostrar_estacionamiento, mostrar_placas_disponibles, mostrar_placas_ocupadas

def interfaz_inicio():
    print("=" * 50)
    print(" " * 5 + "Bienvenido al sistema de Parking Control")
    print("=" * 50)
    
    matriz = crear_estacionamiento()
    mostrar_estacionamiento(matriz)
    agregar_vehiculo_plaza(matriz)
    mostrar_placas_ocupadas(matriz)
    mostrar_placas_disponibles(matriz)