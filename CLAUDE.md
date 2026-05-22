# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexto del proyecto

Proyecto de Programación 1 en Python para UADE. El objetivo es una solución correcta, prolija y defendible para una entrega universitaria — no la más profesional posible. El código debe ser simple y fácil de explicar oralmente en una defensa.

## Cómo ejecutar

```bash
python main.py
```

Sin dependencias externas. Solo biblioteca estándar de Python. No hay tests automáticos ni linter configurado.

## Nivel de código permitido

Usar preferentemente:
- funciones, condicionales, bucles `for` y `while`
- listas, tuplas, diccionarios, matrices (listas anidadas)
- strings y sus métodos básicos
- validaciones con funciones simples
- módulos separados (la estructura actual ya los define)

**Evitar salvo pedido explícito del usuario:**
- clases y programación orientada a objetos
- decoradores, `async`/`await`
- frameworks, bases de datos, APIs
- patrones de diseño avanzados
- dependencias externas
- cualquier solución que parezca de nivel profesional avanzado

## Forma de trabajo

Antes de modificar archivos:
1. Analizar el problema y explicar qué está mal.
2. Indicar qué archivo se va a tocar.
3. Proponer el cambio mínimo necesario.
4. Pedir confirmación si el cambio es grande o afecta varias partes del proyecto.

Al hacer cambios:
- Modificar solo lo necesario. No reescribir lo que funciona.
- No cambiar nombres de funciones existentes sin necesidad.
- No cambiar la arquitectura general sin permiso.
- No borrar código existente sin explicar por qué.
- Explicar archivo por archivo qué se cambió.
- No hacer `commit` ni `git push` sin permiso explícito.
- No instalar librerías sin permiso.

## Git

Claude puede ayudar a revisar `git status`, `git diff` y sugerir mensajes de commit, pero **no debe hacer commit ni push sin permiso explícito**.

## Errores y debugging

Cuando se encuentra un error:
1. Explicar cuál es el error y por qué ocurre.
2. Mostrar la corrección mínima.
3. No cambiar partes no relacionadas.
4. Si hay varias soluciones, elegir la más simple para Programación 1.

## Pruebas

- Indicar cómo probar manualmente cada cambio.
- Sugerir casos simples de prueba.
- No crear estructuras complejas de testing salvo pedido del usuario.

## Validaciones

Usar funciones simples y claras como las que ya existen:
`validar_entero`, `validar_patente`, `validar_fecha`, `validar_dni`, `validar_telefono`.
Cada validación debe ser fácil de leer y entender.

---

## Arquitectura del proyecto

Aplicación CLI pura. Todo el estado vive en memoria y se pierde al cerrar.

Punto de entrada: `main.py` → `interfaz/index.py:interfaz_inicio()`

### Las cuatro estructuras de datos centrales

Creadas en `interfaz_inicio()` y pasadas por referencia entre funciones:

- **`matriz`** (`list[list[str]]`): grilla del estacionamiento. Cada celda: `"LIBRE"`, una patente, o `"RESERVADA"`.
- **`registros`** (`dict[str, dict]`): vehículos actualmente estacionados, indexados por patente. Claves: `patente`, `plaza` (tupla), `hora_ingreso` (datetime), `tipo`, `estado`.
- **`reservas`** (`list[dict]`): reservas creadas por el administrador. Claves: `codigo`, `patente`, `nombre`, `dni`, `numero_telefono`, `fila`, `columna`, `fecha_ingreso`, `fecha_salida`, `tipo_vehiculo`, `estado` (`"ACTIVA"` | `"CANCELADA"`).
- **`reservas_clientes`** (`list[dict]`): solicitudes de clientes. Igual que `reservas` pero sin `codigo`, `fila` ni `columna` hasta que el admin asigne una plaza.

### Responsabilidades por módulo

| Módulo | Responsabilidad |
|---|---|
| `interfaz/index.py` | Todos los menús y flujo de navegación |
| `gestion/index.py` | Crear estacionamiento, registrar ingreso/egreso, calcular tarifa |
| `gestion/reservas.py` | Crear, cancelar, modificar, listar y asignar reservas |
| `consultas/validacion/index.py` | Validadores de patente, DNI, teléfono, fecha y enteros |
| `consultas/visualizacion/index.py` | Muestra la grilla y cuenta plazas ocupadas/disponibles |
| `consultas/constantes/index.py` | Prefijos telefónicos argentinos y días por mes |
| `ui/index.py` | `limpiar_pantalla()` y `encabezado_principal()` |

### Flujo de roles

- **Admin**: acceso completo (crear estacionamiento, registrar vehículos, gestionar reservas).
- **Cliente**: solo puede solicitar reservas (van a `reservas_clientes`, sin plaza asignada).

El admin puede luego ver las solicitudes de clientes y asignarles una plaza con `asignar_plaza()`.

### Tarifas

`$1000` la primera hora + `$500` por cada hora adicional o fracción. Implementado en `gestion/index.py:calcular_tarifa()`.

### Reglas de validación

- **Patente**: `ABC123` (viejo) o `AB123CD` (Mercosur)
- **DNI**: 7–8 dígitos, se permiten puntos (`45.873.620`)
- **Teléfono**: prefijo argentino válido (lista en `constantes`) + 6–8 dígitos, sin `0` ni `15`
- **Fecha**: `AAAA-MM-DD`, con validación real de calendario y años bisiestos

---

## Errores conocidos

| Gravedad | Dónde | Problema |
|---|---|---|
| Crítico | `interfaz/index.py:186` | `cancelar_reserva` se llama con 2 args pero acepta solo 1 → `TypeError` |
| Crítico | `reservas.py:161` | `cancelar_reserva` usa `reserva[0]` y `reserva[6]` en un dict → `TypeError` |
| Crítico | `reservas.py:38-44` | Loop de validación de teléfono nunca re-lee el input → loop infinito |
| Crítico | `reservas.py:379` | `filtrar_rango_fechas` usa `r[4]` en un dict → `KeyError` |
| Alto | `reservas.py:448-499` | `asignar_plaza` busca en `reservas` (admin) pero las del cliente están en `reservas_clientes`; además bloquea por estado `"ACTIVA"` que es el estado inicial del cliente |
| Alto | `reservas.py:199` | `modificar_reserva` limita input a 1–5; opciones 6–9 son inalcanzables |
| Medio | `reservas.py:422-430` | `buscar_por_rango_fechas` pide las fechas dos veces; los primeros valores se descartan |
| Medio | `reservas.py:187` | El `while True` en `modificar_reserva` siempre retorna en el primer ciclo; no permite múltiples modificaciones seguidas |
