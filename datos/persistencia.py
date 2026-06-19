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
            "admin": None,
            "abonos": [],
            "abonos_clientes": [],
        }

    with open(ruta_datos, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    datos["matriz"] = datos.get("matriz", None)
    datos["reservas"] = datos.get("reservas", [])
    datos["reservas_clientes"] = datos.get("reservas_clientes", [])
    datos["registros"] = restaurar_registros(datos.get("registros", {}))
    datos["historial"] = datos.get("historial", [])
    datos["clientes"] = datos.get("clientes", [])
    datos["admin"] = datos.get("admin", None)
    datos["abonos"] = datos.get("abonos", [])
    datos["abonos_clientes"] = datos.get("abonos_clientes", [])

    return datos


def guardar_datos(matriz, reservas, reservas_clientes, registros, historial, clientes, admin, abonos=None, abonos_clientes=None):
    datos = {
        "matriz": matriz,
        "reservas": reservas,
        "reservas_clientes": reservas_clientes,
        "registros": registros,
        "historial": historial,
        "clientes": clientes,
        "admin": admin,
        "abonos": abonos if abonos is not None else [],
        "abonos_clientes": abonos_clientes if abonos_clientes is not None else [],
    }

    datos_convertidos = convertir_para_json(datos)

    with open(ruta_datos, "w", encoding="utf-8") as archivo:
        json.dump(datos_convertidos, archivo, indent=4, ensure_ascii=False)
