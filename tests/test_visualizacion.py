from consultas.visualizacion.index import (
    es_plaza_real,
    contar_plazas_ocupadas,
    contar_plazas_disponibles,
)
from consultas.constantes.index import ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_OCUPADO, ESTADO_RESERVADA


def test_libre_es_plaza_real():
    assert es_plaza_real(ESTADO_LIBRE)


def test_pasillo_no_es_plaza_real():
    assert not es_plaza_real(ESTADO_PASILLO)


def test_contar_plazas_ocupadas():
    matriz = [[ESTADO_OCUPADO, ESTADO_LIBRE], [ESTADO_RESERVADA, ESTADO_PASILLO]]
    assert contar_plazas_ocupadas(matriz) == 1


def test_contar_plazas_ocupadas_ninguna():
    matriz = [[ESTADO_LIBRE, ESTADO_LIBRE]]
    assert contar_plazas_ocupadas(matriz) == 0


def test_contar_plazas_disponibles():
    matriz = [[ESTADO_LIBRE, ESTADO_PASILLO, ESTADO_LIBRE]]
    assert contar_plazas_disponibles(matriz) == 2


def test_contar_plazas_disponibles_ninguna():
    matriz = [[ESTADO_OCUPADO, ESTADO_RESERVADA]]
    assert contar_plazas_disponibles(matriz) == 0
