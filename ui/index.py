import os


def encabezado_principal():
    """
    Crea el encabezado del menu principal.
    """
    print("\n" + "=" * 40)
    print(" " * 7 + "SISTEMA DE ESTACIONAMIENTO")
    print("=" * 40)


def limpiar_pantalla() -> None:
    """Limpia la pantalla de consola."""
    # Para sistemas Windows
    if os.name == "nt":
        _ = os.system("cls")
    # Para sistemas Unix (Linux, macOS)
    else:
        _ = os.system("clear")

def lista_menu_principal():
    print("\n" + "=" * 40)
    print(" " * 13 + "MENÚ PRINCIPAL")
    print("=" * 40)
    print("\n  1 - Panel Administrador")
    print("  2 - Panel Cliente")
    print("  3 - Salir\n")
    
def lista_panel_administracion():
    print("\n" + "=" * 39)
    print(" " * 8 + "PANEL DE ADMINISTRACIÓN")
    print("=" * 39)

    print("\n  1 - Registrar ingreso de vehículo")
    print("  2 - Registrar egreso de vehículo")
    print("  3 - Ver ocupación actual")
    print("  4 - Buscar vehículo")
    print("  5 - Modificar plaza")
    print("  6 - Gestionar reservas")
    print("  7 - Ver historial")
    print("  8 - Modificar estacionamiento")
    print("  9 - Ver estadísticas")
    print(" 10 - Volver\n")
    
def lista_panel_cliente():
    print("\n=== PANEL DE CLIENTE ===\n")
    print("  1 - Solicitar reserva")
    print("  2 - Salir\n")
    
def lista_reservas_admin():
    print("\n" + "=" * 40)
    print(" " * 10 + "GESTIÓN DE RESERVAS")
    print("=" * 40)
    print("\n  1 - Crear reserva")
    print("  2 - Cancelar reserva")
    print("  3 - Modificar reserva")
    print("  4 - Ver reservas activas")
    print("  5 - Ver reservas de clientes")
    print("  6 - Buscar reservas por fecha")
    print("  7 - Buscar reservas por cliente")
    print("  8 - Asignar plaza")
    print("  9 - Gestionar abonos")
    print(" 10 - Volver\n")
    
def lista_crear_estacionamiento():
    print("\nSeleccione el tipo de plano del estacionamiento:\n")
    print("  1 - Rectangular manual")
    print("  2 - Dos columnas con pasillo central")
    print("  3 - Doble pasillo")
    print("  4 - En U\n")

def lista_modificar_estado_plaza():
    print("\nModificaciones:")
    print("  1 - Cambiar patente")
    print("  2 - Cambiar tipo de vehículo")
    print("  3 - Cambiar estado")
    print("  4 - Volver")
    
def lista_modificar_reserva():
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


def lista_abonos_admin():
    print("\n" + "=" * 40)
    print(" " * 11 + "GESTIÓN DE ABONOS")
    print("=" * 40)
    print("\n  1 - Crear abono")
    print("  2 - Listar abonos activos")
    print("  3 - Cancelar abono")
    print("  4 - Ver tabla de tarifas y descuentos")
    print("  5 - Volver\n")


def tabla_tarifas_abono():
    from consultas.constantes.index import (
        TIPOS_ABONO, DESCUENTOS_ABONO, TARIFA_DIARIA_RESERVA, MULTIPLICADORES_TARIFA
    )
    print("\n" + "=" * 55)
    print(" " * 12 + "TARIFAS DE ABONO CON DESCUENTO")
    print("=" * 55)
    print(f"\n  Tarifa diaria base: ${TARIFA_DIARIA_RESERVA:.0f}/día")
    print(f"\n  {'Tipo':<12} {'Días':<8} {'Descuento':<12} {'AUTO':<12} {'MOTO':<10} {'CAMIONETA'}")
    print("  " + "-" * 53)
    for tipo, dias in TIPOS_ABONO.items():
        desc = DESCUENTOS_ABONO[tipo]
        for vehiculo, mult in MULTIPLICADORES_TARIFA.items():
            tarifa = TARIFA_DIARIA_RESERVA * dias * mult * (1 - desc)
            if vehiculo == "AUTO":
                auto = f"${tarifa:.0f}"
            elif vehiculo == "MOTO":
                moto = f"${tarifa:.0f}"
            else:
                camioneta = f"${tarifa:.0f}"
        print(f"  {tipo:<12} {dias:<8} {int(desc*100)}%{'':9} {auto:<12} {moto:<10} {camioneta}")
    print("=" * 55)
    
def lista_historial():
    """
    Muestra las opciones del menú de historial.
    """
    print("\n" + "=" * 40)
    print(" " * 15 + "HISTORIAL")
    print("=" * 40)

    print("\n  1 - Ver historial completo")
    print("  2 - Buscar por patente")
    print("  3 - Buscar por fecha")
    print("  4 - Ordenar por monto")
    print("  5 - Volver\n")