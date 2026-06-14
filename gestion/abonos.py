from datetime import datetime, timedelta
from consultas.constantes.index import (
    TIPO_VEHICULO,
    MULTIPLICADORES_TARIFA,
    TIPOS_ABONO,
    DESCUENTOS_ABONO,
    TARIFA_DIARIA_RESERVA,
)
from consultas.validacion.index import (
    validar_entero,
    validar_patente,
    validar_dni,
    validar_telefono,
    validar_nombre,
    generar_codigo_reserva,
    validar_fecha,
)
from gestion.reservas import verificar_disponibilidad
from gestion.index import seleccionar_plaza_por_codigo, generar_mapa_plazas
from consultas.constantes.index import ESTADO_LIBRE, ESTADO_RESERVADA
from ui.index import limpiar_pantalla
from logs.index import escribir_log
from time import sleep


def calcular_tarifa_abono(tipo_abono, tipo_vehiculo, dias_reales=None):
    """
    Calcula la tarifa con descuento para un abono.

    Aplica una tarifa diaria fija reducida según el tipo de abono y
    un multiplicador según el tipo de vehículo.

    Retorna el monto total como flotante.
    """
    multiplicador = MULTIPLICADORES_TARIFA[tipo_vehiculo]
    descuento = DESCUENTOS_ABONO[tipo_abono]

    dias = dias_reales if dias_reales is not None else TIPOS_ABONO[tipo_abono]

    tarifa_sin_descuento = TARIFA_DIARIA_RESERVA * dias * multiplicador
    tarifa_final = tarifa_sin_descuento * (1 - descuento)

    return tarifa_final


def determinar_tipo_abono_por_dias(dias):
    """
    Determina si la cantidad de días corresponde a un tipo de abono
    y retorna el tipo correspondiente, o None si no aplica.

    Criterios:
    - 15 días: QUINCENAL
    - 30 días: MENSUAL
    - 180 días: SEMESTRAL
    - Rangos intermedios también clasifican al tipo más cercano inferior
    """
    if dias >= 180:
        return "SEMESTRAL"
    elif dias >= 30:
        return "MENSUAL"
    elif dias >= 15:
        return "QUINCENAL"
    return None


def mostrar_tipos_abono():
    """
    Muestra los tipos de abono disponibles con sus descuentos y duración.
    """
    print("\n" + "=" * 40)
    print(" " * 10 + "TIPOS DE ABONO")
    print("=" * 40)
    print(f"\n  1 - QUINCENAL  ({TIPOS_ABONO['QUINCENAL']} días) — {int(DESCUENTOS_ABONO['QUINCENAL']*100)}% descuento")
    print(f"  2 - MENSUAL    ({TIPOS_ABONO['MENSUAL']} días) — {int(DESCUENTOS_ABONO['MENSUAL']*100)}% descuento")
    print(f"  3 - SEMESTRAL  ({TIPOS_ABONO['SEMESTRAL']} días) — {int(DESCUENTOS_ABONO['SEMESTRAL']*100)}% descuento")
    print()


def seleccionar_tipo_abono():
    """
    Solicita al usuario que elija un tipo de abono y lo retorna como string.
    """
    mostrar_tipos_abono()
    opcion = validar_entero("Seleccione tipo de abono: ", 1, 3)
    tipos = ["QUINCENAL", "MENSUAL", "SEMESTRAL"]
    return tipos[opcion - 1]


