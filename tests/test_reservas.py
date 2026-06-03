from gestion.reservas import (
    verificar_disponibilidad,
    buscar_cliente_por_dni,
    ordenar_reservas_fechas,
    filtrar_por_fecha,
    filtrar_rango_fechas,
    registrar_cliente_si_no_existe,
)


def test_disponibilidad_plaza_libre():
    assert verificar_disponibilidad([], 0, 0, "2024-06-01", "2024-06-05") == True


def test_disponibilidad_con_solapamiento():
    reservas = [{"codigo": "R1", "estado": "ACTIVA", "fila": 0, "columna": 0,
                 "fecha_ingreso": "2024-06-01", "fecha_salida": "2024-06-10"}]
    assert verificar_disponibilidad(reservas, 0, 0, "2024-06-05", "2024-06-15") == False


def test_disponibilidad_reserva_cancelada_no_bloquea():
    reservas = [{"codigo": "R1", "estado": "CANCELADA", "fila": 0, "columna": 0,
                 "fecha_ingreso": "2024-06-01", "fecha_salida": "2024-06-10"}]
    assert verificar_disponibilidad(reservas, 0, 0, "2024-06-05", "2024-06-15") == True


def test_buscar_cliente_existente():
    clientes = [{"dni": "12345678", "nombre": "Juan", "telefono": "1123456789"}]
    assert buscar_cliente_por_dni(clientes, "12345678")["nombre"] == "Juan"


def test_buscar_cliente_inexistente():
    assert buscar_cliente_por_dni([], "12345678") is None


def test_ordenar_reservas_por_fecha():
    reservas = [{"fecha_ingreso": "2024-06-10"}, {"fecha_ingreso": "2024-06-01"}]
    resultado = ordenar_reservas_fechas(reservas)
    assert resultado[0]["fecha_ingreso"] == "2024-06-01"


def test_filtrar_por_fecha_exacta():
    reservas = [
        {"fecha_ingreso": "2024-06-01", "patente": "ABC123"},
        {"fecha_ingreso": "2024-06-02", "patente": "XY123AB"},
    ]
    resultado = filtrar_por_fecha(reservas, "2024-06-01")
    assert len(resultado) == 1 and resultado[0]["patente"] == "ABC123"


def test_filtrar_rango_fechas():
    reservas = [
        {"fecha_ingreso": "2024-06-01"},
        {"fecha_ingreso": "2024-06-05"},
        {"fecha_ingreso": "2024-06-10"},
    ]
    assert len(filtrar_rango_fechas(reservas, "2024-06-01", "2024-06-05")) == 2



def test_registrar_cliente_nuevo():
    clientes = []
    registrar_cliente_si_no_existe(clientes, "JUAN", "12345678", "1145678901")
    assert len(clientes) == 1 and clientes[0]["dni"] == "12345678"


def test_registrar_cliente_existente_actualiza_datos():
    clientes = [{"dni": "12345678", "nombre": "JUAN", "telefono": "1111111111"}]
    registrar_cliente_si_no_existe(clientes, "JUAN PEREZ", "12345678", "2222222222")
    assert clientes[0]["nombre"] == "JUAN PEREZ"
