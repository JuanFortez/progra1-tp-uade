# 📘 Proyecto "Programación 1 - UADE"

<p align="center">
<img src= "ParkingControl.png" alt="Logo de Estacionamiento" width="200"/>
</p>

---

## Integrantes

- **MENDES IGNACIO**
- **HYUN IAN**
- **SALAZAR SAMUEL**
- **OTTA SANTIAGO**
- **FORTEZ JUAN IGNACIO**

## Descripcion del proyecto

Este proyecto simula la gestión de estacionamiento y el control de ocupación, siendo una solución diseñada para optimizar la administración de plazas dentro de un estacionamiento. Su propósito es reemplazar los métodos manuales o poco estructurados utilizados habitualmente, permitiendo un control más claro y preciso sobre el estado de ocupación y la disponibilidad de los espacios.
El sistema facilita la gestión de reservas de diferentes duraciones —diarias, semanales, mensuales o anuales— evitando confusiones sobre la asignación de plazas y los períodos de uso. Además, permite registrar el tiempo de permanencia de los vehículos y visualizar en tiempo real qué espacios se encuentran ocupados y cuáles disponibles.
A través de esta herramienta, el administrador podrá organizar y supervisar el uso del estacionamiento de forma más eficiente, mientras que los clientes podrán asegurar su plaza mediante reservas. De esta manera, el sistema contribuye a mejorar la organización, optimizar la utilización del espacio y reducir errores asociados a la gestión manual.

## Funcionalidades
### Gestión del estacionamiento

Crear el estacionamiento con configuración de filas y columnas
Visualizar el estado actual del estacionamiento (plazas ocupadas y libres)
Consultar plazas ocupadas y plazas disponibles en tiempo real
Registrar el ingreso de vehículos (patente, plaza, tipo de auto)
Registrar la salida de vehículos

### Gestión de reservas

Crear reservas asignando patente, plaza y rango de fechas
Cancelar reservas existentes
Modificar reservas (patente, plaza y fechas)
Validar automáticamente la disponibilidad para evitar solapamiento de reservas
Listar reservas activas ordenadas por fecha de inicio
Solicitar reservas por parte del cliente, pendientes de confirmación por el administrador

### Roles de usuario

Rol administrador: acceso completo a todas las funcionalidades de gestión
Rol cliente: visualizar el estacionamiento y solicitar reservas


## Estructura
├── 📁 interfaz/                        # Interfaces de usuario
│   └── index.py                        # interfaz_inicio(), interfaz_admin(), interfaz_cliente()
├── 📁 gestion/                         # Lógica de gestión del estacionamiento
│   ├── index.py                        # Creación del estacionamiento e ingreso de vehículos
│   └── reservas.py                     # Crear, cancelar y modificar reservas
├── 📁 consultas/                       # Consultas y visualización
│   └── 📁 visualización/
│       └── index.py                    # Mostrar estado, plazas ocupadas y disponibles
├── 📄 main.py                          # Punto de entrada del sistema