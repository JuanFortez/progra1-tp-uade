from consultas.validacion.index import validar_entero, validar_fecha, validar_patente, validar_dni, validar_telefono
from consultas.visualizacion.index import mostrar_estacionamiento
from ui.index import limpiar_pantalla


def verificar_disponibilidad(
    reservas, fila, columna, fecha_ingreso, fecha_salida, codigo_excluir=-1
):
    """
    Verifica si una plaza está disponible entre dos fechas.
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
    Crea una nueva reserva si la plaza está disponible.
    """
    limpiar_pantalla()

    patente = input("Ingrese la patente (ej: ABC123 o AB123CD): ").upper()

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

    if fecha_ingreso > fecha_salida:
        print("La fecha de ingreso no puede ser mayor que la fecha de salida.")
        return

    disponible = verificar_disponibilidad(
        reservas, fila, columna, fecha_ingreso, fecha_salida
    )

    if disponible:
        codigo = len(reservas) + 1
        reserva = {
            "codigo": codigo,
            "patente": patente,
            "nombre": nombre,
            "dni": dni,
            "numero_telefono": numero_telefono,
            "fila": fila,
            "columna": columna,
            "fecha_ingreso": fecha_ingreso,
            "fecha_salida": fecha_salida,
            "tipo_vehiculo": tipo_vehiculo,
            "estado": "ACTIVA"
        }
        reservas.append(reserva)
        print("Reserva creada correctamente.")
    else:
        print("La plaza no está disponible en esas fechas.")

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

def cancelar_reserva(reservas):
    """
    Cancela una reserva cambiando su estado a CANCELADA.
    """
    limpiar_pantalla()

    codigo_buscar = validar_entero("Ingrese el código de la reserva a cancelar: ", 1)

    for reserva in reservas:
        if reserva[0] == codigo_buscar:
            if reserva[6] == "CANCELADA":
                print("La reserva ya estaba cancelada.")
                return

            reserva[6] = "CANCELADA"
            print("Reserva cancelada correctamente.")
            return

    print("No se encontró una reserva con ese código.")


def modificar_reserva(reservas, matriz):
    """
    Modifica los datos de una reserva existente.
    """
    limpiar_pantalla()

    codigo_buscar = validar_entero("Ingrese el código de la reserva a modificar: ", 1)

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
                print("  4 - Cambiar número de teléfono")
                print("  5 - Cambiar fila y columna")
                print("  6 - Cambiar fecha de ingreso")
                print("  7 - Cambiar fecha de salida")
                print("  8 - Cambiar tipo de vehiculo")
                print("  9 - Volver")

                opcion = validar_entero("Seleccione la modificación a realizar: ", 1, 5)

                match opcion:
                    case 1:
                        nueva_patente = input("Ingrese nueva patente: ").upper()

                        if not validar_patente(nueva_patente):
                            print("Patente inválida.")
                            continue
                        reserva["patente"] = nueva_patente
                        
                    case 2:
                        nuevo_nombre = input("Ingrese nuevo nombre: ").strip()
                        
                        reserva["nombre"] = nuevo_nombre
                        
                    case 3:
                        nuevo_dni = input("Ingrese nuevo DNI: ").strip()
                        
                        reserva["dni"] = nuevo_dni
                        
                    case 4:
                        nuevo_telefono = input("Ingrese nuevo número de teléfono: ").strip()
                        
                        reserva["numero_telefono"] = nuevo_telefono
                        
                    case 5:
                        nueva_fila = (
                            validar_entero("Ingrese nueva fila: ", 1, len(matriz)) - 1
                        )
                        nueva_columna = (
                            validar_entero("Ingrese nueva columna: ", 1, len(matriz[0]))
                            - 1
                        )
                        
                        reserva["fila"] = nueva_fila
                        reserva["columna"] = nueva_columna

                    case 6:
                        nueva_fecha = input(
                            "Ingrese nueva fecha de inicio (AAAA-MM-DD): "
                        ).strip()

                        if not validar_fecha(nueva_fecha):
                            print("Fecha inválida.")
                            continue
                        reserva["fecha_ingreso"] = nueva_fecha

                    case 7:
                        nueva_fecha = input(
                            "Ingrese nueva fecha de fin (AAAA-MM-DD): "
                        ).strip()

                        if not validar_fecha(nueva_fecha):
                            print("Fecha inválida.")
                            continue
                        reserva["fecha_salida"] = nueva_fecha
                        
                    case 8:
                        nuevo_tipo_vehiculo = input("Ingrese el nuevo tipo de vehículo (auto, moto, camioneta): ").lower()
                        
                        reserva["tipo_vehiculo"] = nuevo_tipo_vehiculo

                if reserva["fecha_ingreso"] > reserva["fecha_salida"]:
                    print("La fecha de ingreso no puede ser mayor que la fecha de salida.")
                    continue

                disponible = verificar_disponibilidad(
                    reservas,
                    reserva["fila"],
                    reserva["columna"],
                    reserva["fecha_ingreso"],
                    reserva["fecha_salida"],
                    codigo_buscar,
                )

                if disponible:
                    print("Reserva modificada correctamente.")
                else:
                    print("La plaza no está disponible en esas fechas.")

                return

    print("No se encontró una reserva con ese código.")


