import os
from datetime import datetime

RUTA_LOG = "logs.txt"


def escribir_log(mensaje):
    """Agrega una entrada al archivo de log con fecha y hora."""
    marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(f"[{marca_tiempo}] {mensaje}\n")


def leer_log():
    """Lee el archivo de log y devuelve la lista de líneas."""
    if not os.path.exists(RUTA_LOG):
        return []

    with open(RUTA_LOG, "r", encoding="utf-8") as archivo:
        return archivo.readlines()