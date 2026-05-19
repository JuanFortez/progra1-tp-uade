from consultas.validacion.index import validar_entero, validar_fecha, validar_patente, validar_dni, validar_telefono
from consultas.visualizacion.index import mostrar_estacionamiento
from ui.index import limpiar_pantalla


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
                    if not (fecha_salida <  reserva["fecha_ingreso"] or fecha_ingreso > reserva["fecha_salida"]):
                        return False

    return True


def crear_reserva_administrador(reservas, matriz):
    """
    Crea una nueva reserva pendiente de asignacion de plaza.
    """
    limpiar_pantalla()

    patente = input("Ingrese la patente (ej: ABC123 o AB123CD): ").upper()

<<<<<<< HEAD
    if not validar_patente(patente):
        print("\nPatente invalida. Formato esperado: ABC123 o AB123CD")
        return

    nombre = input("Ingrese nombre del titular: ").strip()
    dni = input("Ingrese DNI del titular: ").strip()
    numero_telefono = input("Ingrese numero de telefono: ").strip()
    tipo_vehiculo = input("Ingrese tipo de vehiculo (auto, moto, camioneta): ").lower()

    fecha_ingreso = input("Ingrese fecha de ingreso (AAAA-MM-DD): ")

    if not validar_fecha(fecha_ingreso):
        print("Fecha invalida. Formato esperado: AAAA-MM-DD")
        return

    fecha_salida = input("Ingrese fecha de salida (AAAA-MM-DD): ")

    if not validar_fecha(fecha_salida):
        print("Fecha invalida. Formato esperado: AAAA-MM-DD")
        return
=======
    while not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        patente = input("Ingrese la patente (ej: ABC123 o AB123CD): ").upper()
    
    nombre = input("Ingrese nombre del titular: ").strip()
    dni = input("Ingrese DNI del titular: ").strip()
    
    while not validar_dni(dni):
        print("\nDNI inválido. Formato esperado: 45873620 o 45.873.620\n")
        dni = input("Ingrese DNI del titular: ").strip()
    
    numero_telefono = input("Ingrese número de teléfono (sin 0 ni 15): ").strip()

    while not validar_telefono(numero_telefono):
        print("\nNúmero de teléfono inválido.\n")
    
    tipo_vehiculo = input("Ingrese tipo de vehículo (auto, moto, camioneta): ").lower()

    mostrar_estacionamiento(matriz)

    fila = validar_entero("Ingrese fila: ", 1, len(matriz)) - 1
    columna = validar_entero("Ingrese columna: ", 1, len(matriz[0])) - 1

    if matriz[fila][columna] != "LIBRE":
        print("La plaza está ocupada actualmente.")
        return

    fecha_ingreso = input("Ingrese fecha de ingreso (AAAA-MM-DD): ")

    while not validar_fecha(fecha_ingreso):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha_ingreso = input("Ingrese fecha de ingreso (AAAA-MM-DD): ")
    
    fecha_salida = input("Ingrese fecha de salida (AAAA-MM-DD): ")

    while not validar_fecha(fecha_salida):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        fecha_salida = input("Ingrese fecha de salida (AAAA-MM-DD): ")
>>>>>>> develop

    if fecha_ingreso > fecha_salida:
        print("La fecha de ingreso no puede ser mayor que la fecha de salida.")
        return

    codigo = len(reservas) + 1
    reserva = {
        "codigo": codigo,
        "patente": patente,
        "nombre": nombre,
        "dni": dni,
        "numero_telefono": numero_telefono,
        "fila": None,
        "columna": None,
        "fecha_ingreso": fecha_ingreso,
        "fecha_salida": fecha_salida,
        "tipo_vehiculo": tipo_vehiculo,
        "estado": "PENDIENTE",
    }

    reservas.append(reserva)
    print("Reserva creada correctamente. Queda pendiente de asignacion de plaza.")

