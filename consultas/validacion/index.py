import re


def validar_patente(patente):
    patron_viejo = r"^[A-Z]{3}\d{3}$"  # ABC123
    patron_nuevo = r"^[A-Z]{2}\d{3}[A-Z]{2}$"  # AB123CD
    return re.match(patron_viejo, patente) or re.match(patron_nuevo, patente)


const_meses = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


def año_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)


def dia_valido(dia, mes, anio):
    meses = const_meses.copy()

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
