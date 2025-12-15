"""
Ventana principal de la aplicación con interfaz Tkinter.
Diseño tipo tabla Excel según especificación del usuario.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ..models.lp_model import LPModel
from ..utils.validators import validate_float


class LPSolverGUI:
    """
    Clase principal de la interfaz gráfica para resolver problemas de Programación Lineal.
    Diseño tipo tabla Excel para fácil entrada de datos.
    """
    
    def __init__(self, root):
        """Inicializa la ventana principal y todos sus componentes."""
        self.root = root
        self.root.title("Solucionador de Programación Lineal")
        self.root.geometry("1200x700")
        
        # Variables de configuración
        self.sense_var = tk.StringVar(value="Maximizar")
        self.num_vars = tk.IntVar(value=12)
        self.num_constraints = tk.IntVar(value=10)
        
        # Nombres de variables personalizables
        self.variable_names = []
        self.use_custom_names = tk.BooleanVar(value=False)
        
        # Variables enteras
        self.integer_vars = []  # Lista de booleanos para cada variable
        
        # Referencias a widgets
        self.objective_entries = []
        self.constraint_entries = []
        self.variable_labels = []
        self.variable_name_entries = []
        self.integer_checkboxes = []
        self.current_focus_row = None
        
        # Crear interfaz
        self._create_widgets()
        
    def _create_widgets(self):
        """Crea la interfaz completa con sistema de pestañas."""
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña 1: Solver Principal
        solver_tab = tk.Frame(self.notebook)
        self.notebook.add(solver_tab, text="  Solver  ")
        
        # Pestaña 2: Ejemplos
        examples_tab = tk.Frame(self.notebook)
        self.notebook.add(examples_tab, text="  Ejemplos  ")
        
        # Crear contenido de pestaña Solver
        self._create_solver_tab(solver_tab)
        
        # Crear contenido de pestaña Ejemplos
        self._create_examples_tab(examples_tab)
    
    def _create_solver_tab(self, parent):
        """Crea el contenido de la pestaña principal del solver."""
        # Frame principal con dos paneles
        main_paned = tk.PanedWindow(parent, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel izquierdo: Configuración y tabla de datos
        left_frame = tk.Frame(main_paned, bg="white")
        main_paned.add(left_frame, minsize=800)
        
        # Panel derecho: Resultados
        right_frame = tk.Frame(main_paned, bg="white")
        main_paned.add(right_frame, minsize=350)
        
        # Contenido del panel izquierdo
        self._create_left_panel(left_frame)
        
        # Contenido del panel derecho
        self._create_right_panel(right_frame)
    
    def _create_examples_tab(self, parent):
        """Crea la pestaña de ejemplos de prueba."""
        # Frame principal con scrollbar
        canvas = tk.Canvas(parent, bg="white")
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        title_label = tk.Label(
            scrollable_frame,
            text="📚 Ejemplos de Prueba",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        title_label.pack(pady=15)
        
        # Descripción
        desc_label = tk.Label(
            scrollable_frame,
            text="Selecciona un ejemplo y haz clic en 'Cargar' para probarlo en el solver",
            font=("Arial", 10),
            bg="white",
            fg="gray"
        )
        desc_label.pack(pady=5)
        
        # =================== EJEMPLO 1 ===================
        example1_frame = tk.LabelFrame(
            scrollable_frame,
            text="  Ejemplo 1: Mezcla Dietética  ",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#2E7D32",
            relief=tk.RIDGE,
            borderwidth=2
        )
        example1_frame.pack(fill=tk.X, padx=20, pady=10)
        
        example1_text = tk.Text(
            example1_frame,
            height=16,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#F1F8E9",
            relief=tk.FLAT
        )
        example1_text.pack(fill=tk.BOTH, padx=10, pady=10)
        
        example1_content = """📊 PROBLEMA DE LA MEZCLA DIETÉTICA

Determinar las cantidades óptimas de tres alimentos para un menú 
universitario, minimizando el costo total mientras se cumplen los
requerimientos nutricionales.

Variables:
  • x₁ = Onzas del Alimento 1 ($0.10/oz)
  • x₂ = Onzas del Alimento 2 ($0.15/oz)
  • x₃ = Onzas del Alimento 3 ($0.12/oz)

Objetivo: Minimizar Z = 0.10x₁ + 0.15x₂ + 0.12x₃

Restricciones:
  R1: 50x₁ + 30x₂ + 20x₃ ≥ 290  (Vitamina 1 mínimo 290 mg)
  R2: 20x₁ + 10x₂ + 30x₃ ≥ 200  (Vitamina 2 mínimo 200 mg)
  R3: 10x₁ + 50x₂ + 20x₃ ≥ 210  (Vitamina 3 mínimo 210 mg)
  R4: x₁ + x₂ + x₃ ≥ 9          (Tamaño mínimo 9 onzas)

Configuración: 3 variables, 4 restricciones
"""
        example1_text.insert("1.0", example1_content)
        example1_text.config(state=tk.DISABLED)
        
        btn1 = tk.Button(
            example1_frame,
            text="📥 Cargar Ejemplo 1",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            relief=tk.RAISED,
            command=self._load_example_1
        )
        btn1.pack(pady=10)
        
        # =================== EJEMPLO 2 ===================
        example2_frame = tk.LabelFrame(
            scrollable_frame,
            text="  Ejemplo 2: Mantenimiento de Carreteras  ",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#1976D2",
            relief=tk.RIDGE,
            borderwidth=2
        )
        example2_frame.pack(fill=tk.X, padx=20, pady=10)
        
        example2_text = tk.Text(
            example2_frame,
            height=20,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#E3F2FD",
            relief=tk.FLAT
        )
        example2_text.pack(fill=tk.BOTH, padx=10, pady=10)
        
        example2_content = """🚛 PROBLEMA DE MANTENIMIENTO DE CARRETERAS

Distribuir sal y arena con costo mínimo desde dos reservas hacia
cuatro zonas de la ciudad.

