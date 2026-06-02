from consultas.validacion.index import (
    validar_patente,
    validar_dni,
    validar_telefono,
    validar_nombre,
    año_bisiesto,
    dia_valido,
    validar_fecha,
)


def test_patente_formato_viejo_valida():
    assert validar_patente("ABC123")


def test_patente_formato_nuevo_valida():
    assert validar_patente("AB123CD")


def test_patente_invalida():
    assert not validar_patente("AB12")


def test_dni_valido():
    assert validar_dni("12345678")


def test_dni_invalido():
    assert not validar_dni("123456")


def test_telefono_valido():
    assert validar_telefono("1145678901")


def test_telefono_invalido():
    assert not validar_telefono("9999999999")


def test_nombre_valido():
    assert validar_nombre("Juan Perez")


def test_nombre_invalido():
    assert not validar_nombre("Juan123")


def test_año_bisiesto():
    assert año_bisiesto(2024)


def test_año_no_bisiesto():
    assert not año_bisiesto(2023)


def test_dia_valido_febrero_bisiesto():
    assert dia_valido(29, 2, 2024)


def test_dia_invalido_febrero_no_bisiesto():
    assert not dia_valido(29, 2, 2023)


def test_fecha_valida():
    assert validar_fecha("2024-06-15")


def test_fecha_formato_incorrecto():
    assert not validar_fecha("15/06/2024")


def test_fecha_dia_invalido():
    assert not validar_fecha("2024-02-30")
