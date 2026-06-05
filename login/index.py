def login(admin):
    if admin is None:
        usuario = input("Ingrese su nuevo usuario: ").strip()
        while usuario == "-1" or usuario == "":
            if usuario == "":
                print("El usuario no puede estar vacío.")
            else:
                print('El usuario no puede ser "-1".')
            usuario = input("Ingrese su nuevo usuario: ").strip()

        clave = input("Ingrese su nueva clave: ").strip()
        while clave == "-1" or clave == "":
            if clave == "":
                print("La clave no puede estar vacía.")
            else:
                print('La clave no puede ser "-1".')
            clave = input("Ingrese su nueva clave: ").strip()

        admin = {"usuario": usuario, "clave": clave}
        return admin
    else:
        while True:
            usuario = input("Ingrese su usuario (o -1 para salir): ").strip()
            if usuario == "-1":
                return None

            if usuario == admin["usuario"]:
                while True:
                    clave = input("Ingrese su clave (o -1 para salir): ").strip()
                    if clave == "-1":
                        return None
                    if clave == admin["clave"]:
                        return admin
                    print("Clave incorrecta. Intente de nuevo.")
            else:
                print("Usuario incorrecto. Intente de nuevo.")

