from datetime import timedelta
from gestion.index import (
    calcular_tarifa,
    generar_mapa_plazas,
    crear_estacionamiento_dos_columnas,
    crear_estacionamiento_doble_pasillo,
)
from consultas.constantes.index import ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_VACIO, ESTADO_OCUPADO


def test_tarifa_primera_hora():
    assert calcular_tarifa(timedelta(seconds=3600), "AUTO") == 1000.0


def test_tarifa_con_fraccion_extra():
    # 1h + 15min → 1 fracción adicional
    assert calcular_tarifa(timedelta(seconds=4500), "AUTO") == 1250.0


def test_tarifa_camioneta_multiplica_doble():
    # 1h + 15min con camioneta (multiplicador 2.0)
    assert calcular_tarifa(timedelta(seconds=4500), "CAMIONETA") == 1500.0


def test_mapa_plazas_rectangular():
    matriz = [[ESTADO_LIBRE, ESTADO_LIBRE], [ESTADO_LIBRE, ESTADO_LIBRE]]
    assert generar_mapa_plazas(matriz) == {
        "P1": (0, 0), "P2": (0, 1),
        "P3": (1, 0), "P4": (1, 1),
    }


def test_mapa_plazas_excluye_pasillo():
    matriz = [[ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_LIBRE]]
    assert generar_mapa_plazas(matriz) == {"P1": (0, 0), "P2": (0, 2)}


def test_dos_columnas_plazas_pares():
    matriz = crear_estacionamiento_dos_columnas(4)
    assert len(matriz) == 2
    assert matriz[0] == [ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_LIBRE]


def test_dos_columnas_plaza_impar_rellena_con_vacio():
    matriz = crear_estacionamiento_dos_columnas(3)
    assert matriz[1] == [ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_VACIO]


def test_doble_pasillo_pasillos_en_posicion_correcta():
    matriz = crear_estacionamiento_doble_pasillo(4)
    assert matriz[0][1] == ESTADO_PASILLO
    assert matriz[0][4] == ESTADO_PASILLO