Variables:
  • x₁₁ = Toneladas de Reserva 1 a Zona 1 ($2.00/ton)
  • x₁₂ = Toneladas de Reserva 1 a Zona 2 ($3.00/ton)
  • x₁₃ = Toneladas de Reserva 1 a Zona 3 ($1.50/ton)
  • x₁₄ = Toneladas de Reserva 1 a Zona 4 ($2.50/ton)
  • x₂₁ = Toneladas de Reserva 2 a Zona 1 ($4.00/ton)
  • x₂₂ = Toneladas de Reserva 2 a Zona 2 ($3.50/ton)
  • x₂₃ = Toneladas de Reserva 2 a Zona 3 ($2.50/ton)
  • x₂₄ = Toneladas de Reserva 2 a Zona 4 ($3.00/ton)

Objetivo: Minimizar Z = 2.00x₁₁ + 3.00x₁₂ + 1.50x₁₃ + 2.50x₁₄ +
                         4.00x₂₁ + 3.50x₂₂ + 2.50x₂₃ + 3.00x₂₄

Restricciones de Oferta (Capacidad):
  R1: x₁₁ + x₁₂ + x₁₃ + x₁₄ ≤ 900  (Reserva 1 máximo 900 ton)
  R2: x₂₁ + x₂₂ + x₂₃ + x₂₄ ≤ 750  (Reserva 2 máximo 750 ton)

Restricciones de Demanda (Mínimos):
  R3: x₁₁ + x₂₁ ≥ 300  (Zona 1 mínimo 300 ton)
  R4: x₁₂ + x₂₂ ≥ 450  (Zona 2 mínimo 450 ton)
  R5: x₁₃ + x₂₃ ≥ 500  (Zona 3 mínimo 500 ton)
  R6: x₁₄ + x₂₄ ≥ 350  (Zona 4 mínimo 350 ton)

Configuración: 8 variables, 6 restricciones
"""
        example2_text.insert("1.0", example2_content)
        example2_text.config(state=tk.DISABLED)
        
        btn2 = tk.Button(
            example2_frame,
            text="📥 Cargar Ejemplo 2",
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            cursor="hand2",
            relief=tk.RAISED,
            command=self._load_example_2
        )
        btn2.pack(pady=10)
        
        # =================== EJEMPLO 3 ===================
        example3_frame = tk.LabelFrame(
            scrollable_frame,
            text="  Ejemplo 3: Entrega de Premios (Asignación de Capital)  ",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#F57C00",
            relief=tk.RIDGE,
            borderwidth=2
        )
        example3_frame.pack(fill=tk.X, padx=20, pady=10)
        
        example3_text = tk.Text(
            example3_frame,
            height=20,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#FFF3E0",
            relief=tk.FLAT
        )
        example3_text.pack(fill=tk.BOTH, padx=10, pady=10)
        
        example3_content = """💰 PROBLEMA DE ENTREGA DE PREMIOS (Asignación de Capital)

Determinar fondos para 6 proyectos de energía, maximizando el
beneficio neto total con presupuesto de $1000 millones.

Variables (fondos en millones):
  • x₁ = Proyecto 1 Solar (Beneficio: 4.4/dólar)
  • x₂ = Proyecto 2 Solar (Beneficio: 3.8/dólar)
  • x₃ = Proyecto 3 Combustibles Sintéticos (Beneficio: 4.1/dólar)
  • x₄ = Proyecto 4 Carbón (Beneficio: 3.5/dólar)
  • x₅ = Proyecto 5 Nuclear (Beneficio: 5.1/dólar)
  • x₆ = Proyecto 6 Geotérmica (Beneficio: 3.2/dólar)

Objetivo: Maximizar Z = 4.4x₁ + 3.8x₂ + 4.1x₃ + 3.5x₄ + 5.1x₅ + 3.2x₆

Restricciones:
  R1: x₁ + x₂ + x₃ + x₄ + x₅ + x₆ ≤ 1000  (Presupuesto total)
  R2: x₁ ≤ 200  (Máximo Proyecto 1)
  R3: x₂ ≤ 180  (Máximo Proyecto 2)
  R4: x₃ ≤ 250  (Máximo Proyecto 3)
  R5: x₄ ≤ 150  (Máximo Proyecto 4)
  R6: x₅ ≤ 400  (Máximo Proyecto 5)
  R7: x₆ ≤ 120  (Máximo Proyecto 6)
  R8: x₅ ≥ 200  (Mínimo 50% para Nuclear)
  R9: x₁ + x₂ ≥ 300  (Mínimo proyectos solares)

Configuración: 6 variables, 9 restricciones
"""
        example3_text.insert("1.0", example3_content)
        example3_text.config(state=tk.DISABLED)
        
        btn3 = tk.Button(
            example3_frame,
            text="📥 Cargar Ejemplo 3",
            font=("Arial", 10, "bold"),
            bg="#FF9800",
            fg="white",
            cursor="hand2",
            relief=tk.RAISED,
            command=self._load_example_3
        )
        btn3.pack(pady=10)
        
        # =================== EJEMPLO 4 ===================
        example4_frame = tk.LabelFrame(
            scrollable_frame,
            text="  Ejemplo 4: Mezcla de Petróleo (Refinería)  ",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#7B1FA2",
            relief=tk.RIDGE,
            borderwidth=2
        )
        example4_frame.pack(fill=tk.X, padx=20, pady=10)
        
        example4_text = tk.Text(
            example4_frame,
            height=24,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg="#F3E5F5",
            relief=tk.FLAT
        )
        example4_text.pack(fill=tk.BOTH, padx=10, pady=10)
        
        example4_content = """⛽ PROBLEMA DE MEZCLA DE PETRÓLEO (Refinería)

Determinar litros de 4 componentes para producir 3 mezclas de gasolina,
maximizando utilidad total.

Variables (litros):
  • x₁₁, x₁₂, x₁₃ = Componente 1 en Mezcla 1, 2, 3
  • x₂₁, x₂₂, x₂₃ = Componente 2 en Mezcla 1, 2, 3
  • x₃₁, x₃₂, x₃₃ = Componente 3 en Mezcla 1, 2, 3
  • x₄₁, x₄₂, x₄₃ = Componente 4 en Mezcla 1, 2, 3

Objetivo: Maximizar Z = 
  0.11x₁₁ + 0.08x₂₁ + 0.14x₃₁ + 0.12x₄₁ +
  0.07x₁₂ + 0.04x₂₂ + 0.10x₃₂ + 0.08x₄₂ +
  0.05x₁₃ + 0.02x₂₃ + 0.08x₃₃ + 0.06x₄₃

