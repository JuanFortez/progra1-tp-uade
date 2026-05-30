import os
from datetime import datetime
from consultas.constantes.index import RUTA_LOG

ruta_log = str(RUTA_LOG)


def escribir_log(mensaje):
    """Agrega una entrada al archivo de log con fecha y hora."""
    marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ruta_log, "a", encoding="utf-8") as archivo:
        archivo.write(f"[{marca_tiempo}] {mensaje}\n")


def leer_log():
    """Lee el archivo de log y devuelve la lista de líneas."""
    if not os.path.exists(ruta_log):
        return []

    with open(ruta_log, "r", encoding="utf-8") as archivo:
        return archivo.readlines()