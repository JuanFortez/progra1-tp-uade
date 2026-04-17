import re


def validar_patente(patente):
    patron_viejo = r"^[A-Z]{3}\d{3}$"  # ABC123
    patron_nuevo = r"^[A-Z]{2}\d{3}[A-Z]{2}$"  # AB123CD
    return re.match(patron_viejo, patente) or re.match(patron_nuevo, patente)


def validar_fecha(fecha):
    """
    Valida que la fecha tenga formato AAAA-MM-DD.
    Retorna True si es válida, False si no.
    """
    patron = r"^\d{4}-\d{2}-\d{2}$"
    return re.match(patron, fecha) is not None


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