def crear_abono_administrador(abonos, reservas, matriz, clientes):
    """
    Crea un abono desde el panel de administrador.

    El administrador elige el tipo de abono (quincenal, mensual, semestral),
    la fecha de inicio y la plaza. La fecha de fin se calcula automáticamente.
    Se aplica tarifa fija reducida según el tipo y vehículo.
    """
    limpiar_pantalla()

    print("\n" + "=" * 40)
    print(" " * 10 + "CREAR ABONO")
    print("=" * 40)

    patente = input("\nIngrese la patente (ej: ABC123 o AB123CD): ").upper().strip()
    while not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        patente = input("Ingrese la patente: ").upper().strip()

    nombre_titular = input("Ingrese nombre del titular: ").upper().strip()
    while not validar_nombre(nombre_titular):
        print("\nNombre inválido. Ingrese solo letras y espacios.\n")
        nombre_titular = input("Ingrese nombre del titular: ").upper().strip()

    dni_titular = input("Ingrese DNI del titular: ").strip()
    while not validar_dni(dni_titular):
        print("\nDNI inválido. Formato esperado: 99999999 o 99.999.999\n")
        dni_titular = input("Ingrese DNI del titular: ").strip()

    numero_telefono = input("Ingrese número de teléfono (sin 0 ni 15): ").strip()
    while not validar_telefono(numero_telefono):
        print("\nNúmero de teléfono inválido.\n")
        numero_telefono = input("Ingrese número de teléfono (sin 0 ni 15): ").strip()

    tipo_vehiculo = input("Ingrese tipo de vehículo (AUTO, MOTO, CAMIONETA): ").upper().strip()
    while tipo_vehiculo not in TIPO_VEHICULO:
        print("Tipo inválido. Opciones válidas: AUTO, MOTO, CAMIONETA")
        tipo_vehiculo = input("Ingrese el tipo de vehículo: ").upper().strip()

    tipo_abono = seleccionar_tipo_abono()
    dias_abono = TIPOS_ABONO[tipo_abono]

    fecha_inicio = input("Ingrese fecha de inicio del abono (AAAA-MM-DD): ").strip()
    while not validar_fecha(fecha_inicio):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha_inicio = input("Ingrese fecha de inicio del abono (AAAA-MM-DD): ").strip()

    # Calcular fecha fin automáticamente
    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_fin_dt = fecha_inicio_dt + timedelta(days=dias_abono)
    fecha_fin = fecha_fin_dt.strftime("%Y-%m-%d")
    print(f"Fecha de fin del abono: {fecha_fin}")

    plaza = seleccionar_plaza_por_codigo(matriz)
    if plaza is None:
        return

    fila, columna = plaza

    if matriz[fila][columna] != ESTADO_LIBRE:
        print("La plaza seleccionada no está libre.")
        return

    disponible = verificar_disponibilidad(reservas, fila, columna, fecha_inicio, fecha_fin)
    if not disponible:
        print("La plaza no está disponible en esas fechas.")
        return

    tarifa = calcular_tarifa_abono(tipo_abono, tipo_vehiculo, dias_abono)

    # Registrar cliente si no existe
    from gestion.reservas import registrar_cliente_si_no_existe
    registrar_cliente_si_no_existe(clientes, nombre_titular, dni_titular, numero_telefono)

    codigo = generar_codigo_reserva(abonos)

    abono = {
        "codigo": codigo,
        "tipo": "ABONO",
        "tipo_abono": tipo_abono,
        "patente": patente,
        "nombre": nombre_titular,
        "dni_cliente": dni_titular,
        "numero_telefono": numero_telefono,
        "tipo_vehiculo": tipo_vehiculo,
        "fila": fila,
        "columna": columna,
        "fecha_ingreso": fecha_inicio,
        "fecha_salida": fecha_fin,
        "tarifa_total": tarifa,
        "estado": "ACTIVA",
    }

    abonos.append(abono)
    reservas.append(abono)
    matriz[fila][columna] = ESTADO_RESERVADA

    print(f"\n✅ Abono {tipo_abono} creado correctamente.")
    print(f"   Período: {fecha_inicio} → {fecha_fin} ({dias_abono} días)")
    print(f"   Tarifa total con descuento ({int(DESCUENTOS_ABONO[tipo_abono]*100)}%): ${tarifa:.2f}")
    escribir_log(f"Abono {tipo_abono} creado, patente: {patente}, tarifa: ${tarifa:.2f}")


