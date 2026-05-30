import json
import os
from datetime import datetime
from consultas.constantes.index import DATOS_DIR

ruta_datos = str(DATOS_DIR)

def convertir_para_json(dato):
    if isinstance(dato, datetime):
        return dato.isoformat()

    if isinstance(dato, tuple):
        return list(dato)

    if isinstance(dato, list):
        return [convertir_para_json(elemento) for elemento in dato]

    if isinstance(dato, dict):
        return {clave: convertir_para_json(valor) for clave, valor in dato.items()}

    return dato


def restaurar_registros(registros):
    for patente in registros:
        if "hora_ingreso" in registros[patente]:
            registros[patente]["hora_ingreso"] = datetime.fromisoformat(
                registros[patente]["hora_ingreso"]
            )

        if "plaza" in registros[patente]:
            registros[patente]["plaza"] = tuple(registros[patente]["plaza"])

    return registros


def cargar_datos():
    if not os.path.exists(ruta_datos):
        return {
            "matriz": None,
            "reservas": [],
            "reservas_clientes": [],
            "registros": {},
            "historial": [],
            "clientes": [],
        }

    with open(ruta_datos, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    datos["registros"] = restaurar_registros(datos.get("registros", {}))
    datos["historial"] = datos.get("historial", [])
    datos["clientes"] = datos.get("clientes", [])

    return datos


def guardar_datos(matriz, reservas, reservas_clientes, registros, historial, clientes):
    datos = {
        "matriz": matriz,
        "reservas": reservas,
        "reservas_clientes": reservas_clientes,
        "registros": registros,
        "historial": historial,
        "clientes": clientes,
    }

    datos_convertidos = convertir_para_json(datos)

    with open(ruta_datos, "w", encoding="utf-8") as archivo:
        json.dump(datos_convertidos, archivo, indent=4, ensure_ascii=False)
