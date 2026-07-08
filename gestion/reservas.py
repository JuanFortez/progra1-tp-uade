from consultas.constantes.index import TIPO_VEHICULO, ESTADO_LIBRE, ESTADO_RESERVADA, ESTADO_OCUPADO
from consultas.validacion.index import (
    validar_entero,
    validar_fecha,
    validar_patente,
    validar_dni,
    validar_telefono,
    generar_codigo_reserva,
    validar_nombre,
)
from consultas.visualizacion.index import mostrar_estacionamiento, generar_letras_columnas
from gestion.index import seleccionar_plaza_por_codigo
from ui.index import limpiar_pantalla, lista_modificar_reserva
from logs.index import escribir_log
from time import sleep


def verificar_disponibilidad(
    reservas, fila, columna, fecha_ingreso, fecha_salida, codigo_excluir=-1
):
    """
    Verifica si una plaza esta disponible entre dos fechas.
    """
    for reserva in reservas:
        if reserva["codigo"] != codigo_excluir:
            if reserva["estado"] == "ACTIVA":
                if reserva["fila"] == fila and reserva["columna"] == columna:
                    if not (
                        fecha_salida < reserva["fecha_ingreso"]
                        or fecha_ingreso > reserva["fecha_salida"]
                    ):
                        return False

    return True


def crear_reserva_administrador(reservas, reservas_clientes, matriz, clientes):
    """
    Crea una reserva desde el panel de administrador.

    Los datos del cliente se guardan en la lista clientes.
    La reserva solo guarda el DNI como referencia al cliente.
    """
    limpiar_pantalla()

    patente = input("Ingrese la patente (ej: ABC123 o AB123CD): ").upper().strip()

    while not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        patente = input("Ingrese la patente (ej: ABC123 o AB123CD): ").upper()

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

    tipo_vehiculo = (
        input("Ingrese tipo de vehículo (auto, moto, camioneta): ").upper().strip()
    )

    while tipo_vehiculo not in TIPO_VEHICULO:
        print("Tipo inválido. Opciones válidas: AUTO, MOTO, CAMIONETA")
        tipo_vehiculo = (
            input("\nIngrese el tipo de vehículo (AUTO, MOTO o CAMIONETA): ")
            .upper()
            .strip()
        )

    registrar_cliente_si_no_existe(
        clientes, nombre_titular, dni_titular, numero_telefono
    )

    plaza = seleccionar_plaza_por_codigo(matriz)

    if plaza is None:
        return

    fila, columna = plaza

    while matriz[fila][columna] == ESTADO_OCUPADO:
        print("La plaza seleccionada está físicamente ocupada.")
        plaza = seleccionar_plaza_por_codigo(matriz)
        if plaza is None:
            return
        fila, columna = plaza

    fecha_ingreso = input("Ingrese fecha de ingreso (AAAA-MM-DD): ").strip()

    while not validar_fecha(fecha_ingreso):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha_ingreso = input("Ingrese fecha de ingreso (AAAA-MM-DD): ")

    fecha_salida = input("Ingrese fecha de salida (AAAA-MM-DD): ").strip()

    while not validar_fecha(fecha_salida):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha_salida = input("Ingrese fecha de salida (AAAA-MM-DD): ")

    if fecha_ingreso >= fecha_salida:
        print("La fecha de ingreso debe ser anterior a la fecha de salida.")
        return

    reservas_activas_clientes = [r for r in reservas_clientes if r["estado"] == "ACTIVA"]

    disponible = verificar_disponibilidad(
        reservas + reservas_activas_clientes, fila, columna, fecha_ingreso, fecha_salida
    )

    if disponible:
        codigo = generar_codigo_reserva(reservas)
        reserva = {
            "codigo": codigo,
            "patente": patente,
            "nombre": nombre_titular,
            "dni_cliente": dni_titular,
            "numero_telefono": numero_telefono,
            "tipo_vehiculo": tipo_vehiculo,
            "fila": fila,
            "columna": columna,
            "fecha_ingreso": fecha_ingreso,
            "fecha_salida": fecha_salida,
            "estado": "ACTIVA",
        }
        reservas.append(reserva)
        matriz[fila][columna] = ESTADO_RESERVADA
        print("Reserva creada correctamente.")
        escribir_log(f"Reserva creada correctamente, patente: {patente}")
    else:
        print("La plaza no está disponible en esas fechas.")


