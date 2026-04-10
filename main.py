from interfaz.index import interfaz_inicio
from consultas.visualizacion.index import mostrar_placas_disponibles
from gestion.index import crear_estacionamiento

def main():
    matriz = crear_estacionamiento()
    interfaz_inicio()
    mostrar_placas_disponibles(matriz)
    
if __name__ == "__main__":
    main()