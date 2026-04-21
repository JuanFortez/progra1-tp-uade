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
El sistema facilita la gestión de reservas mediante asignación de fechas específicas, evitando confusiones sobre la asignación de plazas y los períodos de uso. Además, permite registrar el tiempo de permanencia de los vehículos y visualizar en tiempo real qué espacios se encuentran ocupados y cuáles disponibles, con cálculo automático de tarifas.
A través de esta herramienta, el administrador podrá organizar y supervisar el uso del estacionamiento de forma más eficiente. De esta manera, el sistema contribuye a mejorar la organización, optimizar la utilización del espacio y reducir errores asociados a la gestión manual.

## Funcionalidades

### Gestión del estacionamiento

Crear el estacionamiento con configuración de filas y columnas.
Visualizar el estado actual del estacionamiento (plazas ocupadas y libres).
Consultar plazas ocupadas y plazas disponibles en tiempo real.
Registrar el ingreso de vehículos (patente, plaza).
Registrar la salida de vehículos con cálculo automático de tarifa.

### Gestión de reservas

Crear reservas asignando patente, plaza y rango de fechas.
Cancelar reservas existentes.
Modificar reservas (patente, plaza y fechas).
Validar automáticamente la disponibilidad para evitar solapamiento de reservas.
Listar reservas activas ordenadas por fecha de inicio.
Solicitar reservas por parte del cliente, actualmente creadas sin aprobación del administrador.

### Roles de usuario

Rol administrador: acceso completo a todas las funcionalidades de gestión.
Rol cliente: solicitar reservas (sin acceso a visualización del estacionamiento ni gestión de reservas existentes).

## Estructura

```
├── 📁 interfaz/                        # Interfaces de usuario
│   └── index.py                        # Se muestran las interfaces de inicio, admin y cliente
├── 📁 gestion/                         # Lógica de gestión del estacionamiento
│   ├── index.py                        # Creación del estacionamiento e ingreso de vehículos
│   └── reservas.py                     # Crear, cancelar y modificar reservas
├── 📁 consultas/                       # Consultas y visualización
│   ├── 📁 validacion/                  # Validación de datos de entrada
│   │   └── index.py                    # Valida formato de patentes y fechas, y enteros en inputs
│   └── 📁 visualizacion/               # Visualización del estado del estacionamiento
│       └── index.py                    # Mostrar estado, plazas ocupadas y disponibles
├── 📁 ui/                              # Utilidades básicas de interfaz
├── 📄 .gitignore
├── 📄 main.py                          # Punto de entrada del sistema
```

## Características NO implementadas

- Categorización de reservas por duración (diaria, semanal, mensual, anual)
- Tipo de vehículo (solo se captura patente y plaza)
- Sistema de aprobación de reservas por administrador (se crean activas directamente)
- Visualización del estacionamiento para clientes
- Gestión de reservas existentes por parte del cliente
- Historial de transacciones y reportes de ocupación

## Limitaciones y Notas técnicas

- **Persistencia de datos**: Los datos (reservas y registros de vehículos) se almacenan en memoria y se pierden al cerrar la aplicación. No hay base de datos ni archivos persistentes por el momento.
- **Cálculo de tarifa**: $1000 primera hora + $500 por cada hora adicional.
- **Validación de patentes**: Formatos aceptados: ABC123 o AB123CD
- **Validación de fechas**: Formato AAAA-MM-DD con validación de fechas válidas (considerando años bisiestos)