def crear_reserva_cliente(reservas_clientes):
    """
    Crea una nueva reserva de cliente si la plaza está disponible.
    """
    limpiar_pantalla()

    patente = input("Ingrese la patente (ej: ABC123 o AB123CD): ").upper()

    if not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        return
    
    nombre = input("Ingrese nombre del titular: ").strip()
    dni = input("Ingrese DNI del titular: ").strip()
    
    while not validar_dni(dni):
        print("\nDNI inválido. Formato esperado: 45873620 o 45.873.620\n")
        dni = input("Ingrese DNI del titular: ").strip()
    
    numero_telefono = input("Ingrese número de teléfono: ").strip()
    
    while not validar_telefono(numero_telefono):
        print("\nNúmero de teléfono inválido.\n")
    
    tipo_vehiculo = input("Ingrese tipo de vehículo (auto, moto, camioneta): ").lower()
    
    fecha_ingreso = input("Ingrese fecha de ingreso (AAAA-MM-DD): ")

    if not validar_fecha(fecha_ingreso):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        return
    
    fecha_salida = input("Ingrese fecha de salida (AAAA-MM-DD): ")

    if not validar_fecha(fecha_salida):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        return

    if fecha_ingreso > fecha_salida:
        print("La fecha de ingreso no puede ser mayor que la fecha de salida.")
        return
    
    reserva = {
        "patente": patente,
        "nombre": nombre,
        "dni": dni,
        "numero_telefono": numero_telefono,
        "fecha_ingreso": fecha_ingreso,
        "fecha_salida": fecha_salida,
        "tipo_vehiculo": tipo_vehiculo,
        "estado": "ACTIVA"
        }
    reservas_clientes.append(reserva)
    print("Reserva creada correctamente.")

def cancelar_reserva(reservas, matriz=None):
    """
    Cancela una reserva cambiando su estado a CANCELADA.
    """
    limpiar_pantalla()

    codigo_buscar = validar_entero("Ingrese el codigo de la reserva a cancelar: ", 1)

    for reserva in reservas:
        if reserva["codigo"] == codigo_buscar:
            if reserva["estado"] == "CANCELADA":
                print("La reserva ya estaba cancelada.")
                return

            fila = reserva["fila"]
            columna = reserva["columna"]

            if matriz is not None and fila is not None and columna is not None:
                if matriz[fila][columna] == "RESERVADA":
                    matriz[fila][columna] = "LIBRE"

            reserva["estado"] = "CANCELADA"
            print("Reserva cancelada correctamente.")
            return

    print("No se encontro una reserva con ese codigo.")


def modificar_reserva(reservas, matriz):
    """
    Modifica los datos de una reserva existente.
    """
    limpiar_pantalla()

    codigo_buscar = validar_entero("Ingrese el codigo de la reserva a modificar: ", 1)

    for reserva in reservas:
        if reserva["codigo"] == codigo_buscar:
            if reserva["estado"] == "CANCELADA":
                print("No se puede modificar una reserva cancelada.")
                return

            while True:
                print("\nModificaciones:")
                print("  1 - Cambiar patente")
                print("  2 - Cambiar nombre")
                print("  3 - Cambiar DNI")
                print("  4 - Cambiar numero de telefono")
                print("  5 - Cambiar fila y columna")
                print("  6 - Cambiar fecha de ingreso")
                print("  7 - Cambiar fecha de salida")
                print("  8 - Cambiar tipo de vehiculo")
                print("  9 - Volver")

                opcion = validar_entero("Seleccione la modificacion a realizar: ", 1, 9)

                match opcion:
                    case 1:
                        nueva_patente = input("Ingrese nueva patente: ").upper()

                        if not validar_patente(nueva_patente):
                            print("Patente invalida.")
                            continue

                        reserva["patente"] = nueva_patente

                    case 2:
                        reserva["nombre"] = input("Ingrese nuevo nombre: ").strip()

                    case 3:
                        reserva["dni"] = input("Ingrese nuevo DNI: ").strip()

                    case 4:
                        reserva["numero_telefono"] = input(
                            "Ingrese nuevo numero de telefono: "
                        ).strip()

                    case 5:
                        if not cambiar_plaza_reserva(reservas, matriz, reserva):
                            continue

                    case 6:
                        nueva_fecha = input(
                            "Ingrese nueva fecha de ingreso (AAAA-MM-DD): "
                        ).strip()

                        if not validar_fecha(nueva_fecha):
                            print("Fecha invalida.")
                            continue

                        if nueva_fecha > reserva["fecha_salida"]:
                            print("La fecha de ingreso no puede ser mayor que la fecha de salida.")
                            continue

                        if reserva["fila"] is not None and reserva["columna"] is not None:
                            disponible = verificar_disponibilidad(
                                reservas,
                                reserva["fila"],
                                reserva["columna"],
                                nueva_fecha,
                                reserva["fecha_salida"],
                                codigo_buscar,
                            )

                            if not disponible:
                                print("La plaza no esta disponible en esas fechas.")
                                continue

                        reserva["fecha_ingreso"] = nueva_fecha

                    case 7:
                        nueva_fecha = input(
                            "Ingrese nueva fecha de salida (AAAA-MM-DD): "
                        ).strip()

                        if not validar_fecha(nueva_fecha):
                            print("Fecha invalida.")
                            continue

                        if reserva["fecha_ingreso"] > nueva_fecha:
                            print("La fecha de ingreso no puede ser mayor que la fecha de salida.")
                            continue

                        if reserva["fila"] is not None and reserva["columna"] is not None:
                            disponible = verificar_disponibilidad(
                                reservas,
                                reserva["fila"],
                                reserva["columna"],
                                reserva["fecha_ingreso"],
                                nueva_fecha,
                                codigo_buscar,
                            )

                            if not disponible:
                                print("La plaza no esta disponible en esas fechas.")
                                continue

                        reserva["fecha_salida"] = nueva_fecha

                    case 8:
                        reserva["tipo_vehiculo"] = input(
                            "Ingrese el nuevo tipo de vehiculo (auto, moto, camioneta): "
                        ).lower()

                    case 9:
                        return

                if reserva["fecha_ingreso"] > reserva["fecha_salida"]:
                    print("La fecha de ingreso no puede ser mayor que la fecha de salida.")
                    continue

                print("Reserva modificada correctamente.")
                return

    print("No se encontro una reserva con ese codigo.")


