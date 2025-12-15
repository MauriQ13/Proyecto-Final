# 📊 LP Solver - Solucionador de Programación Lineal

Aplicación de escritorio con interfaz tipo Excel para resolver problemas de Programación Lineal (LP) y Programación Entera Mixta (MIP).

## ✨ Características

- 🏷️ **Variables Personalizadas** - Renombra variables con nombres significativos
- 🔢 **Variables Enteras** - Soporte completo para MIP
- ♾️ **Alta Capacidad** - Hasta 100 variables y 100 restricciones
- 🎨 **Interfaz Excel** - Tabla intuitiva con navegación por teclado
- 📐 **Restricciones** - Soporta `<=`, `>=`, `=`
- 📚 **4 Ejemplos Incluidos** - Problemas listos para probar
- 👁️ **Visualización en Tiempo Real** - Modelo y resultados en panel lateral

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install pulp

# Ejecutar aplicación
python lp_solver_app.py
```

## 📖 Cómo Usar

### Opción 1: Usar Ejemplos (Más Rápido) ⚡
1. Abre la pestaña **"Ejemplos"**
2. Elige uno de los ejemplos disponibles:
   - 🥗 **Mezcla Dietética** (3 vars, 4 restricciones)
   - 🚛 **Mantenimiento de Carreteras** (8 vars, 6 restricciones)
3. Click en **"Cargar Ejemplo"**
4. Ve a la pestaña **"Solver"** y click en **"Resolver Problema"**

### Opción 2: Crear tu Propio Problema
1. **Configura tu problema**
   - Selecciona: Maximizar/Minimizar
   - Define: Número de variables (2-100) y restricciones (1-100)
   - Click en "Configurar"

2. **Personaliza (opcional)**
   - **Fila 0**: Renombra variables (ej: "Mesas", "Sillas")
   - **Fila 2**: Marca checkboxes para variables enteras

3. **Ingresa datos**
   - **Fila Objetivo**: Coeficientes de la función objetivo
   - **Filas de restricciones**: Coeficientes, tipo (<=, >=, =) y valor

4. **Resuelve**
   - Click en "Resolver Problema"
   - Ve el resultado en el panel derecho

3. **Resuelve**:
   - Click en "Resolver Problema"
   - El modelo se muestra formateado en panel derecho
   - Los resultados aparecen destacados en amarillo

### 🎹 Navegación con Teclado (Estilo Excel):

- **Enter / ↓**: Baja en la columna actual
- **↑**: Sube en la columna actual
- **→**: Avanza a la siguiente celda
- **←**: Retrocede a la celda anterior
- **Selección automática**: El texto se selecciona al navegar

### 🎨 Código de Colores:

- 🔵 **Azul**: Encabezados (X1, X2, ..., Tipo, Valor)
- 🟢 **Verde**: Fila de Objetivo
- 🟡 **Amarillo**: Restricciones 1-5
- 🟢 **Verde claro**: Restricciones 6-10
- 🟡 **Amarillo claro**: Columna de Valores (RHS)
- 🟡 **Amarillo pálido**: Área de Resultados

### Ejemplo Simple (2 variables):

**Maximizar:** Z = 3x₁ + 5x₂

**Sujeto a:**
- R1: x₁ + 2x₂ ≤ 20
- R2: 3x₁ + 2x₂ ≤ 40
- R3: x₁ + x₂ ≤ 15
- x₁, x₂ ≥ 0 (no negatividad automática)

## ⌨️ Atajos de Teclado

- **Flechas** (↑↓←→): Navegar entre celdas
- **Enter**: Ir a celda inferior o siguiente
- **Tab**: Avanzar al siguiente campo
- **Números**: Ingresar coeficientes directamente

## 📦 Distribución de la Aplicación

### Opción 1: Código Fuente (Recomendado)
Comparte la carpeta completa. El usuario necesita:
```bash
pip install pulp
python lp_solver_app.py
```

### Opción 2: Ejecutable (PyInstaller)
Crear un .exe independiente:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="LP_Solver" lp_solver_app.py
```
El .exe estará en la carpeta `dist/`

### Opción 3: ZIP con todo incluido
Comprime la carpeta y comparte. Incluye instrucciones en README.

## 📁 Estructura del Proyecto

```
Proyecto final/
├── lp_solver_app.py       # Punto de entrada (20 líneas)
├── requirements.txt       # Dependencias (pulp)
├── README.md             # Documentación
└── src/
    ├── models/
    │   └── lp_model.py   # Motor de optimización (~160 líneas)
    ├── ui/
    │   └── main_window.py # Interfaz gráfica (~1300 líneas)
    └── utils/
        └── validators.py  # Validación de entradas (~30 líneas)
```

## 🏗️ Arquitectura del Sistema

### Componentes Principales

#### 1. **lp_solver_app.py** (Punto de Entrada)
```python
# Inicializa la aplicación
root = tk.Tk()
app = LPSolverGUI(root)
root.mainloop()
```
**Responsabilidad:** Configurar ventana Tkinter y lanzar interfaz.

---

#### 2. **src/models/lp_model.py** (Motor de Optimización)
Encapsula toda la lógica de PuLP para resolver problemas LP/MIP.