Restricciones de Calidad:
  R1: -0.40x₁₁ + 0.60x₂₁ - 0.40x₃₁ - 0.40x₄₁ ≤ 0  (C2 en M1 ≤ 40%)
  R2: -0.25x₁₂ - 0.25x₂₂ + 0.75x₃₂ - 0.25x₄₂ ≥ 0  (C3 en M2 ≥ 25%)
  R3: 0.70x₁₃ - 0.30x₂₃ - 0.30x₃₃ - 0.30x₄₃ = 0   (C1 en M3 = 30%)
  R4: -0.60x₁₁ + 0.40x₂₁ - 0.60x₃₁ + 0.40x₄₁ ≥ 0  (C2+C4 en M1 ≥ 60%)

Restricciones de Disponibilidad:
  R5: x₂₁ + x₂₂ + x₂₃ ≤ 1500000  (Componente 2 máx)
  R6: x₃₁ + x₃₂ + x₃₃ ≤ 1000000  (Componente 3 máx)

Restricciones de Producción:
  R7: Σ todas las x = 5000000  (Producción total exacta)
  R8: x₁₁ + x₂₁ + x₃₁ + x₄₁ ≥ 2000000  (Mezcla 1 mínima)

Configuración: 12 variables, 8 restricciones
"""
        example4_text.insert("1.0", example4_content)
        example4_text.config(state=tk.DISABLED)
        
        btn4 = tk.Button(
            example4_frame,
            text="📥 Cargar Ejemplo 4",
            font=("Arial", 10, "bold"),
            bg="#9C27B0",
            fg="white",
            cursor="hand2",
            relief=tk.RAISED,
            command=self._load_example_4
        )
        btn4.pack(pady=10)
        
        # Nota final
        note_label = tk.Label(
            scrollable_frame,
            text="💡 Tip: Después de cargar, ve a la pestaña 'Solver' y haz clic en 'Resolver Problema'",
            font=("Arial", 9, "italic"),
            bg="white",
            fg="#666"
        )
        note_label.pack(pady=15)
        
    def _create_left_panel(self, parent):
        """Crea el panel izquierdo con la configuración y tabla de datos."""
        # Título
        title_label = tk.Label(
            parent,
            text="DATOS",
            font=("Arial", 14, "bold"),
            bg="white"
        )
        title_label.pack(pady=10)
        
        # Frame de configuración
        config_frame = tk.Frame(parent, bg="white")
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Configuración en línea
        tk.Label(config_frame, text="Tipo:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            config_frame,
            text="Maximizar",
            variable=self.sense_var,
            value="Maximizar"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            config_frame,
            text="Minimizar",
            variable=self.sense_var,
            value="Minimizar"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(config_frame, text="  Variables:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=(20, 5))
        
        vars_spinbox = tk.Spinbox(
            config_frame,
            from_=2,
            to=100,
            textvariable=self.num_vars,
            width=5,
            font=("Arial", 10)
        )
        vars_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Label(config_frame, text="Restricciones:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=(10, 5))
        
        const_spinbox = tk.Spinbox(
            config_frame,
            from_=1,
            to=100,
            textvariable=self.num_constraints,
            width=5,
            font=("Arial", 10)
        )
        const_spinbox.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            config_frame,
            text="Aplicar",
            font=("Arial", 9),
            bg="#2196F3",
            fg="white",
            command=self._rebuild_table,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=10)
        
        # Frame para la tabla con scroll
        table_container = tk.Frame(parent, bg="white")
        table_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbars
        self.canvas = tk.Canvas(table_container, bg="white", highlightthickness=0)
        v_scrollbar = tk.Scrollbar(table_container, orient="vertical", command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(table_container, orient="horizontal", command=self.canvas.xview)
        
        self.table_frame = tk.Frame(self.canvas, bg="white")
        
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars y canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Actualizar región de scroll
        self.table_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Construir tabla inicial
        self._build_table()
        
        # Botón de resolver
        tk.Button(
            parent,
            text="Resolver Problema",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=30,
            pady=10,
            command=self._solve_problem,
            cursor="hand2"
        ).pack(pady=10)
        
    def _create_right_panel(self, parent):
        """Crea el panel derecho con el modelo y resultados."""
        # Título MODELO
        tk.Label(
            parent,
            text="MODELO",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(pady=10)
        
        # Frame para el modelo
        model_frame = tk.LabelFrame(
            parent,
            text="Función Objetivo y Restricciones",
            font=("Arial", 10, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        model_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.model_text = scrolledtext.ScrolledText(
            model_frame,
            height=15,
            font=("Courier New", 9),
            wrap="word",
            bg="#f5f5f5"
        )
        self.model_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame para resultados
        results_frame = tk.LabelFrame(
            parent,
            text="RESULTADOS",
            font=("Arial", 10, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=10,
            font=("Courier New", 10, "bold"),
            wrap="word",
            bg="#ffffcc"
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
    def _build_table(self):
        """Construye la tabla tipo Excel."""
        # Limpiar tabla existente
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.objective_entries.clear()
        self.constraint_entries.clear()
        self.variable_labels.clear()
        self.variable_name_entries.clear()
        self.integer_checkboxes.clear()
        
        num_vars = self.num_vars.get()
        num_constraints = self.num_constraints.get()
        
        # Inicializar listas
        if len(self.variable_names) != num_vars:
            self.variable_names = [f"X{i+1}" for i in range(num_vars)]
        if len(self.integer_vars) != num_vars:
            self.integer_vars = [tk.BooleanVar(value=False) for _ in range(num_vars)]
        
        # Estilo de celdas
        header_bg = "#4472C4"
        header_fg = "white"
        cell_width = 8
        
        # Fila -1: Nombres de variables editables
        tk.Label(
            self.table_frame,
            text="Nombres:",
            width=15,
            bg="#E7E6E6",
            font=("Arial", 8, "bold"),
            relief=tk.RAISED,
            borderwidth=1
        ).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        for i in range(num_vars):
            name_entry = tk.Entry(
                self.table_frame,
                width=cell_width,
                font=("Arial", 8),
                justify="center",
                relief=tk.SOLID,
                borderwidth=1,
                bg="#F0F0F0"
            )
            name_entry.grid(row=0, column=i+1, sticky="nsew", padx=1, pady=1)
            name_entry.insert(0, self.variable_names[i])
            name_entry.bind('<FocusOut>', lambda e, idx=i: self._update_variable_name(idx, e.widget.get()))
            name_entry.bind('<Return>', lambda e, idx=i: self._update_variable_name(idx, e.widget.get()))
            self.variable_name_entries.append(name_entry)
        
        # Columnas vacías para tipo y valor en fila de nombres
        tk.Label(self.table_frame, text="", bg="white").grid(row=0, column=num_vars+1, sticky="nsew")
        tk.Label(self.table_frame, text="", bg="white").grid(row=0, column=num_vars+2, sticky="nsew")
        
        # Fila 0: Encabezados con nombres de variables
        tk.Label(self.table_frame, text="", width=15, bg="white").grid(row=1, column=0, sticky="nsew")
        
        for i in range(num_vars):
            var_label = tk.Label(
                self.table_frame,
                text=self.variable_names[i],
                width=cell_width,
                bg=header_bg,
                fg=header_fg,
                font=("Arial", 9, "bold"),
                relief=tk.RAISED,
                borderwidth=1
            )
            var_label.grid(row=1, column=i+1, sticky="nsew", padx=1, pady=1)
            self.variable_labels.append(var_label)
        
        # Columnas de restricción
        tk.Label(
            self.table_frame,
            text="Tipo",
            width=cell_width,
            bg=header_bg,
            fg=header_fg,
            font=("Arial", 9, "bold"),
            relief=tk.RAISED,
            borderwidth=1
        ).grid(row=1, column=num_vars+1, sticky="nsew", padx=1, pady=1)
        
        tk.Label(
            self.table_frame,
            text="Valor",
            width=cell_width+2,
            bg=header_bg,
            fg=header_fg,
            font=("Arial", 9, "bold"),
            relief=tk.RAISED,
            borderwidth=1
        ).grid(row=1, column=num_vars+2, sticky="nsew", padx=1, pady=1)
        
        # Fila 1.5: Checkboxes para variables enteras
        tk.Label(
            self.table_frame,
            text="Entera:",
            width=15,
            bg="#E7E6E6",
            font=("Arial", 8, "bold"),
            relief=tk.RAISED,
            borderwidth=1
        ).grid(row=2, column=0, sticky="nsew", padx=1, pady=1)
        
        for i in range(num_vars):
            check_frame = tk.Frame(self.table_frame, bg="#F0F0F0")
            check_frame.grid(row=2, column=i+1, sticky="nsew", padx=1, pady=1)
            
            chk = tk.Checkbutton(
                check_frame,
                variable=self.integer_vars[i],
                bg="#F0F0F0",
                activebackground="#F0F0F0"
            )
            chk.pack()
            self.integer_checkboxes.append(chk)
        
        # Columnas vacías para tipo y valor en fila de enteros
        tk.Label(self.table_frame, text="", bg="white").grid(row=2, column=num_vars+1, sticky="nsew")
        tk.Label(self.table_frame, text="", bg="white").grid(row=2, column=num_vars+2, sticky="nsew")
        
        # Fila 3: Objetivo
        obj_label = tk.Label(
            self.table_frame,
            text="Objetivo",
            width=15,
            bg="#70AD47",
            fg="white",
            font=("Arial", 9, "bold"),
            relief=tk.RAISED,
            borderwidth=1
        )
        obj_label.grid(row=3, column=0, sticky="nsew", padx=1, pady=1)
        
        for i in range(num_vars):
            entry = tk.Entry(
                self.table_frame,
                width=cell_width,
                font=("Arial", 10),
                justify="center",
                relief=tk.SOLID,
                borderwidth=1
            )
            entry.grid(row=3, column=i+1, sticky="nsew", padx=1, pady=1)
            entry.insert(0, "0")
            
            # Resaltar fila al hacer foco
            entry.bind('<FocusIn>', lambda e, row=3: self._highlight_row(row))
            entry.bind('<FocusOut>', lambda e: self._unhighlight_row())
            
            # Navegación con teclado
            entry.bind('<Return>', lambda e, idx=i: self._navigate_objective(e, idx))
            entry.bind('<Down>', lambda e: self._focus_constraint(0, 0))
            entry.bind('<Right>', lambda e, idx=i: self._nav_obj_right(e, idx))
            entry.bind('<Left>', lambda e, idx=i: self._nav_obj_left(e, idx))
            
            self.objective_entries.append(entry)
        
        # Celdas vacías en objetivo para tipo y valor
        tk.Label(self.table_frame, text="", bg="white").grid(row=3, column=num_vars+1, sticky="nsew")
        tk.Label(self.table_frame, text="", bg="white").grid(row=3, column=num_vars+2, sticky="nsew")
        
        # Filas 4+: Restricciones
        for r in range(num_constraints):
            # Etiqueta de restricción
            tk.Label(
                self.table_frame,
                text=f"Restricción {r+1}",
                width=15,
                bg="#FFC000" if r < 5 else "#92D050",
                fg="black",
                font=("Arial", 9, "bold"),
                relief=tk.RAISED,
                borderwidth=1
            ).grid(row=r+4, column=0, sticky="nsew", padx=1, pady=1)
            
            # Coeficientes
            coef_entries = []
            for c in range(num_vars):
                entry = tk.Entry(
                    self.table_frame,
                    width=cell_width,
                    font=("Arial", 10),
                    justify="center",
                    relief=tk.SOLID,
                    borderwidth=1
                )
                entry.grid(row=r+4, column=c+1, sticky="nsew", padx=1, pady=1)
                entry.insert(0, "0")
                
                # Resaltar fila al hacer foco
                entry.bind('<FocusIn>', lambda e, row=r+4: self._highlight_row(row))
                entry.bind('<FocusOut>', lambda e: self._unhighlight_row())
                
                # Navegación
                entry.bind('<Return>', lambda e, row=r, col=c: self._nav_const_down(e, row, col))
                entry.bind('<Down>', lambda e, row=r, col=c: self._nav_const_down(e, row, col))
                entry.bind('<Up>', lambda e, row=r, col=c: self._nav_const_up(e, row, col))
                entry.bind('<Right>', lambda e, row=r, col=c: self._nav_const_right(e, row, col))
                entry.bind('<Left>', lambda e, row=r, col=c: self._nav_const_left(e, row, col))
                
                coef_entries.append(entry)
            
            # Tipo de restricción (cambiado a <=, >=, =)
            type_combo = ttk.Combobox(
                self.table_frame,
                values=["<=", ">=", "="],
                state="readonly",
                width=cell_width-2,
                font=("Arial", 10),
                justify="center"
            )
            type_combo.grid(row=r+4, column=num_vars+1, sticky="nsew", padx=1, pady=1)
            type_combo.current(0)
            type_combo.bind('<Return>', lambda e, row=r: self._nav_to_value(e, row))
            
            # Valor RHS
            value_entry = tk.Entry(
                self.table_frame,
                width=cell_width+2,
                font=("Arial", 10),
                justify="center",
                relief=tk.SOLID,
                borderwidth=1,
                bg="#FFFF99"
            )
            value_entry.grid(row=r+4, column=num_vars+2, sticky="nsew", padx=1, pady=1)
            value_entry.insert(0, "0")
            
            # Resaltar fila al hacer foco
            value_entry.bind('<FocusIn>', lambda e, row=r+4: self._highlight_row(row))
            value_entry.bind('<FocusOut>', lambda e: self._unhighlight_row())
            
            value_entry.bind('<Return>', lambda e, row=r: self._nav_from_value(e, row))
            value_entry.bind('<Up>', lambda e, row=r: self._nav_value_up(e, row))
            value_entry.bind('<Down>', lambda e, row=r: self._nav_value_down(e, row))
            
            self.constraint_entries.append({
                'coefficients': coef_entries,
                'type': type_combo,
                'value': value_entry
            })
    
    def _rebuild_table(self):
        """Reconstruye la tabla cuando cambia la configuración."""
        self._build_table()
        self._update_model_display()
    
    # Métodos de navegación
    def _navigate_objective(self, event, idx):
        num_vars = len(self.objective_entries)
        if idx < num_vars - 1:
            self.objective_entries[idx + 1].focus()
            self.objective_entries[idx + 1].select_range(0, tk.END)
        return 'break'
    
    def _nav_obj_right(self, event, idx):
        num_vars = len(self.objective_entries)
        if idx < num_vars - 1:
            self.objective_entries[idx + 1].focus()
            self.objective_entries[idx + 1].select_range(0, tk.END)
        return 'break'
    
    def _nav_obj_left(self, event, idx):
        if idx > 0:
            self.objective_entries[idx - 1].focus()
            self.objective_entries[idx - 1].select_range(0, tk.END)
        return 'break'
    
    def _focus_constraint(self, row, col):
        if self.constraint_entries and self.constraint_entries[row]['coefficients']:
            self.constraint_entries[row]['coefficients'][col].focus()
            self.constraint_entries[row]['coefficients'][col].select_range(0, tk.END)
        return 'break'
    
    def _nav_const_down(self, event, row, col):
        if row < len(self.constraint_entries) - 1:
            self.constraint_entries[row + 1]['coefficients'][col].focus()
            self.constraint_entries[row + 1]['coefficients'][col].select_range(0, tk.END)
        return 'break'
    
    def _nav_const_up(self, event, row, col):
        if row > 0:
            self.constraint_entries[row - 1]['coefficients'][col].focus()
            self.constraint_entries[row - 1]['coefficients'][col].select_range(0, tk.END)
        else:
            if col < len(self.objective_entries):
                self.objective_entries[col].focus()
                self.objective_entries[col].select_range(0, tk.END)
        return 'break'
    
    def _nav_const_right(self, event, row, col):
        num_vars = len(self.constraint_entries[0]['coefficients'])
        if col < num_vars - 1:
            self.constraint_entries[row]['coefficients'][col + 1].focus()
            self.constraint_entries[row]['coefficients'][col + 1].select_range(0, tk.END)
        else:
            self.constraint_entries[row]['type'].focus()
        return 'break'
    
    def _nav_const_left(self, event, row, col):
        if col > 0:
            self.constraint_entries[row]['coefficients'][col - 1].focus()
            self.constraint_entries[row]['coefficients'][col - 1].select_range(0, tk.END)
        return 'break'
    
    def _nav_to_value(self, event, row):
        self.constraint_entries[row]['value'].focus()
        self.constraint_entries[row]['value'].select_range(0, tk.END)
        return 'break'
    
    def _nav_from_value(self, event, row):
        if row < len(self.constraint_entries) - 1:
            self.constraint_entries[row + 1]['coefficients'][0].focus()
            self.constraint_entries[row + 1]['coefficients'][0].select_range(0, tk.END)
        return 'break'
    
    def _nav_value_up(self, event, row):
        if row > 0:
            self.constraint_entries[row - 1]['value'].focus()
            self.constraint_entries[row - 1]['value'].select_range(0, tk.END)
        return 'break'
    
    def _nav_value_down(self, event, row):
        if row < len(self.constraint_entries) - 1:
            self.constraint_entries[row + 1]['value'].focus()
            self.constraint_entries[row + 1]['value'].select_range(0, tk.END)
        return 'break'
    
    def _update_model_display(self):
        """Actualiza la visualización del modelo."""
        self.model_text.delete(1.0, tk.END)
        
        sense = self.sense_var.get()
        self.model_text.insert(tk.END, f"{sense}:\n", "bold")
        self.model_text.insert(tk.END, "Z = ")
        
        # Mostrar función objetivo con nombres personalizados
        num_vars = len(self.objective_entries)
        for i in range(num_vars):
            coef = self.objective_entries[i].get()
            if i > 0:
                self.model_text.insert(tk.END, " + ")
            var_name = self.variable_names[i] if i < len(self.variable_names) else f"X{i+1}"
            self.model_text.insert(tk.END, f"{coef}·{var_name}")
        
        self.model_text.insert(tk.END, "\n\nSujeto a:\n")
        
        # Mostrar restricciones
        for i, constraint in enumerate(self.constraint_entries):
            self.model_text.insert(tk.END, f"R{i+1}: ")
            for j, entry in enumerate(constraint['coefficients']):
                coef = entry.get()
                if j > 0:
                    self.model_text.insert(tk.END, " + ")
                var_name = self.variable_names[j] if j < len(self.variable_names) else f"X{j+1}"
                self.model_text.insert(tk.END, f"{coef}·{var_name}")
            
            tipo = constraint['type'].get()
            valor = constraint['value'].get()
            tipo_map = {"<": "≤", "<=": "≤", ">": "≥", ">=": "≥", "=": "="}
            self.model_text.insert(tk.END, f" {tipo_map.get(tipo, tipo)} {valor}\n")
        
        # Mostrar restricciones de no negatividad y enteras
        self.model_text.insert(tk.END, "\nRestricciones adicionales:\n")
        for i, var_name in enumerate(self.variable_names):
            if i < len(self.integer_vars) and self.integer_vars[i].get():
                self.model_text.insert(tk.END, f"  {var_name} ≥ 0 y entera\n")
            else:
                self.model_text.insert(tk.END, f"  {var_name} ≥ 0\n")
    
    def _solve_problem(self):
        """Resuelve el problema de PL."""
        try:
            # Actualizar visualización del modelo
            self._update_model_display()
            
            # Validar y obtener función objetivo
            objective_coefficients = []
            for i, entry in enumerate(self.objective_entries):
                var_name = self.variable_names[i] if i < len(self.variable_names) else f"X{i+1}"
                coef = validate_float(entry.get(), f"Coeficiente {var_name} de función objetivo")
                objective_coefficients.append(coef)
            
            # Validar y obtener restricciones
            constraints_data = []
            for i, constraint in enumerate(self.constraint_entries):
                coefficients = []
                for j, entry in enumerate(constraint['coefficients']):
                    var_name = self.variable_names[j] if j < len(self.variable_names) else f"X{j+1}"
                    coef = validate_float(entry.get(), f"Coeficiente {var_name} de R{i+1}")
                    coefficients.append(coef)
                
                rhs = validate_float(constraint['value'].get(), f"Valor de R{i+1}")
                constraint_type = constraint['type'].get()
                
                # Los símbolos ya están correctos (<=, >=, =)
                if constraint_type not in ["<=", ">=", "="]:
                    constraint_type = "<="  # Default fallback
                
                constraints_data.append({
                    'coefficients': coefficients,
                    'type': constraint_type,
                    'rhs': rhs,
                    'name': f"R{i+1}"
                })
            
            # Crear y resolver el problema
            lp_model = LPModel()
            
            # Obtener flags de variables enteras
            integer_flags = [var.get() for var in self.integer_vars[:len(objective_coefficients)]]
            
            lp_model.create_problem(
                self.sense_var.get(), 
                objective_coefficients,
                variable_names=self.variable_names[:len(objective_coefficients)],
                integer_vars=integer_flags
            )
            
            # Añadir restricciones
            for constraint in constraints_data:
                lp_model.add_constraint(
                    constraint['coefficients'],
                    constraint['type'],
                    constraint['rhs'],
                    constraint['name']
                )
            
            # Resolver
            result = lp_model.solve()
            
            # Mostrar resultado
            self._display_result(result['message'])
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{str(e)}")
    
    def _display_result(self, message):
        """Muestra el resultado en el área de resultados."""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, message)
    
    def _update_variable_name(self, idx, value):
        """Actualiza el nombre de una variable y refresca los encabezados."""
        value = value.strip()
        if value and value != self.variable_names[idx]:
            self.variable_names[idx] = value
            # Actualizar el label del encabezado
            if idx < len(self.variable_name_entries):
                # Encontrar y actualizar el label de la fila 1
                for widget in self.table_frame.grid_slaves(row=1, column=idx+1):
                    if isinstance(widget, tk.Label):
                        widget.config(text=value)
    
    def _highlight_row(self, row):
        """Resalta la fila actualmente seleccionada."""
        self.current_focus_row = row
        # Aplicar color de fondo sutil a todos los widgets de la fila
        for widget in self.table_frame.grid_slaves(row=row):
            if isinstance(widget, tk.Entry):
                if widget.cget('bg') == '#FFFF99':  # Mantener color amarillo de valores
                    widget.config(bg='#FFEB9C')
                else:
                    widget.config(bg='#E8F5E9')
    
    def _unhighlight_row(self):
        """Quita el resaltado de la fila anterior."""
        if self.current_focus_row is not None:
            row = self.current_focus_row
            for widget in self.table_frame.grid_slaves(row=row):
                if isinstance(widget, tk.Entry):
                    if widget.cget('bg') in ['#FFEB9C', '#E8F5E9']:
                        # Restaurar color original
                        if row >= 4:  # Restricciones - verificar si es columna de valor
                            grid_info = widget.grid_info()
                            if grid_info and grid_info.get('column') == len(self.objective_entries) + 2:
                                widget.config(bg='#FFFF99')
                            else:
                                widget.config(bg='white')
                        else:
                            widget.config(bg='white')
            self.current_focus_row = None
    
    def _load_example_1(self):
        """Carga el Ejemplo 1: Mezcla Dietética."""
        # Configurar parámetros
        self.sense_var.set("Minimizar")
        self.num_vars.set(3)
        self.num_constraints.set(4)
        
        # Reconstruir tabla
        self._rebuild_table()
        
        # Esperar a que la tabla se construya
        self.root.update_idletasks()
        
        # Nombres de variables
        nombres = ["Alim_1", "Alim_2", "Alim_3"]
        for i, nombre in enumerate(nombres):
            if i < len(self.variable_name_entries):
                self.variable_name_entries[i].delete(0, tk.END)
                self.variable_name_entries[i].insert(0, nombre)
                self._update_variable_name(i, nombre)
        
        # Función objetivo: 0.10, 0.15, 0.12
        obj_coefs = ["0.10", "0.15", "0.12"]
        for i, coef in enumerate(obj_coefs):
            if i < len(self.objective_entries):
                self.objective_entries[i].delete(0, tk.END)
                self.objective_entries[i].insert(0, coef)
        
        # Restricciones
        # R1: 50, 30, 20 >= 290 (Vitamina 1)
        # R2: 20, 10, 30 >= 200 (Vitamina 2)
        # R3: 10, 50, 20 >= 210 (Vitamina 3)
        # R4: 1, 1, 1 >= 9 (Tamaño)
        constraints_data = [
            (["50", "30", "20"], ">=", "290"),
            (["20", "10", "30"], ">=", "200"),
            (["10", "50", "20"], ">=", "210"),
            (["1", "1", "1"], ">=", "9")
        ]
        
        for r, (coefs, tipo, valor) in enumerate(constraints_data):
            if r < len(self.constraint_entries):
                # Coeficientes
                for c, coef in enumerate(coefs):
                    if c < len(self.constraint_entries[r]['coefficients']):
                        self.constraint_entries[r]['coefficients'][c].delete(0, tk.END)
                        self.constraint_entries[r]['coefficients'][c].insert(0, coef)
                
                # Tipo
                self.constraint_entries[r]['type'].set(tipo)
                
                # Valor
                self.constraint_entries[r]['value'].delete(0, tk.END)
                self.constraint_entries[r]['value'].insert(0, valor)
        
        # Cambiar a pestaña Solver
        self.notebook.select(0)
        
        # Actualizar visualización del modelo
        self._update_model_display()
        
        messagebox.showinfo(
            "Ejemplo Cargado",
            "✅ Ejemplo 1: Mezcla Dietética cargado exitosamente.\n\n"
            "Haz clic en 'Resolver Problema' para ver la solución."
        )
    
    def _load_example_2(self):
        """Carga el Ejemplo 2: Mantenimiento de Carreteras."""
        # Configurar parámetros
        self.sense_var.set("Minimizar")
        self.num_vars.set(8)
        self.num_constraints.set(6)
        
        # Reconstruir tabla
        self._rebuild_table()
        
        # Esperar a que la tabla se construya
        self.root.update_idletasks()
        
        # Nombres de variables
        nombres = ["X11", "X12", "X13", "X14", "X21", "X22", "X23", "X24"]
        for i, nombre in enumerate(nombres):
            if i < len(self.variable_name_entries):
                self.variable_name_entries[i].delete(0, tk.END)
                self.variable_name_entries[i].insert(0, nombre)
                self._update_variable_name(i, nombre)
        
        # Función objetivo: 2.00, 3.00, 1.50, 2.50, 4.00, 3.50, 2.50, 3.00
        obj_coefs = ["2.00", "3.00", "1.50", "2.50", "4.00", "3.50", "2.50", "3.00"]
        for i, coef in enumerate(obj_coefs):
            if i < len(self.objective_entries):
                self.objective_entries[i].delete(0, tk.END)
                self.objective_entries[i].insert(0, coef)
        
        # Restricciones
        # R1: 1,1,1,1,0,0,0,0 <= 900 (Reserva 1)
        # R2: 0,0,0,0,1,1,1,1 <= 750 (Reserva 2)
        # R3: 1,0,0,0,1,0,0,0 >= 300 (Zona 1)
        # R4: 0,1,0,0,0,1,0,0 >= 450 (Zona 2)
        # R5: 0,0,1,0,0,0,1,0 >= 500 (Zona 3)
        # R6: 0,0,0,1,0,0,0,1 >= 350 (Zona 4)
        constraints_data = [
            (["1", "1", "1", "1", "0", "0", "0", "0"], "<=", "900"),
            (["0", "0", "0", "0", "1", "1", "1", "1"], "<=", "750"),
            (["1", "0", "0", "0", "1", "0", "0", "0"], ">=", "300"),
            (["0", "1", "0", "0", "0", "1", "0", "0"], ">=", "450"),
            (["0", "0", "1", "0", "0", "0", "1", "0"], ">=", "500"),
            (["0", "0", "0", "1", "0", "0", "0", "1"], ">=", "350")
        ]
        
        for r, (coefs, tipo, valor) in enumerate(constraints_data):
            if r < len(self.constraint_entries):
                # Coeficientes
                for c, coef in enumerate(coefs):
                    if c < len(self.constraint_entries[r]['coefficients']):
                        self.constraint_entries[r]['coefficients'][c].delete(0, tk.END)
                        self.constraint_entries[r]['coefficients'][c].insert(0, coef)
                
                # Tipo
                self.constraint_entries[r]['type'].set(tipo)
                
                # Valor
                self.constraint_entries[r]['value'].delete(0, tk.END)
                self.constraint_entries[r]['value'].insert(0, valor)
        
        # Cambiar a pestaña Solver
        self.notebook.select(0)
        
        # Actualizar visualización del modelo
        self._update_model_display()
        
        messagebox.showinfo(
            "Ejemplo Cargado",
            "✅ Ejemplo 2: Mantenimiento de Carreteras cargado exitosamente.\n\n"
            "Haz clic en 'Resolver Problema' para ver la solución."
        )
    
    def _load_example_3(self):
        """Carga el Ejemplo 3: Entrega de Premios (Asignación de Capital)."""
        # Configurar parámetros
        self.sense_var.set("Maximizar")
        self.num_vars.set(6)
        self.num_constraints.set(9)
        
        # Reconstruir tabla
        self._rebuild_table()
        
        # Esperar a que la tabla se construya
        self.root.update_idletasks()
        
        # Nombres de variables
        nombres = ["Solar1", "Solar2", "Sintet", "Carbon", "Nuclear", "Geoter"]
        for i, nombre in enumerate(nombres):
            if i < len(self.variable_name_entries):
                self.variable_name_entries[i].delete(0, tk.END)
                self.variable_name_entries[i].insert(0, nombre)
                self._update_variable_name(i, nombre)
        
        # Función objetivo: 4.4, 3.8, 4.1, 3.5, 5.1, 3.2
        obj_coefs = ["4.4", "3.8", "4.1", "3.5", "5.1", "3.2"]
        for i, coef in enumerate(obj_coefs):
            if i < len(self.objective_entries):
                self.objective_entries[i].delete(0, tk.END)
                self.objective_entries[i].insert(0, coef)
        
        # Restricciones
        # R1: 1,1,1,1,1,1 <= 1000 (Presupuesto total)
        # R2: 1,0,0,0,0,0 <= 200 (Máx Solar1)
        # R3: 0,1,0,0,0,0 <= 180 (Máx Solar2)
        # R4: 0,0,1,0,0,0 <= 250 (Máx Sintéticos)
        # R5: 0,0,0,1,0,0 <= 150 (Máx Carbón)
        # R6: 0,0,0,0,1,0 <= 400 (Máx Nuclear)
        # R7: 0,0,0,0,0,1 <= 120 (Máx Geotérmica)
        # R8: 0,0,0,0,1,0 >= 200 (Mín Nuclear 50%)
        # R9: 1,1,0,0,0,0 >= 300 (Mín Solares)
        constraints_data = [
            (["1", "1", "1", "1", "1", "1"], "<=", "1000"),
            (["1", "0", "0", "0", "0", "0"], "<=", "200"),
            (["0", "1", "0", "0", "0", "0"], "<=", "180"),
            (["0", "0", "1", "0", "0", "0"], "<=", "250"),
            (["0", "0", "0", "1", "0", "0"], "<=", "150"),
            (["0", "0", "0", "0", "1", "0"], "<=", "400"),
            (["0", "0", "0", "0", "0", "1"], "<=", "120"),
            (["0", "0", "0", "0", "1", "0"], ">=", "200"),
            (["1", "1", "0", "0", "0", "0"], ">=", "300")
        ]
        
        for r, (coefs, tipo, valor) in enumerate(constraints_data):
            if r < len(self.constraint_entries):
                # Coeficientes
                for c, coef in enumerate(coefs):
                    if c < len(self.constraint_entries[r]['coefficients']):
                        self.constraint_entries[r]['coefficients'][c].delete(0, tk.END)
                        self.constraint_entries[r]['coefficients'][c].insert(0, coef)
                
                # Tipo
                self.constraint_entries[r]['type'].set(tipo)
                
                # Valor
                self.constraint_entries[r]['value'].delete(0, tk.END)
                self.constraint_entries[r]['value'].insert(0, valor)
        
        # Cambiar a pestaña Solver
        self.notebook.select(0)
        
        # Actualizar visualización del modelo
        self._update_model_display()
        
        messagebox.showinfo(
            "Ejemplo Cargado",
            "✅ Ejemplo 3: Entrega de Premios cargado exitosamente.\n\n"
            "Haz clic en 'Resolver Problema' para ver la solución."
        )
    
    def _load_example_4(self):
        """Carga el Ejemplo 4: Mezcla de Petróleo (Refinería)."""
        # Configurar parámetros
        self.sense_var.set("Maximizar")
        self.num_vars.set(12)
        self.num_constraints.set(8)
        
        # Reconstruir tabla
        self._rebuild_table()
        
        # Esperar a que la tabla se construya
        self.root.update_idletasks()
        
        # Nombres de variables
        nombres = ["X11", "X12", "X13", "X21", "X22", "X23", "X31", "X32", "X33", "X41", "X42", "X43"]
        for i, nombre in enumerate(nombres):
            if i < len(self.variable_name_entries):
                self.variable_name_entries[i].delete(0, tk.END)
                self.variable_name_entries[i].insert(0, nombre)
                self._update_variable_name(i, nombre)
        
        # Función objetivo: 0.11, 0.07, 0.05, 0.08, 0.04, 0.02, 0.14, 0.10, 0.08, 0.12, 0.08, 0.06
        obj_coefs = ["0.11", "0.07", "0.05", "0.08", "0.04", "0.02", "0.14", "0.10", "0.08", "0.12", "0.08", "0.06"]
        for i, coef in enumerate(obj_coefs):
            if i < len(self.objective_entries):
                self.objective_entries[i].delete(0, tk.END)
                self.objective_entries[i].insert(0, coef)
        
        # Restricciones (orden según imagen)
        # R1: 1,1,1,1,1,1,1,1,1,1,1,1 = 5000000 (Producción total)
        # R2: -0.40,0,0,0.60,0,0,-0.40,0,0,-0.40,0,0 >= 0 (C2 en M1 <= 40%)
        # R3: 0,-0.25,0,0,-0.25,0,0,0.75,0,0,-0.25,0 >= 0 (C3 en M2 >= 25%)
        # R4: 0,0,0.70,0,0,-0.30,0,0,-0.30,0,0,-0.30 = 0 (C1 en M3 = 30%)
        # R5: -0.60,0,0,0.40,0,0,-0.60,0,0,0.40,0,0 >= 0 (C2+C4 en M1 >= 60%)
        # R6: 0,0,0,1,1,1,0,0,0,0,0,0 <= 1500000 (Comp2 disponible)
        # R7: 0,0,0,0,0,0,1,1,1,0,0,0 <= 1000000 (Comp3 disponible)
        # R8: 1,0,0,1,0,0,1,0,0,1,0,0 >= 2000000 (Mezcla 1 mínima)
        constraints_data = [
            (["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"], "=", "5000000"),
            (["-0.40", "0", "0", "0.60", "0", "0", "-0.40", "0", "0", "-0.40", "0", "0"], ">=", "0"),
            (["0", "-0.25", "0", "0", "-0.25", "0", "0", "0.75", "0", "0", "-0.25", "0"], ">=", "0"),
            (["0", "0", "0.70", "0", "0", "-0.30", "0", "0", "-0.30", "0", "0", "-0.30"], "=", "0"),
            (["-0.60", "0", "0", "0.40", "0", "0", "-0.60", "0", "0", "0.40", "0", "0"], ">=", "0"),
            (["0", "0", "0", "1", "1", "1", "0", "0", "0", "0", "0", "0"], "<=", "1500000"),
            (["0", "0", "0", "0", "0", "0", "1", "1", "1", "0", "0", "0"], "<=", "1000000"),
            (["1", "0", "0", "1", "0", "0", "1", "0", "0", "1", "0", "0"], ">=", "2000000")
        ]
        
        for r, (coefs, tipo, valor) in enumerate(constraints_data):
            if r < len(self.constraint_entries):
                # Coeficientes
                for c, coef in enumerate(coefs):
                    if c < len(self.constraint_entries[r]['coefficients']):
                        self.constraint_entries[r]['coefficients'][c].delete(0, tk.END)
                        self.constraint_entries[r]['coefficients'][c].insert(0, coef)
                
                # Tipo
                self.constraint_entries[r]['type'].set(tipo)
                
                # Valor
                self.constraint_entries[r]['value'].delete(0, tk.END)
                self.constraint_entries[r]['value'].insert(0, valor)
        
        # Cambiar a pestaña Solver
        self.notebook.select(0)
        
        # Actualizar visualización del modelo
        self._update_model_display()
        
        messagebox.showinfo(
            "Ejemplo Cargado",
            "✅ Ejemplo 4: Mezcla de Petróleo cargado exitosamente.\n\n"
            "Haz clic en 'Resolver Problema' para ver la solución."
        )