def crear_reserva_cliente(reservas_clientes):
    """
    Crea una nueva reserva de cliente si la plaza está disponible.
    """
    limpiar_pantalla()

    patente = input("Ingrese la patente (ej: ABC123 o AB123CD): ").upper().strip()

    while not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        patente = input("Ingrese la patente (ej: ABC123 o AB123CD): ").upper().strip()

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

    tipo_vehiculo = (
        input("Ingrese tipo de vehículo (AUTO, MOTO, CAMIONETA): ").upper().strip()
    )

    while tipo_vehiculo not in TIPO_VEHICULO:
        print("Tipo inválido. Opciones válidas: AUTO, MOTO, CAMIONETA")
        tipo_vehiculo = (
            input("\nIngrese el tipo de vehículo (AUTO, MOTO o CAMIONETA): ")
            .upper()
            .strip()
        )

    fecha_ingreso = input("Ingrese fecha de ingreso (AAAA-MM-DD): ").strip()

    while not validar_fecha(fecha_ingreso):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha_ingreso = input("Ingrese fecha de ingreso (AAAA-MM-DD): ")

    fecha_salida = input("Ingrese fecha de salida (AAAA-MM-DD): ").strip()

    while not validar_fecha(fecha_salida):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha_salida = input("Ingrese fecha de salida (AAAA-MM-DD): ")

    if fecha_ingreso >= fecha_salida:
        print("La fecha de ingreso debe ser anterior a la fecha de salida.")
        return

    codigo = generar_codigo_reserva(reservas_clientes)
    reserva = {
        "codigo": codigo,
        "patente": patente,
        "nombre": nombre_titular,
        "dni": dni_titular,
        "numero_telefono": numero_telefono,
        "tipo_vehiculo": tipo_vehiculo,
        "fecha_ingreso": fecha_ingreso,
        "fecha_salida": fecha_salida,
        "estado": "PENDIENTE",
    }
    reservas_clientes.append(reserva)
    print("Reserva creada correctamente.")
    escribir_log(f"Reserva creada correctamente, patente: {patente}.")


def cancelar_reserva(reservas, matriz):
    """
    Cancela una reserva cambiando su estado a CANCELADA.
    """
    limpiar_pantalla()

    codigo_buscar = input("Ingrese el código de la reserva a cancelar: ").strip()

    for reserva in reservas:

        if reserva["codigo"] == codigo_buscar:

            if reserva["estado"] == "CANCELADA":
                print("La reserva ya estaba cancelada.")
                return

            reserva["estado"] = "CANCELADA"

            if "fila" in reserva and "columna" in reserva:
                matriz[reserva["fila"]][reserva["columna"]] = ESTADO_LIBRE

            print("Reserva cancelada correctamente.")
            escribir_log(
                f"Reserva cancelada correctamente, patente: {reserva['patente']}"
            )
            return

    print("No se encontró una reserva con ese código.")