def lista_reservas_activas(reservas):
    """
    Muestra todas las reservas activas.
    """
    limpiar_pantalla()

    hay_activas = False
    reservas_ordenadas = ordenar_reservas_fechas(reservas)

    print("\nLISTA DE RESERVAS ACTIVAS")
    print("-" * 40)

    for reserva in reservas_ordenadas:
        if reserva[6] == "ACTIVA":
            hay_activas = True
            print("Código:", reserva[0])
            print("Patente:", reserva[1])
            print("Fila:", reserva[2] + 1)
            print("Columna:", reserva[3] + 1)
            print("Fecha inicio:", reserva[4])
            print("Fecha fin:", reserva[5])
            print("Estado:", reserva[6])
            print("-" * 40)

    if not hay_activas:
        print("No hay reservas activas.")

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
    Ordena las reservas por fecha de inicio, de menor a mayor.
    """

    reservas_ordenadas = reservas[:]

    for i in range(len(reservas_ordenadas) - 1):
        for j in range(i + 1, len(reservas_ordenadas)):
            if reservas_ordenadas[i][4] > reservas_ordenadas[j][4]:
                aux = reservas_ordenadas[i]
                reservas_ordenadas[i] = reservas_ordenadas[j]
                reservas_ordenadas[j] = aux

    return reservas_ordenadas


def filtrar_por_fecha(reservas, fecha):
    """
    Devuelve reservas que comienzan en la fecha indicada
    """
    return list(filter(lambda r: r[4] == fecha, reservas))


def filtrar_rango_fechas(reservas, fecha_ingreso, fecha_salida):
    """
    Devuelve reservas dentro del rango de fechas
    """
    return list(filter(lambda r: r[4] >= fecha_ingreso and r[4] <= fecha_salida, reservas))


def filtrar_vehiculo_patente(vehiculos, patente):
    """
    Busca vehículos que coincidan con la patente
    """
    return list(filter(lambda v: v[0] == patente, vehiculos))


def buscar_fecha(reservas):
    """
    Permite elegir el tipo de búsqueda o volver al menú anterior
    """
    print("\nTipo de búsqueda:")
    print("1 - Fecha exacta")
    print("2 - Rango de fechas")
    print("3 - Volver al menú anterior")

    opcion = validar_entero("Seleccione una opción: ", 1, 3)

    if opcion == 1:
        buscar_por_fecha_exacta(reservas)
    elif opcion == 2:
        buscar_por_rango_fechas(reservas)
    elif opcion == 3:
        return


def buscar_por_fecha_exacta(reservas):
    """
    Busca reservas que coincidan con una fecha exacta
    """

    fecha = input("Ingrese la fecha (AAAA-MM-DD): ")

    if validar_fecha(fecha) == False:
        print("Fecha inválida.")
        return

    reservas_filtradas = filtrar_por_fecha(reservas, fecha)
    lista_reservas_activas(reservas_filtradas)


def buscar_por_rango_fechas(reservas):
    """
    Busca reservas cuya fecha de inicio esté dentro de un rango
    """

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