def cambiar_plaza_reserva(reservas, matriz, reserva):
    """
    Cambia la plaza asignada a una reserva o asigna una si estaba pendiente.
    """
    fila_anterior = reserva["fila"]
    columna_anterior = reserva["columna"]

    mostrar_estacionamiento(matriz)

    nueva_fila = validar_entero("Ingrese nueva fila: ", 1, len(matriz)) - 1
    nueva_columna = validar_entero("Ingrese nueva columna: ", 1, len(matriz[0])) - 1

    if matriz[nueva_fila][nueva_columna] != "LIBRE":
        print("La plaza esta ocupada o reservada actualmente.")
        return False

    disponible = verificar_disponibilidad(
        reservas,
        nueva_fila,
        nueva_columna,
        reserva["fecha_ingreso"],
        reserva["fecha_salida"],
        reserva["codigo"],
    )

    if not disponible:
        print("La plaza no esta disponible en esas fechas.")
        return False

    if fila_anterior is not None and columna_anterior is not None:
        if matriz[fila_anterior][columna_anterior] == "RESERVADA":
            matriz[fila_anterior][columna_anterior] = "LIBRE"

    reserva["fila"] = nueva_fila
    reserva["columna"] = nueva_columna
    reserva["estado"] = "ACTIVA"
    matriz[nueva_fila][nueva_columna] = "RESERVADA"
    return True


def lista_reservas_activas(reservas):
    """
    Muestra todas las reservas pendientes y activas.
    """
    limpiar_pantalla()

    hay_reservas = False
    reservas_ordenadas = ordenar_reservas_fechas(reservas)

    print("\nLISTA DE RESERVAS")
    print("-" * 40)

    for reserva in reservas_ordenadas:
        if reserva["estado"] != "CANCELADA":
            hay_reservas = True
            fila = "Sin asignar"
            columna = "Sin asignar"

            if reserva["fila"] is not None:
                fila = reserva["fila"] + 1

            if reserva["columna"] is not None:
                columna = reserva["columna"] + 1

            print("Codigo:", reserva["codigo"])
            print("Patente:", reserva["patente"])
            print("Nombre:", reserva["nombre"])
            print("DNI:", reserva["dni"])
            print("Telefono:", reserva["numero_telefono"])
            print("Fila:", fila)
            print("Columna:", columna)
            print("Fecha ingreso:", reserva["fecha_ingreso"])
            print("Fecha salida:", reserva["fecha_salida"])
            print("Tipo de vehiculo:", reserva["tipo_vehiculo"])
            print("Estado:", reserva["estado"])
            print("-" * 40)

    if not hay_reservas:
        print("No hay reservas pendientes ni activas.")

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
        if reserva['estado'] == "ACTIVA":
            hay_activas = True
            print("Patente:",               reserva["patente"])
            print("Nombre:",                reserva["nombre"])
            print("DNI:",                   reserva["dni"])
            print("Teléfono:",              reserva["numero_telefono"])
            print("Tipo de vehículo:",      reserva["tipo_vehiculo"])
            print("Fecha de ingreso:",      reserva["fecha_ingreso"])
            print("Fecha de salida:",       reserva["fecha_salida"])
            print("Estado:",                reserva["estado"])
            print("-" * 40)

    if not hay_activas:
        print("No hay reservas activas.")

