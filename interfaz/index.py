from gestion.index import crear_estacionamiento, registrar_ingreso_vehiculo, registrar_salida_vehiculo
from consultas.visualización.index import mostrar_estacionamiento
from ui.index import encabezado_principal
from time import sleep


def interfaz_inicio():
    
    print("🚗" * 19)
    print(" " * 5 + "BIENVENIDO A PARKING CONTROL")
    print("🚗" * 19)
    
    while True:
        print("\n" + "=" * 40)
        print(" " * 13 + "MENÚ PRINCIPAL")
        print("=" * 40)
        print("\n  1 - Panel Administrador")
        print("  2 - Panel Cliente")
        print("  3 - Salir\n")
        
        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 1:
            print("Accediendo a panel de administración...")
            interfaz_admin()
            
        elif opcion == 2:
            print("Accediendo a panel de cliente...")
            interfaz_cliente()
            
        elif opcion == 3:
            print("\n👋 ¡Gracias por usar Parking Control!")
            print("🚗 ¡Hasta la próxima!")
            sleep(2)
            break

    
def interfaz_admin():
    encabezado_principal() 
    
    matriz = crear_estacionamiento()
    mostrar_estacionamiento(matriz)
    
    while True:
        print("\n" + "=" * 39)
        print(" " * 8 + "PANEL DE ADMINISTRACIÓN") 
        print("=" * 39)
        
        print("\n  1 - Registrar ingreso de vehículo")
        print("  2 - Registrar egreso de vehículo")
        print("  3 - Ver ocupación actual")
        print("  4 - Buscar vehículo")
        print("  9 - Salir\n")
        
        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 1:
            print("Ingreso de vehiculo...")
            registrar_ingreso_vehiculo(matriz)
            
        elif opcion == 2:
            print("Salida de vehiculo...")
            registrar_salida_vehiculo(matriz)
            
        elif opcion == 3:
            print("Estado de estacionamiento...")
            mostrar_estacionamiento(matriz)
            
        elif opcion == 4:
            pass
            
        elif opcion == 9:
            print("\n👋 Saliendo del panel de administración...")
            sleep(2)
            break
        
def interfaz_cliente():
    encabezado_principal()
    
    while True:    
        print("\n=== PANEL DE CLIENTE ===\n")
        print("  1 - Solicitar reserva")
        print("  2 - Salir\n")
        
        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 1:
            pass
        
        elif opcion == 2:
            print("\n👋 ¡Gracias por usar Parking Control!")
            print("🚗 Saliendo del panel de cliente...")
            sleep(2)
            break
            

