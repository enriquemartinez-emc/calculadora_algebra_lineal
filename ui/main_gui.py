import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from factories.ui_factory import OperationUIFactory

class LinearAlgebraCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.style = Style()  # Initialize the Style
        self.style.theme_use('darkly')  # Set the initial theme
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        self.create_main_ui()

    def create_main_ui(self):
        self.create_top_bar()

        frame_width = 300  # Fixed width for all frames

        self.frame1 = tk.LabelFrame(self.root, text="Seleccion de Operacion", width=frame_width)
        self.frame1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame1.grid_propagate(False)

        self.frame2 = tk.LabelFrame(self.root, text="Entrada", width=frame_width)
        self.frame2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame2.grid_propagate(False)

        self.frame3 = tk.LabelFrame(self.root, text="Resultado", width=frame_width)
        self.frame3.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.frame3.grid_propagate(False)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.create_operation_selection_ui()

        # Load the default operation UI (Eliminacion Gaussiana)
        self.load_ui_component("Eliminacion Gaussiana")

    def create_top_bar(self):
        top_frame = tk.Frame(self.root, bg=self.root.cget('bg'))
        top_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

        # Adding icon and title
        icon = tk.PhotoImage(file="assets/icono-ventana.png")
        # Resize the icon to be half the previous height
        resized_icon = icon.subsample(8, 8)  # Adjust the subsample factor to make it smaller
        icon_label = tk.Label(top_frame, image=resized_icon)
        icon_label.image = resized_icon  # Keep a reference to the image to prevent garbage collection
        icon_label.pack(side="left", padx=5)

        title_label = tk.Label(top_frame, text="PySolve", font=("Helvetica", 16, "bold"))
        title_label.pack(side="left", padx=5)

        # Theme Checkbutton
        theme_checkbutton = ttk.Checkbutton(top_frame, text="Tema Claro", command=self.toggle_theme)
        theme_checkbutton.pack(side="right", padx=5)

    def toggle_theme(self):
        current_theme = self.style.theme_use()
        new_theme = 'cosmo' if current_theme == 'darkly' else 'darkly'
        self.style.theme_use(new_theme)

    def create_operation_selection_ui(self):
        self.categories = {
            "Sistemas de Ecuaciones Lineales": ["Eliminación Gaussiana", "Forma Escalonada"],
            "Operaciones con matrices": ["Transponer matriz", "Producto de matriz por suma de vectores", "Sumas de matrices", "Producto de matrices/vectores", "Calcular el determinante de una matriz", "Aplicar regla de Cramer", "Obtener la inversa de una matriz"],
            "Operaciones con Vectores": ["Sumar vectores", "Multiplicar vectores"],
            "Raíces de Funciones": ["Método de bisección", "Método de Newton", "Regla falsa", "Secante"]
        }

        # Map Spanish options to English terms for loading the correct UI component
        self.operation_mapping = {
            "Eliminación Gaussiana": "Gaussian Elimination",
            "Forma Escalonada": "Row Echelon Form",
            "Transponer matriz": "Transpose Matrix",
            "Producto de matriz por suma de vectores": "Matrix Product by Vector Sum",
            "Sumas de matrices": "Matrix Addition",
            "Producto de matrices/vectores": "Matrix Product",
            "Calcular el determinante de una matriz": "Determinant of a Matrix",
            "Aplicar regla de Cramer": "Cramer's Rule",
            "Obtener la inversa de una matriz": "Inverse of a Matrix",
            "Sumar vectores": "Vector Addition",
            "Multiplicar vectores": "Vector Multiplication",
            "Método de bisección": "Bisection Method",
            "Método de Newton": "Newton Raphson Method",
            "Regla falsa": "False Position Method",
            "Secante": "Secant Method"
        }

        # Calculate width based on the longest text
        combobox_width = 25  # Half of the previous width

        self.category_label = tk.Label(self.frame1, text="Categorias:")
        self.category_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.category_combo = ttk.Combobox(self.frame1, values=list(self.categories.keys()), width=combobox_width)
        self.category_combo.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_selected)

        self.operation_label = tk.Label(self.frame1, text="Operaciones:")
        self.operation_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.operation_combo = ttk.Combobox(self.frame1, width=combobox_width)
        self.operation_combo.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.operation_combo.bind("<<ComboboxSelected>>", self.on_operation_selected)

        self.frame1.grid_columnconfigure(0, weight=1)  # Center the operation combo

        # Set default category and fill operations
        self.category_combo.set("Sistemas de Ecuaciones Lineales")
        self.on_category_selected(None)

    def on_category_selected(self, event):
        selected_category = self.category_combo.get()
        operations = self.categories.get(selected_category, [])
        self.operation_combo["values"] = operations
        if operations:
            self.operation_combo.current(0)  # Set the default selection to the first child operation
            self.on_operation_selected(None)  # Load the first operation's UI

    def on_operation_selected(self, event):
        selected_operation = self.operation_combo.get()
        self.clear_result_section()  # Clear the result section
        self.load_ui_component(selected_operation)

    def clear_result_section(self):
        for widget in self.frame3.winfo_children():
            widget.destroy()

    def load_ui_component(self, operation):
        for widget in self.frame2.winfo_children():
            widget.destroy()

        # Use the mapping to get the English term for the selected operation
        operation_english = self.operation_mapping.get(operation, operation)
        ui_factory = OperationUIFactory()
        ui_component = ui_factory.get_operation_ui(operation_english)
        if ui_component:
            ui_component.create_ui(self.frame2, self.frame3)
