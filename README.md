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
El sistema facilita la gestión de reservas mediante asignación de fechas específicas, evitando confusiones sobre la asignación de plazas y los períodos de uso. Además, permite registrar el tiempo de permanencia de los vehículos y visualizar en tiempo real qué espacios se encuentran ocupados y cuáles disponibles, con cálculo automático de tarifas diferenciadas por tipo de vehículo.
A través de esta herramienta, el administrador podrá organizar y supervisar el uso del estacionamiento de forma más eficiente. De esta manera, el sistema contribuye a mejorar la organización, optimizar la utilización del espacio y reducir errores asociados a la gestión manual.

## Funcionalidades

### Gestión del estacionamiento

- Crear el estacionamiento con configuración de filas y columnas (4 diseños disponibles: rectangular, 2 columnas, doble pasillo, forma U).
- Visualizar el estado actual del estacionamiento (⬜ Libre, 🟥 Ocupada, 🟧 Reservada).
- Consultar plazas ocupadas y plazas disponibles en tiempo real.
- Registrar el ingreso de vehículos (patente, plaza, tipo de vehículo).
- Registrar la salida de vehículos con cálculo automático de tarifa según tipo.
- Buscar vehículos por patente.
- Modificar el estado de una plaza (patente, tipo, estado).
- Consultar historial completo de movimientos.

### Gestión de reservas

- Crear reservas asignando patente, plaza, cliente y rango de fechas.
- Cancelar reservas existentes.
- Modificar reservas (patente, plaza y fechas).
- Validar automáticamente la disponibilidad para evitar solapamiento de reservas.
- Listar reservas activas ordenadas por fecha de inicio.
- Buscar reservas por fecha exacta, rango de fechas o cliente (nombre, DNI, patente).
- Asignar plazas a reservas pendientes de clientes.
- Solicitar reservas por parte del cliente (requieren asignación de plaza por parte del administrador).
- Buscar reservas por cliente (nombre, DNI o patente), integrando datos de reservas del administrador y del cliente.

### Roles de usuario

- **Rol administrador:** acceso completo a todas las funcionalidades de gestión.
- **Rol cliente:** puede solicitar reservas ingresando sus datos. La reserva queda pendiente hasta que el administrador le asigne una plaza.

## Estructura

```
├── 📁 interfaz/                        # Interfaces de usuario
│   └── index.py                        # Interfaces de inicio, admin y cliente
├── 📁 gestion/                         # Lógica de gestión del estacionamiento
│   ├── index.py                        # Creación del estacionamiento e ingreso/egreso de vehículos
│   └── reservas.py                     # Crear, cancelar, modificar y consultar reservas
├── 📁 consultas/                       # Consultas y visualización
│   ├── 📁 constantes/                  # Constantes del sistema
│   │   └── index.py                    # Estados, tipos de vehículo, multiplicadores de tarifa
│   ├── 📁 validacion/                  # Validación de datos de entrada
│   │   └── index.py                    # Valida formato de patentes, fechas, DNI y teléfonos
│   └── 📁 visualizacion/               # Visualización del estado del estacionamiento
│       └── index.py                    # Mostrar estado, plazas ocupadas y disponibles
├── 📁 datos/                           # Persistencia de datos
│   ├── persistencia.py                 # Carga y guarda el estado en JSON
│   └── datos_estacionamiento.json      # Archivo de datos persistente
├── 📁 logs/                            # Registro de eventos
│   └── index.py                        # Escritura y lectura de logs
├── 📁 tests/                           # Pruebas unitarias
│   ├── test_gestion.py                 # Pruebas de tarifas, mapa de plazas y tipos de estacionamiento
│   ├── test_reservas.py                # Pruebas de disponibilidad, filtros y clientes
│   ├── test_validacion.py              # Pruebas de validación de patentes, fechas, DNI y teléfono
│   └── test_visualizacion.py           # Pruebas de conteo de plazas ocupadas y disponibles
├── 📁 ui/                              # Utilidades básicas de interfaz
│   └── index.py                        # Menús y funciones de presentación
├── 📄 logs.txt                         # Archivo de logs del sistema
├── 📄 .gitignore
├── 📄 main.py                          # Punto de entrada del sistema
```

## Características NO implementadas

- Categorización de reservas por duración (diaria, semanal, mensual, anual)
- Visualización del estacionamiento para clientes
- Gestión de reservas existentes por parte del cliente (cancelar, modificar)
- Notificaciones o recordatorios de reservas próximas a vencer

## Limitaciones y Notas técnicas

- **Persistencia de datos**: Los datos se guardan automáticamente en `datos/datos_estacionamiento.json` al realizar cada acción relevante (ingreso, egreso, reservas, modificaciones).
- **Logs**: Cada acción importante queda registrada con fecha y hora en `logs.txt`.
- **Tipos de vehículo**: AUTO, MOTO y CAMIONETA.
- **Cálculo de tarifa**: $1000 primera hora + $250 por cada 15 minutos adicionales, con multiplicador según tipo de vehículo (MOTO: ×0.5, AUTO: ×1.0, CAMIONETA: ×2.0).
- **Validación de patentes**: Formatos aceptados: ABC123 (patente vieja) o AB123CD (patente nueva).
- **Validación de fechas**: Formato AAAA-MM-DD con validación de fechas válidas (considerando años bisiestos).
- **Validación de teléfonos**: Se verifican prefijos argentinos válidos. No se acepta el 0 ni el 15.
- **Validación de DNI**: Acepta formato con o sin puntos, de 7 u 8 dígitos.
- **Reservas de clientes**: Las reservas solicitadas por clientes quedan en estado PENDIENTE hasta que el administrador les asigne una plaza manualmente.
- **Modificación del estacionamiento**: No se puede modificar la estructura mientras hay vehículos estacionados. Si hay reservas activas, se advierte que sus coordenadas quedarán inválidas.
- **Portabilidad**: El sistema no usa rutas absolutas; todas las rutas se construyen de forma relativa usando `pathlib`, por lo que funciona en cualquier computadora.