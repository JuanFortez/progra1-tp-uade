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

    patente = input("Ingrese la patente: ").upper()
    fila = int(input("Ingrese fila: "))
    columna = int(input("Ingrese columna: "))
    fecha_inicio = input("Ingrese fecha de inicio (AAAA-MM-DD): ")
    fecha_fin = input("Ingrese fecha de fin (AAAA-MM-DD): ")

    if fila < 0 or fila >= len(matriz) or columna < 0 or columna >= len(matriz[0]):
        print("La plaza no existe.")
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

    codigo_buscar = int(input("Ingrese el código de la reserva a cancelar: "))

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

    codigo_buscar = int(input("Ingrese el código de la reserva a modificar: "))

    for reserva in reservas:
        if reserva[0] == codigo_buscar:
            if reserva[6] == "CANCELADA":
                print("No se puede modificar una reserva cancelada.")
                return

            nueva_patente = input("Ingrese nueva patente: ").upper()
            nueva_fila = int(input("Ingrese nueva fila: "))
            nueva_columna = int(input("Ingrese nueva columna: "))
            nueva_fecha_inicio = input("Ingrese nueva fecha de inicio (AAAA-MM-DD): ")
            nueva_fecha_fin = input("Ingrese nueva fecha de fin (AAAA-MM-DD): ")

            if (
                nueva_fila < 0
                or nueva_fila >= len(matriz)
                or nueva_columna < 0
                or nueva_columna >= len(matriz[0])
            ):
                print("La plaza no existe.")
                return

            if nueva_fecha_inicio > nueva_fecha_fin:
                print("La fecha de inicio no puede ser mayor que la fecha de fin.")
                return

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

    hay_activas = False

    print("\nLISTA DE RESERVAS ACTIVAS")
    print("-" * 40)

    for reserva in reservas:
        if reserva[6] == "ACTIVA":
            hay_activas = True
            print("Código:", reserva[0])
            print("Patente:", reserva[1])
            print("Fila:", reserva[2])
            print("Columna:", reserva[3])
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
