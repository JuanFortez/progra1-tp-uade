def obtener_usuario_input():
    """Solicita el nombre de usuario."""
    while True:
        usuario = input("Ingrese su usuario (o -1 para salir): ").strip()
        if usuario == "":
            print("El usuario no puede estar vacío.")
        else:
            return usuario


def obtener_clave_input():
    """Solicita la clave del administrador."""
    while True:
        clave = input("Ingrese su clave (o -1 para salir): ").strip()
        if clave == "":
            print("La clave no puede estar vacía.")
        else:
            return clave


def crear_admin():
    """Crea las credenciales del administrador por primera vez."""
    print("No hay administrador registrado. Cree uno nuevo.")

    while True:
        usuario = input("Ingrese su nuevo usuario: ").strip()
        if not usuario or usuario == "-1":
            print('El usuario no puede estar vacío ni ser "-1".')
        else:
            break

    while True:
        clave = input("Ingrese su nueva clave: ").strip()
        if not clave or clave == "-1":
            print('La clave no puede estar vacía ni ser "-1".')
        else:
            break

    return {"usuario": usuario, "clave": clave}


def login(admin):
    """Maneja el inicio de sesión del administrador.
    Retorna True si el login es exitoso, False si cancela.
    """
    usuario = obtener_usuario_input()

    if usuario == "-1":
        return False

    if usuario != admin["usuario"]:
        print("Usuario incorrecto. Intente de nuevo.")
        return False

    while True:
        clave = obtener_clave_input()

        if clave == "-1":
            print("Acceso cancelado.")
            return False

        if clave == admin["clave"]:
            return True

        print("Clave incorrecta. Intente de nuevo.")