def modificar_reserva(reservas, reservas_clientes, matriz):
    """
    Modifica los datos de una reserva existente.
    """
    limpiar_pantalla()

    codigo_buscar = input("Ingrese el código de la reserva a modificar: ").strip()

    encontrada = False
    for reserva in reservas:
        if reserva["codigo"] == codigo_buscar:
            encontrada = True
            if reserva["estado"] == "CANCELADA":
                print("No se puede modificar una reserva cancelada.")
                return

            while True:
                lista_modificar_reserva()

                opcion = validar_entero("Seleccione la modificación a realizar: ", 1, 9)

                if opcion == 5:
                    plaza = seleccionar_plaza_por_codigo(matriz)

                    if plaza is None:
                        continue

                    nueva_fila, nueva_columna = plaza

                    if matriz[nueva_fila][nueva_columna] == ESTADO_OCUPADO:
                        print("La plaza seleccionada está físicamente ocupada.")
                        continue

                    reservas_activas_clientes = [r for r in reservas_clientes if r["estado"] == "ACTIVA"]

                    disponible = verificar_disponibilidad(
                        reservas + reservas_activas_clientes,
                        nueva_fila,
                        nueva_columna,
                        reserva["fecha_ingreso"],
                        reserva["fecha_salida"],
                        codigo_buscar,
                    )

                    if not disponible:
                        print("La plaza no está disponible en esas fechas.")
                        continue

                    matriz[reserva["fila"]][reserva["columna"]] = ESTADO_LIBRE
                    reserva["fila"] = nueva_fila
                    reserva["columna"] = nueva_columna
                    matriz[nueva_fila][nueva_columna] = ESTADO_RESERVADA
                    escribir_log(f"Plaza de la reserva {codigo_buscar} modificada a {plaza}")
                    print("Plaza de la reserva modificada correctamente.")
                    continue
                
                if opcion == 9:
                    print("Volviendo a vista de reservas...")
                    sleep(1)
                    break
                
                match opcion:
                    case 1:
                        nueva_patente = input("Ingrese nueva patente: ").upper().strip()

                        if not validar_patente(nueva_patente):
                            print("Patente inválida.")
                            continue
                        reserva["patente"] = nueva_patente
                        escribir_log(f"Patente de la reserva {codigo_buscar} modificada a {nueva_patente}")
                        print("Patente modificada correctamente.")
                        continue

                    case 2:
                        nuevo_nombre = input("Ingrese nuevo nombre: ").upper().strip()

                        while not validar_nombre(nuevo_nombre):
                            print(
                                "\nNombre inválido. Ingrese solo letras y espacios.\n"
                            )
                            nuevo_nombre = (
                                input("Ingrese nuevo nombre: ").upper().strip()
                            )

                        reserva["nombre"] = nuevo_nombre
                        escribir_log(f"Nombre de la reserva {codigo_buscar} modificado a {nuevo_nombre}")
                        print("Nombre modificado correctamente.")
                        continue

                    case 3:
                        nuevo_dni = input("Ingrese nuevo DNI: ").strip()

                        while not validar_dni(nuevo_dni):
                            print(
                                "\nDNI inválido. Formato esperado: 9999999 o 99.999.999\n"
                            )
                            nuevo_dni = input("Ingrese nuevo DNI: ").strip()

                        reserva["dni_cliente"] = nuevo_dni
                        escribir_log(f"DNI de la reserva {codigo_buscar} modificado a {nuevo_dni}")
                        print("DNI modificado correctamente.")
                        continue

                    case 4:
                        nuevo_telefono = input(
                            "Ingrese nuevo número de teléfono (sin 0 ni 15): "
                        ).strip()

                        while not validar_telefono(nuevo_telefono):
                            print("\nNúmero de teléfono inválido.\n")
                            nuevo_telefono = input(
                                "Ingrese nuevo número de teléfono: "
                            ).strip()

                        reserva["numero_telefono"] = nuevo_telefono
                        escribir_log(f"Teléfono de la reserva {codigo_buscar} modificado a {nuevo_telefono}")
                        print("Teléfono modificado correctamente.")
                        continue

                    case 6:
                        nueva_fecha = input(
                            "Ingrese nueva fecha de inicio (AAAA-MM-DD): "
                        ).strip()

                        if not validar_fecha(nueva_fecha):
                            print("Fecha inválida.")
                            continue
                        if nueva_fecha >= reserva["fecha_salida"]:
                            print("La fecha de ingreso debe ser anterior a la fecha de salida.")
                            continue
                        reservas_activas_clientes = [r for r in reservas_clientes if r["estado"] == "ACTIVA"]
                        if not verificar_disponibilidad(
                            reservas + reservas_activas_clientes,
                            reserva["fila"], reserva["columna"],
                            nueva_fecha, reserva["fecha_salida"],
                            codigo_buscar,
                        ):
                            print("Las nuevas fechas generan un conflicto con otra reserva.")
                            continue
                        reserva["fecha_ingreso"] = nueva_fecha
                        escribir_log(f"Fecha de ingreso de la reserva {codigo_buscar} modificada a {nueva_fecha}")
                        print("Fecha de ingreso modificada correctamente.")
                        continue

                    case 7:
                        nueva_fecha = input(
                            "Ingrese nueva fecha de fin (AAAA-MM-DD): "
                        ).strip()

                        if not validar_fecha(nueva_fecha):
                            print("Fecha inválida.")
                            continue
                        if reserva["fecha_ingreso"] >= nueva_fecha:
                            print("La fecha de salida debe ser posterior a la fecha de ingreso.")
                            continue
                        reservas_activas_clientes = [r for r in reservas_clientes if r["estado"] == "ACTIVA"]
                        if not verificar_disponibilidad(
                            reservas + reservas_activas_clientes,
                            reserva["fila"], reserva["columna"],
                            reserva["fecha_ingreso"], nueva_fecha,
                            codigo_buscar,
                        ):
                            print("Las nuevas fechas generan un conflicto con otra reserva.")
                            continue
                        reserva["fecha_salida"] = nueva_fecha
                        escribir_log(f"Fecha de salida de la reserva {codigo_buscar} modificada a {nueva_fecha}")
                        print("Fecha de salida modificada correctamente.")
                        continue

                    case 8:
                        nuevo_tipo_vehiculo = (
                            input("Ingrese el nuevo tipo de vehículo (auto, moto, camioneta): ")
                            .upper()
                            .strip()
                        )

                        while nuevo_tipo_vehiculo not in TIPO_VEHICULO:
                            print("Tipo inválido. Opciones válidas: AUTO, MOTO, CAMIONETA")
                            nuevo_tipo_vehiculo = (
                                input("\nIngrese el tipo de vehículo (AUTO, MOTO o CAMIONETA): ")
                                .upper()
                                .strip()
                            )
                        reserva["tipo_vehiculo"] = nuevo_tipo_vehiculo
                        escribir_log(f"Tipo de vehículo de la reserva {codigo_buscar} modificado a {nuevo_tipo_vehiculo}")
                        print("Tipo de vehículo modificado correctamente.")
                        continue

            break

    if not encontrada:
        print("No se encontró una reserva con ese código.")