**Métodos clave:**
- `create_problem(sense, objective_coefficients, variable_names, integer_vars)`
  - Crea el problema de optimización
  - Define variables (continuas o enteras)
  - Establece función objetivo (Max/Min)
  
- `add_constraint(coefficients, constraint_type, rhs, name)`
  - Agrega restricciones al modelo
  - Soporta `<=`, `>=`, `=`
  
- `solve()`
  - Ejecuta el solver CBC
  - Retorna: `{'status': str, 'objective_value': float, 'solution': dict}`

**Fix Importante (Línea 136):**
```python
# Antes (fallaba con nombres personalizados):
sorted(self.variables.keys(), key=lambda x: int(x[1:]))

# Después (funciona con cualquier nombre):
self.variables.keys()
```

---

#### 3. **src/ui/main_window.py** (Interfaz Gráfica)
El componente más grande, maneja toda la interacción del usuario.

**Arquitectura interna:**
```
LPSolverGUI
│
├── Notebook (pestañas)
│   ├── Tab 1: Solver
│   │   ├── Panel Izquierdo (800px)
│   │   │   ├── Configuración (vars, restricciones, sentido)
│   │   │   └── Tabla Excel (Canvas + Scrollbars)
│   │   │       ├── Fila 0: Nombres personalizados
│   │   │       ├── Fila 1: Headers (X1, X2, ...)
│   │   │       ├── Fila 2: Checkboxes enteros
│   │   │       ├── Fila 3: Objetivo (verde)
│   │   │       └── Filas 4+: Restricciones
│   │   │
│   │   └── Panel Derecho (350px)
│   │       ├── Modelo formateado
│   │       └── Resultados
│   │
│   └── Tab 2: Ejemplos
│       └── 4 ejemplos con botones "Cargar"
```

**Métodos principales:**

| Método | Propósito |
|--------|-----------|
| `_build_table()` | Genera tabla dinámica con widgets |
| `_solve_problem()` | Valida datos, crea LPModel, muestra resultados |
| `_load_example_1/2/3/4()` | Carga ejemplos predefinidos |
| `_nav_obj_right/left()` | Navegación Excel en objetivo |
| `_nav_const_down/up/right/left()` | Navegación Excel en restricciones |
| `_highlight_row()` | Resalta fila activa |
| `_update_variable_name()` | Actualiza nombre y refresca headers |

**Flujo de datos:**
```
Usuario ingresa datos
    ↓
Validación (validate_float)
    ↓
Creación de LPModel
    ↓
Solver (PuLP + CBC)
    ↓
Formateo de resultados
    ↓
Visualización en panel derecho
```

---

#### 4. **src/utils/validators.py** (Validación)
```python
def validate_float(value, field_name):
    """Valida que el valor sea numérico."""
    if not value or value.strip() == "":
        raise ValueError(f"{field_name} está vacío")
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"{field_name} debe ser numérico")
```

**Uso:** Prevenir errores antes de enviar al solver.

---

### 🔄 Flujo de Ejecución

```
1. Usuario ejecuta: python lp_solver_app.py
   ↓
2. lp_solver_app.py crea ventana Tkinter
   ↓
3. LPSolverGUI (main_window.py) construye interfaz
   │  ├── Crea Notebook con 2 tabs
   │  ├── Genera tabla Excel dinámica
   │  └── Configura navegación por teclado
   ↓
4. Usuario configura problema o carga ejemplo
   ↓
5. Click en "Resolver Problema"
   │  ├── validators.py valida todos los campos
   │  ├── lp_model.py crea problema PuLP
   │  ├── Solver CBC ejecuta optimización
   │  └── Resultados se muestran en panel derecho
   ↓
6. Usuario puede modificar y re-resolver
```

---

### 📊 División de Responsabilidades

| Componente | Responsabilidad | Dependencias |
|------------|----------------|--------------|
| **lp_solver_app.py** | Inicialización | tkinter, LPSolverGUI |
| **lp_model.py** | Lógica de optimización | PuLP |
| **main_window.py** | Interfaz y eventos | tkinter, ttk, LPModel, validators |
| **validators.py** | Validación de datos | Ninguna |

**Principio aplicado:** Separación de capas (UI / Lógica / Datos)

---

### 🔌 Extensibilidad

Para agregar nuevas características:

1. **Nuevo tipo de restricción:**
   - Modificar `lp_model.py` → método `add_constraint()`
   - Actualizar dropdown en `main_window.py`

2. **Nuevo ejemplo:**
   - Crear método `_load_example_5()` en `main_window.py`
   - Agregar botón en `_create_examples_tab()`

3. **Nueva validación:**
   - Agregar función en `validators.py`
   - Llamarla desde `_solve_problem()` en `main_window.py`

4. **Exportar resultados:**
   - Agregar método en `lp_model.py` para formatear salida
   - Crear botón "Exportar" en `main_window.py`

## 🔧 Solución de Problemas

| Problema | Solución |
|----------|----------|
| "No module named 'pulp'" | Ejecuta: `pip install pulp` |
| "Infactible" | Verifica restricciones contradictorias |
| Variables no enteras | Marca checkbox en Fila 2 |

---

**Versión:** 2.0 | **Python:** 3.7+ | **Licencia:** MIT
