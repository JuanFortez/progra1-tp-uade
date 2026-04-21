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
