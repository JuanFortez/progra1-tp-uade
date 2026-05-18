import re
from constantes.index import PREFIJOS_PREFIJOS, MESES

def validar_patente(patente):
    patron_viejo = r"^[A-Z]{3}\d{3}$"  # ABC123
    patron_nuevo = r"^[A-Z]{2}\d{3}[A-Z]{2}$"  # AB123CD
    return re.match(patron_viejo, patente) or re.match(patron_nuevo, patente)

def validar_telefono(numero):
    """
    Valida números argentinos:
    - Solo dígitos
    - Sin +54
    - Sin 15
    - Prefijo válido
    """

    prefijos = "|".join(sorted(PREFIJOS_PREFIJOS, key=len, reverse=True))

    patron = rf"^({prefijos})(?!15)\d{{6,8}}$"

    return re.match(patron, numero.strip()) is not None

def validar_dni(dni):
    '''
    Valida DNI formato argentino
    - Solo números
    - Permite puntos
    - Permite formato viejo de 7 dígitos
    '''
    return re.match(r'^\d{7,8}$', dni.replace('.', '').strip())


def año_bisiesto(anio):
    """
    Devuelve si un año es bisiesto o no.
    """
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)


def dia_valido(dia, mes, anio):
    """
    Devuelve la cantidad de dias por mes.
    """
    meses = MESES.copy()

    if año_bisiesto(anio):
        meses[2] = 29

    return 1 <= dia <= meses[mes]


def validar_fecha(fecha):
    """
    Valida que la fecha tenga formato AAAA-MM-DD.
    Retorna True si es válida, False si no.
    """
    patron = r"^\d{4}-\d{2}-\d{2}$"

    if re.match(patron, fecha) is None:
        return False

    anio, mes, dia = fecha.split("-")

    anio = int(anio)
    mes = int(mes)
    dia = int(dia)

    if mes < 1 or mes > 12:
        return False

    if not dia_valido(dia, mes, anio):
        return False

    return True


def validar_entero(mensaje, minimo=None, maximo=None):
    """
    Solicita un número entero al usuario y valída opcionalmente
    si se encuentra dentro de un rango.
    """

    while True:
        entrada = input(mensaje).strip()

        if not entrada.isdigit():
            print("Debe ingresar un número entero válido.")
            continue

        numero = int(entrada)

        if minimo is not None and numero < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue

        if maximo is not None and numero > maximo:
            print(f"El valor debe ser menos o igual a {maximo}.")
            continue

        return numero
