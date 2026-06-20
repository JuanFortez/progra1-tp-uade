from functools import reduce
from ui.index import limpiar_pantalla
from consultas.constantes.index import ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_VACIO, ESTADO_RESERVADA, ESTADO_OCUPADO

def mostrar_estacionamiento(matriz):
    """
    Muestra el estado actual del estacionamiento en formato de grilla,
    con encabezados de columna (A, B, C, ...) y filas etiquetadas como
    Fila-1, Fila-2, etc. Las columnas sin ninguna plaza real (pasillos
    o espacios vacíos en toda su extensión) no muestran letra.
    """
    limpiar_pantalla()
 
    print("")
 
    if not matriz:
        print("El estacionamiento no tiene plazas configuradas.")
        return
 
    letras_columnas = generar_letras_columnas(matriz)
 
    mostrar_encabezado_columnas(matriz, letras_columnas)
 
    for indice_fila, fila in enumerate(matriz, start=1):
        linea = f"Fila-{indice_fila}:".ljust(9)
 
        for valor in fila:
            linea += f" {valor} "
 
        print(linea)
 
    print("\nLeyenda: ⬜️ Libre  🟥 Ocupada  🟧 Reservada")
    mostrar_plazas_ocupadas(matriz)
    mostrar_plazas_disponibles(matriz)
    mostrar_alerta_ocupacion(matriz)

def obtener_columnas_con_plaza(matriz):
    """
    Determina qué columnas de la matriz contienen al menos una plaza real
    (no PASILLO ni VACIO) en alguna de sus filas.
 
    Retorna una lista de índices de columna que tienen alguna plaza real.
    """
    if not matriz:
        return []
 
    cantidad_columnas = max(len(fila) for fila in matriz)
    columnas_con_plaza = []
 
    for columna in range(cantidad_columnas):
        tiene_plaza = False
 
        for fila in matriz:
            if columna < len(fila) and es_plaza_real(fila[columna]):
                tiene_plaza = True
                break
 
        if tiene_plaza:
            columnas_con_plaza.append(columna)
 
    return columnas_con_plaza

def generar_letras_columnas(matriz):
    """
    Genera un diccionario que asocia cada índice de columna con su letra
    correspondiente (A, B, C, ...), pero solo para aquellas columnas que
    contienen al menos una plaza real.
 
    Las columnas que son enteramente PASILLO o VACIO no reciben letra.
    """
    columnas_con_plaza = obtener_columnas_con_plaza(matriz)
    letras_columnas = {}
 
    for indice, columna in enumerate(columnas_con_plaza):
        letras_columnas[columna] = chr(ord("A") + indice)
 
    return letras_columnas

def mostrar_encabezado_columnas(matriz, letras_columnas):
    """
    Imprime la fila de encabezado con las letras de columna, dejando en
    blanco las columnas que no tienen ninguna plaza real.
    """
    cantidad_columnas = max(len(fila) for fila in matriz)
 
    encabezado = "Columnas:".ljust(9)
 
    for columna in range(cantidad_columnas):
        letra = letras_columnas.get(columna, " ")
        encabezado += f" {letra}  "
 
    print(encabezado)

def es_plaza_real(valor):
    """
    Indica si una celda de la matriz representa una plaza real del estacionamiento.

    No son plazas reales:
    - PASILLO
    - VACIO

    Sí son plazas reales:
    - LIBRE
    - OCUPADO / RESERVADA
    - Una patente registrada
    """
    return valor != ESTADO_PASILLO and valor != ESTADO_VACIO


def contar_plazas_ocupadas(matriz):
    """
    Cuenta y retorna el número de plazas ocupadas en el estacionamiento.
    """
    matriz_plana = [col for fila in matriz for col in fila]

    return reduce(
        lambda acc, col: acc + (1 if col == ESTADO_OCUPADO else 0),
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

def contar_plazas_reales(matriz):
    """Cuenta las plazas reales del estacionamiento."""
    total = 0

    for fila in matriz:
        for celda in fila:
            if es_plaza_real(celda):
                total += 1

    return total


def calcular_porcentaje_ocupacion(matriz):
    """Calcula el porcentaje de ocupación actual."""
    total_plazas = contar_plazas_reales(matriz)

    if total_plazas == 0:
        return 0

    ocupadas = contar_plazas_ocupadas(matriz)
    porcentaje = (ocupadas / total_plazas) * 100

    return porcentaje


def mostrar_alerta_ocupacion(matriz):
    """Muestra una advertencia si la ocupación supera el 80%."""
    porcentaje = calcular_porcentaje_ocupacion(matriz)

    if porcentaje > 80:
        print("\nATENCIÓN: el estacionamiento supera el 80% de ocupación.")
        print(f"Ocupación actual: {porcentaje:.1f}%")