def lista_reservas_activas(reservas, matriz):
    """
    Muestra todas las reservas activas indicando el código de plaza.
    """
    limpiar_pantalla()

    letras_columnas = generar_letras_columnas(matriz)

    print("=" * 32)
    print("\tReservas activas")
    print("=" * 32)

    hay_activas = False

    for i, reserva in enumerate(reservas):
        if reserva["estado"] == "CANCELADA":
            continue

        hay_activas = True
        codigo_plaza = "Sin asignar"

        if "fila" in reserva and "columna" in reserva:
            letra_columna = letras_columnas.get(reserva["columna"])
            if letra_columna is not None:
                codigo_plaza = f"{reserva['fila'] + 1}{letra_columna}"

        print(f"Reserva #{i + 1}")
        print(f"Código: {reserva.get('codigo', 'Sin dato')}")
        print(f"Patente: {reserva['patente']}")

        if "fecha_ingreso" in reserva:
            print(f"Fecha inicio: {reserva['fecha_ingreso']}")

        if "fecha_salida" in reserva:
            print(f"Fecha fin: {reserva['fecha_salida']}")

        if "fecha" in reserva:
            print(f"Fecha: {reserva['fecha']}")

        if "hora" in reserva:
            print(f"Hora: {reserva['hora']}")

        print(f"Estado: {reserva.get('estado', 'Sin dato')}")
        print(f"Plaza: {codigo_plaza}")
        print("-" * 30)

    if not hay_activas:
        print("\nNo hay reservas activas.")
        sleep(2)
        return


