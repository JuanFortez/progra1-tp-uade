import re

def validar_patente(patente):
    patron_viejo = r'^[A-Z]{3}\d{3}$'       # ABC123
    patron_nuevo = r'^[A-Z]{2}\d{3}[A-Z]{2}$'  # AB123CD
    return re.match(patron_viejo, patente) or re.match(patron_nuevo, patente)

def validar_fecha(fecha):
    """
    Valida que la fecha tenga formato AAAA-MM-DD.
    Retorna True si es válida, False si no.
    """
    patron = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(patron, fecha) is not None