def ordenar_reservas_fechas(reservas):
    """
    Ordena las reservas por fecha de ingreso, de menor a mayor.
    """
    reservas_ordenadas = reservas[:]

    for i in range(len(reservas_ordenadas) - 1):
        for j in range(i + 1, len(reservas_ordenadas)):
            if reservas_ordenadas[i]["fecha_ingreso"] > reservas_ordenadas[j]["fecha_ingreso"]:
                aux = reservas_ordenadas[i]
                reservas_ordenadas[i] = reservas_ordenadas[j]
                reservas_ordenadas[j] = aux

    return reservas_ordenadas


def filtrar_por_fecha(reservas, fecha):
    """
    Devuelve reservas que comienzan en la fecha indicada.
    """
    return list(filter(lambda r: r["fecha_ingreso"] == fecha, reservas))


def filtrar_rango_fechas(reservas, fecha_ingreso, fecha_salida):
    """
    Devuelve reservas dentro del rango de fechas.
    """
    return list(filter(lambda r: r[4] >= fecha_ingreso and r[4] <= fecha_salida, reservas))


def filtrar_vehiculo_patente(vehiculos, patente):
    """
    Busca vehiculos que coincidan con la patente.
    """
    return list(filter(lambda v: v["patente"] == patente, vehiculos))


def buscar_fecha(reservas):
    """
    Permite elegir el tipo de busqueda o volver al menu anterior.
    """
    print("\nTipo de busqueda:")
    print("1 - Fecha exacta")
    print("2 - Rango de fechas")
    print("3 - Volver al menu anterior")

    opcion = validar_entero("Seleccione una opcion: ", 1, 3)

    if opcion == 1:
        buscar_por_fecha_exacta(reservas)
    elif opcion == 2:
        buscar_por_rango_fechas(reservas)
    elif opcion == 3:
        return


def buscar_por_fecha_exacta(reservas):
    """
    Busca reservas que coincidan con una fecha exacta.
    """
    fecha = input("Ingrese la fecha (AAAA-MM-DD): ")

    if validar_fecha(fecha) == False:
        print("Fecha invalida.")
        return

    reservas_filtradas = filtrar_por_fecha(reservas, fecha)
    lista_reservas_activas(reservas_filtradas)


def buscar_por_rango_fechas(reservas):
    """
    Busca reservas cuya fecha de ingreso este dentro de un rango.
    """
    fecha_ingreso = input("Ingrese fecha ingreso (AAAA-MM-DD): ")
    fecha_salida = input("Ingrese fecha salida (AAAA-MM-DD): ")

    fecha_ingreso = input("Ingrese fecha inicio (AAAA-MM-DD): ")
    fecha_salida = input("Ingrese fecha fin (AAAA-MM-DD): ")

    if validar_fecha(fecha_ingreso) == False:
        print("Fecha de inicio inválida.")
        return

    if validar_fecha(fecha_salida) == False:
        print("Fecha de fin inválida.")
        return

    if fecha_ingreso > fecha_salida:
        print("La fecha de inicio no puede ser mayor que la fecha de fin.")
        return

    reservas_filtradas = filtrar_rango_fechas(reservas, fecha_ingreso, fecha_salida)
    lista_reservas_activas(reservas_filtradas)


def asignar_plaza(reservas, matriz):
    """
    Asigna una plaza libre a una reserva pendiente.
    """
    limpiar_pantalla()

    codigo_buscar = validar_entero("Ingrese el codigo de la reserva: ", 1)
    reserva_encontrada = None

    for reserva in reservas:
        if reserva["codigo"] == codigo_buscar:
            reserva_encontrada = reserva
            break

    if reserva_encontrada is None:
        print("No se encontro una reserva con ese codigo.")
        return

    if reserva_encontrada["estado"] == "CANCELADA":
        print("No se puede asignar plaza a una reserva cancelada.")
        return

    if reserva_encontrada["estado"] == "ACTIVA":
        print("La reserva ya tiene una plaza asignada.")
        return

    mostrar_estacionamiento(matriz)

    fila = validar_entero("Ingrese fila: ", 1, len(matriz)) - 1
    columna = validar_entero("Ingrese columna: ", 1, len(matriz[0])) - 1

    if matriz[fila][columna] != "LIBRE":
        print("La plaza esta ocupada o reservada actualmente.")
        return

    disponible = verificar_disponibilidad(
        reservas,
        fila,
        columna,
        reserva_encontrada["fecha_ingreso"],
        reserva_encontrada["fecha_salida"],
        codigo_buscar,
    )

    if not disponible:
        print("La plaza no esta disponible en esas fechas.")
        return

    reserva_encontrada["fila"] = fila
    reserva_encontrada["columna"] = columna
    reserva_encontrada["estado"] = "ACTIVA"
    matriz[fila][columna] = "RESERVADA"
    print("La plaza fue reservada correctamente.")