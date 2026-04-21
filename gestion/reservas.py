from consultas.validacion.index import validar_entero, validar_fecha, validar_patente
from consultas.visualizacion.index import mostrar_estacionamiento
from ui.index import limpiar_pantalla


def verificar_disponibilidad(
    reservas, fila, columna, fecha_inicio, fecha_fin, codigo_excluir=-1
):
    """
    Verifica si una plaza está disponible entre dos fechas.
    """

    for reserva in reservas:
        codigo = reserva[0]
        fila_reserva = reserva[2]
        columna_reserva = reserva[3]
        inicio_reserva = reserva[4]
        fin_reserva = reserva[5]
        estado = reserva[6]

        if codigo != codigo_excluir:
            if estado == "ACTIVA":
                if fila_reserva == fila and columna_reserva == columna:
                    if not (fecha_fin < inicio_reserva or fecha_inicio > fin_reserva):
                        return False

    return True


def crear_reserva(reservas, matriz):
    """
    Crea una nueva reserva si la plaza está disponible.
    """
    limpiar_pantalla()

    patente = input("Ingrese la patente (ej: ABC123 o AB123CD): "   ).upper()

    if not validar_patente(patente):
        print("\nPatente inválida. Formato esperado: ABC123 o AB123CD")
        return

    mostrar_estacionamiento(matriz)

    fila = validar_entero("Ingrese fila: ", 1, len(matriz)) - 1
    columna = validar_entero("Ingrese columna: ", 1, len(matriz[0])) - 1

    fecha_inicio = input("Ingrese fecha de inicio (AAAA-MM-DD): ")

    if not validar_fecha(fecha_inicio):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        return
    fecha_fin = input("Ingrese fecha de fin (AAAA-MM-DD): ")

    if not validar_fecha(fecha_fin):
        print("Fecha inválida. Formato esperado: AAAA-MM-DD")
        return

    if fecha_inicio > fecha_fin:
        print("La fecha de inicio no puede ser mayor que la fecha de fin.")
        return

    disponible = verificar_disponibilidad(
        reservas, fila, columna, fecha_inicio, fecha_fin
    )

    if disponible:
        codigo = len(reservas) + 1
        reserva = [codigo, patente, fila, columna, fecha_inicio, fecha_fin, "ACTIVA"]
        reservas.append(reserva)
        print("Reserva creada correctamente.")
    else:
        print("La plaza no está disponible en esas fechas.")


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
        if reserva[0] == codigo_buscar:
            if reserva[6] == "CANCELADA":
                print("No se puede modificar una reserva cancelada.")
                return

            nueva_patente = reserva[1]
            nueva_fila = reserva[2]
            nueva_columna = reserva[3]
            nueva_fecha_inicio = reserva[4]
            nueva_fecha_fin = reserva[5]

            while True:
                print("\nModificaciones:")
                print("  1 - Cambiar patente")
                print("  2 - Cambiar fila y columna")
                print("  3 - Cambiar fecha de inicio")
                print("  4 - Cambiar fecha de finalización")
                print("  5 - Volver")

                opcion = validar_entero("Seleccione la modificación a realizar: ", 1, 5)

                match opcion:
                    case 1:
                        nueva_patente = input("Ingrese nueva patente: ").upper()

                        if not validar_patente(nueva_patente):
                            print("Patente inválida.")
                            continue
                    case 2:
                        nueva_fila = (
                            validar_entero("Ingrese nueva fila: ", 1, len(matriz)) - 1
                        )
                        nueva_columna = (
                            validar_entero("Ingrese nueva columna: ", 1, len(matriz[0]))
                            - 1
                        )

                    case 3:
                        nueva_fecha_inicio = input(
                            "Ingrese nueva fecha de inicio (AAAA-MM-DD): "
                        ).strip()

                        if not validar_fecha(nueva_fecha_inicio):
                            print("Fecha inválida.")
                            continue

                    case 4:
                        nueva_fecha_fin = input(
                            "Ingrese nueva fecha de fin (AAAA-MM-DD): "
                        ).strip()

                        if not validar_fecha(nueva_fecha_fin):
                            print("Fecha inválida.")
                            continue

                if nueva_fecha_inicio > nueva_fecha_fin:
                    print("La fecha de inicio no puede ser mayor que la fecha de fin.")
                    continue

                disponible = verificar_disponibilidad(
                    reservas,
                    nueva_fila,
                    nueva_columna,
                    nueva_fecha_inicio,
                    nueva_fecha_fin,
                    codigo_buscar,
                )

                if disponible:
                    reserva[1] = nueva_patente
                    reserva[2] = nueva_fila
                    reserva[3] = nueva_columna
                    reserva[4] = nueva_fecha_inicio
                    reserva[5] = nueva_fecha_fin
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


def filtrar_rango_fechas(reservas, fecha_inicio, fecha_fin):
    """
    Devuelve reservas dentro del rango de fechas
    """
    return list(filter(lambda r: r[4] >= fecha_inicio and r[4] <= fecha_fin, reservas))


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

    if opcion == 0:
        return

    elif opcion == 1:
        buscar_por_fecha_exacta(reservas)
    else:
        buscar_por_rango_fechas(reservas)

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

    fecha_inicio = input("Ingrese fecha inicio (AAAA-MM-DD): ")
    fecha_fin = input("Ingrese fecha fin (AAAA-MM-DD): ")

    if validar_fecha(fecha_inicio) == False:
        print("Fecha de inicio inválida.")
        return

    if validar_fecha(fecha_fin) == False:
        print("Fecha de fin inválida.")
        return

    if fecha_inicio > fecha_fin:
        print("La fecha de inicio no puede ser mayor que la fecha de fin.")
        return

    reservas_filtradas = filtrar_rango_fechas(reservas, fecha_inicio, fecha_fin)
    lista_reservas_activas(reservas_filtradas)