def buscar_reserva_por_cliente(reservas, reservas_clientes, clientes, matriz):
    """
    Busca reservas por cliente usando los datos guardados en la lista clientes.

    Permite buscar por:
    - nombre
    - DNI
    - patente
    """
    if len(reservas) == 0 and len(reservas_clientes) == 0:
        print("\nNo hay reservas registradas.")
        return

    busqueda = input("\nIngrese nombre, DNI o patente del cliente: ").upper().strip()

    if busqueda == "":
        print("\nDebe ingresar un término de búsqueda.")
        return

    reservas_encontradas = []

    for reserva in reservas:
        dni_cliente = reserva.get("dni_cliente", "")
        cliente = buscar_cliente_por_dni(clientes, dni_cliente)

        if cliente is not None:
            nombre_cliente = cliente["nombre"].upper()
            dni = cliente["dni"]
        else:
            nombre_cliente = reserva.get("nombre", "").upper()
            dni = reserva.get("dni_cliente", "")

        patente = reserva.get("patente", "").upper()

        if busqueda in nombre_cliente or busqueda == dni or busqueda == patente:
            reservas_encontradas.append((reserva, cliente))

    for reserva in reservas_clientes:
        dni_cliente = reserva.get("dni", "")
        cliente = buscar_cliente_por_dni(clientes, dni_cliente)

        if cliente is not None:
            nombre_cliente = cliente["nombre"].upper()
            dni = cliente["dni"]
        else:
            nombre_cliente = reserva.get("nombre", "").upper()
            dni = reserva.get("dni", "")

        patente = reserva.get("patente", "").upper()

        if busqueda in nombre_cliente or busqueda == dni or busqueda == patente:
            reservas_encontradas.append((reserva, cliente))

    if len(reservas_encontradas) == 0:
        print("\nNo se encontraron reservas para ese cliente.")
        return

    letras_columnas = generar_letras_columnas(matriz)

    print("\nReservas encontradas:\n")

    for i, datos_reserva in enumerate(reservas_encontradas):
        reserva = datos_reserva[0]
        cliente = datos_reserva[1]

        codigo_plaza = "Sin asignar"

        if "fila" in reserva and "columna" in reserva:
            letra_columna = letras_columnas.get(reserva["columna"])
            if letra_columna is not None:
                codigo_plaza = f"{reserva['fila'] + 1}{letra_columna}"

        print(f"Reserva #{i + 1}")
        print(f"Patente: {reserva.get('patente', 'Sin dato')}")

        if cliente is not None:
            print(f"Cliente: {cliente['nombre']}")
            print(f"DNI: {cliente['dni']}")
            print(f"Teléfono: {cliente['telefono']}")
        elif "nombre" in reserva:
            print(f"Cliente: {reserva['nombre']}")
            dni_mostrar = reserva.get("dni") or reserva.get("dni_cliente")
            if dni_mostrar:
                print(f"DNI: {dni_mostrar}")
            if "numero_telefono" in reserva:
                print(f"Teléfono: {reserva['numero_telefono']}")
        else:
            print("Cliente: Sin datos guardados")

        print(f"Tipo de vehículo: {reserva.get('tipo_vehiculo', 'Sin dato')}")
        print(f"Plaza: {codigo_plaza}")

        if "fecha_ingreso" in reserva:
            print(f"Fecha ingreso: {reserva['fecha_ingreso']}")

        if "fecha_salida" in reserva:
            print(f"Fecha salida: {reserva['fecha_salida']}")

        print("-" * 30)


def buscar_cliente_por_dni(clientes, dni, indice=0):
    """
    Busca un cliente por DNI dentro de la lista de clientes.
    """
    if indice >= len(clientes):
        return None

    if clientes[indice]["dni"] == dni:
        return clientes[indice]

    return buscar_cliente_por_dni(clientes, dni, indice + 1)


def registrar_cliente_si_no_existe(clientes, nombre, dni, numero_telefono):
    """
    Registra un cliente en la lista si todavía no existe.

    Si ya existe, actualiza nombre y teléfono por si cambiaron.
    """
    cliente = buscar_cliente_por_dni(clientes, dni)

    if cliente is None:
        clientes.append({"dni": dni, "nombre": nombre, "telefono": numero_telefono})
    else:
        cliente["nombre"] = nombre
        cliente["telefono"] = numero_telefono


def lista_reservas_clientes(reservas):
    """
    Muestra todas las reservas activas.
    """
    limpiar_pantalla()
    hay_activas = False

    reservas_ordenadas = ordenar_reservas_fechas(reservas)

    print("\nLISTA DE RESERVAS DE CLIENTES")
    print("-" * 40)

    for reserva in reservas_ordenadas:
        if reserva["estado"] == "PENDIENTE":
            hay_activas = True
            print("Patente:", reserva["patente"])
            print("Nombre:", reserva["nombre"])
            print("DNI:", reserva["dni"])
            print("Teléfono:", reserva["numero_telefono"])
            print("Tipo de vehículo:", reserva["tipo_vehiculo"])
            print("Fecha de ingreso:", reserva["fecha_ingreso"])
            print("Fecha de salida:", reserva["fecha_salida"])
            print("Estado:", reserva["estado"])
            print("-" * 40)

    if not hay_activas:
        print("No hay reservas pendientes.")


def ordenar_reservas_fechas(reservas):
    """
    Ordena las reservas por fecha de ingreso, de menor a mayor.
    """

    reservas_ordenadas = reservas[:]

    for i in range(len(reservas_ordenadas) - 1):
        for j in range(i + 1, len(reservas_ordenadas)):

            if (
                reservas_ordenadas[i]["fecha_ingreso"]
                > reservas_ordenadas[j]["fecha_ingreso"]
            ):

                aux = reservas_ordenadas[i]
                reservas_ordenadas[i] = reservas_ordenadas[j]
                reservas_ordenadas[j] = aux

    return reservas_ordenadas