def crear_abono_cliente(abonos_clientes):
    """
    Permite a un cliente solicitar un abono.

    El cliente elige el tipo de abono y la fecha de inicio.
    La reserva queda en estado PENDIENTE hasta que el administrador asigne plaza.
    """
    limpiar_pantalla()

    print("\n" + "=" * 40)
    print(" " * 10 + "SOLICITAR ABONO")
    print("=" * 40)

    patente = input("\nIngrese la patente (ej: ABC123 o AB123CD): ").upper().strip()
    while not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        patente = input("Ingrese la patente: ").upper().strip()

    nombre_titular = input("Ingrese nombre del titular: ").strip()
    while not validar_nombre(nombre_titular):
        print("\nNombre inválido. Ingrese solo letras y espacios.\n")
        nombre_titular = input("Ingrese nombre del titular: ").strip()

    dni_titular = input("Ingrese DNI del titular: ").strip()
    while not validar_dni(dni_titular):
        print("\nDNI inválido. Formato esperado: 99999999 o 99.999.999\n")
        dni_titular = input("Ingrese DNI del titular: ").strip()

    numero_telefono = input("Ingrese número de teléfono (sin 0 ni 15): ").strip()
    while not validar_telefono(numero_telefono):
        print("\nNúmero de teléfono inválido.\n")
        numero_telefono = input("Ingrese número de teléfono (sin 0 ni 15): ").strip()

    tipo_vehiculo = input("Ingrese tipo de vehículo (AUTO, MOTO, CAMIONETA): ").upper().strip()
    while tipo_vehiculo not in TIPO_VEHICULO:
        print("Tipo inválido. Opciones válidas: AUTO, MOTO, CAMIONETA")
        tipo_vehiculo = input("Ingrese el tipo de vehículo: ").upper().strip()

    tipo_abono = seleccionar_tipo_abono()
    dias_abono = TIPOS_ABONO[tipo_abono]

    fecha_inicio = input("Ingrese fecha de inicio del abono (AAAA-MM-DD): ").strip()
    while not validar_fecha(fecha_inicio):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha_inicio = input("Ingrese fecha de inicio (AAAA-MM-DD): ").strip()

    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_fin_dt = fecha_inicio_dt + timedelta(days=dias_abono)
    fecha_fin = fecha_fin_dt.strftime("%Y-%m-%d")

    tarifa = calcular_tarifa_abono(tipo_abono, tipo_vehiculo, dias_abono)

    codigo = generar_codigo_reserva(abonos_clientes)

    abono = {
        "codigo": codigo,
        "tipo": "ABONO",
        "tipo_abono": tipo_abono,
        "patente": patente,
        "nombre": nombre_titular,
        "dni": dni_titular,
        "numero_telefono": numero_telefono,
        "tipo_vehiculo": tipo_vehiculo,
        "fecha_ingreso": fecha_inicio,
        "fecha_salida": fecha_fin,
        "tarifa_total": tarifa,
        "estado": "PENDIENTE",
    }

    abonos_clientes.append(abono)

    print(f"\n✅ Solicitud de abono {tipo_abono} registrada correctamente.")
    print(f"   Período: {fecha_inicio} → {fecha_fin} ({dias_abono} días)")
    print(f"   Tarifa estimada con descuento ({int(DESCUENTOS_ABONO[tipo_abono]*100)}%): ${tarifa:.2f}")
    print("   El administrador le asignará una plaza a la brevedad.")
    escribir_log(f"Solicitud abono {tipo_abono} cliente, patente: {patente}")


def listar_abonos(abonos):
    """
    Muestra todos los abonos activos con sus datos y tarifa.
    """
    limpiar_pantalla()

    print("\n" + "=" * 40)
    print(" " * 12 + "ABONOS ACTIVOS")
    print("=" * 40)

    hay_abonos = False

    for abono in abonos:
        if abono.get("tipo") != "ABONO":
            continue
        if abono["estado"] == "CANCELADA":
            continue

        hay_abonos = True
        print(f"\nCódigo:     {abono.get('codigo', 'Sin dato')}")
        print(f"Tipo abono: {abono.get('tipo_abono', 'Sin dato')}")
        print(f"Patente:    {abono['patente']}")
        print(f"Nombre:     {abono.get('nombre', 'Sin dato')}")
        print(f"Vehículo:   {abono.get('tipo_vehiculo', 'Sin dato')}")
        print(f"Desde:      {abono['fecha_ingreso']}")
        print(f"Hasta:      {abono['fecha_salida']}")
        print(f"Tarifa:     ${abono.get('tarifa_total', 0):.2f}")
        print(f"Estado:     {abono['estado']}")
        print("-" * 40)

    if not hay_abonos:
        print("\nNo hay abonos activos.")
        sleep(2)


def calcular_tarifa_reserva_por_dias(fecha_ingreso, fecha_salida, tipo_vehiculo):
    """
    Calcula la tarifa para una reserva según su duración.

    Si la reserva califica como abono (15, 30 o 180+ días), aplica
    el descuento correspondiente. Si no califica, aplica tarifa diaria normal.

    Retorna una tupla: (tarifa_total, tipo_abono_aplicado)
    donde tipo_abono_aplicado puede ser None si no hay descuento.
    """
    fecha_ini_dt = datetime.strptime(fecha_ingreso, "%Y-%m-%d")
    fecha_fin_dt = datetime.strptime(fecha_salida, "%Y-%m-%d")
    dias = (fecha_fin_dt - fecha_ini_dt).days

    tipo_abono = determinar_tipo_abono_por_dias(dias)

    multiplicador = MULTIPLICADORES_TARIFA[tipo_vehiculo]

    if tipo_abono:
        descuento = DESCUENTOS_ABONO[tipo_abono]
        tarifa_sin_descuento = TARIFA_DIARIA_RESERVA * dias * multiplicador
        tarifa_final = tarifa_sin_descuento * (1 - descuento)
    else:
        tarifa_final = TARIFA_DIARIA_RESERVA * dias * multiplicador

    return tarifa_final, tipo_abono
