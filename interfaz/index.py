from gestion.index import crear_estacionamiento, agregar_vehiculo_plaza
<<<<<<< HEAD
from consultas.visualizacion.index import mostrar_estacionamiento
=======
from consultas.visualización.index import mostrar_estacionamiento
>>>>>>> 75659ea0ab4a25c1a718a026bc39a33c65e1268e


def interfaz_inicio():
    print("=" * 50)
    print(" " * 5 + "Bienvenido al sistema de Parking Control")
    print("=" * 50)

    matriz = crear_estacionamiento()
    mostrar_estacionamiento(matriz)
<<<<<<< HEAD
    agregar_vehiculo_plaza(matriz)
=======
    agregar_vehiculo_plaza(matriz)
    reservas = []
>>>>>>> 75659ea0ab4a25c1a718a026bc39a33c65e1268e