def filtrar_por_fecha(reservas, fecha):
    """
    Devuelve reservas que comienzan en la fecha indicada.
    """

    return list(filter(lambda reserva: reserva["fecha_ingreso"] == fecha, reservas))


def filtrar_rango_fechas(reservas, fecha_ingreso, fecha_salida):
    """
    Devuelve reservas dentro del rango de fechas.
    """

    return list(
        filter(
            lambda reserva: reserva["fecha_ingreso"] >= fecha_ingreso
            and reserva["fecha_ingreso"] <= fecha_salida,
            reservas,
        )
    )

def filtrar_vehiculo_patente(vehiculos, patente):
    """
    Busca vehículos que coincidan con la patente.
    """

    return list(filter(lambda vehiculo: vehiculo["patente"] == patente, vehiculos))


def buscar_fecha(reservas, matriz):
    """
    Permite elegir el tipo de búsqueda o volver al menú anterior.
    """

    print("\nTipo de búsqueda:")
    print("1 - Fecha exacta")
    print("2 - Rango de fechas")
    print("3 - Volver al menú anterior")

    opcion = validar_entero("Seleccione una opción: ", 1, 3)

    if opcion == 1:
        buscar_por_fecha_exacta(reservas, matriz)

    elif opcion == 2:
        buscar_por_rango_fechas(reservas, matriz)

    elif opcion == 3:
        return


def buscar_por_fecha_exacta(reservas, matriz):
    """
    Busca reservas que coincidan con una fecha exacta.
    """

    fecha = input("Ingrese la fecha (AAAA-MM-DD): ")

    if not validar_fecha(fecha):
        print("Fecha inválida.")
        return

    reservas_filtradas = filtrar_por_fecha(reservas, fecha)

    lista_reservas_activas(reservas_filtradas, matriz)


def buscar_por_rango_fechas(reservas, matriz):
    """
    Busca reservas cuya fecha de ingreso esté dentro de un rango.
    """

    fecha_ingreso = input("Ingrese fecha inicio (AAAA-MM-DD): ")

    if not validar_fecha(fecha_ingreso):
        print("Fecha de inicio inválida.")
        return

    fecha_salida = input("Ingrese fecha fin (AAAA-MM-DD): ")

    if not validar_fecha(fecha_salida):
        print("Fecha de fin inválida.")
        return

    if fecha_ingreso > fecha_salida:
        print("La fecha de inicio no puede ser mayor que la fecha de fin.")
        return

    reservas_filtradas = filtrar_rango_fechas(reservas, fecha_ingreso, fecha_salida)

    lista_reservas_activas(reservas_filtradas, matriz)


def asignar_plaza(reservas_clientes, reservas, matriz):
    """
    Asigna una plaza libre a una reserva pendiente de cliente.
    """
    limpiar_pantalla()

    patente_buscar = (
        input("Ingrese la patente de la reserva a asignar: ").upper().strip()
    )
    reserva_encontrada = None

    for reserva in reservas_clientes:
        if reserva["patente"] == patente_buscar and reserva["estado"] == "PENDIENTE":
            reserva_encontrada = reserva
            break

    if reserva_encontrada is None:
        existe = any(r["patente"] == patente_buscar for r in reservas_clientes)
        if existe:
            print("No hay reservas pendientes con esa patente.")
        else:
            print("No se encontró una reserva con esa patente.")
        return

    plaza = seleccionar_plaza_por_codigo(matriz)

    if plaza is None:
        return

    fila, columna = plaza

    if matriz[fila][columna] == ESTADO_OCUPADO:
        print("La plaza esta físicamente ocupada actualmente.")
        return

    reservas_activas_clientes = [r for r in reservas_clientes if r["estado"] == "ACTIVA"]

    disponible = verificar_disponibilidad(
        reservas + reservas_activas_clientes,
        fila,
        columna,
        reserva_encontrada["fecha_ingreso"],
        reserva_encontrada["fecha_salida"],
    )

    if not disponible:
        print("La plaza no esta disponible en esas fechas.")
        return

    reserva_encontrada["fila"] = fila
    reserva_encontrada["columna"] = columna
    reserva_encontrada["estado"] = "ACTIVA"
    matriz[fila][columna] = ESTADO_RESERVADA
    print("La plaza fue reservada correctamente.")
