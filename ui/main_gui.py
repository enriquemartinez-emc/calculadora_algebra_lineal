import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from factories.ui_factory import OperationUIFactory

class LinearAlgebraCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.style = Style()  # Initialize the Style
        self.style.theme_use('solar')  # Set the initial theme
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        self.create_main_ui()

    def create_main_ui(self):
        self.create_top_bar()

        frame_width = 300  # Fixed width for all frames

        self.frame1 = tk.LabelFrame(self.root, text="Operation Selection", width=frame_width)
        self.frame1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame1.grid_propagate(False)

        self.frame2 = tk.LabelFrame(self.root, text="Input", width=frame_width)
        self.frame2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame2.grid_propagate(False)

        self.frame3 = tk.LabelFrame(self.root, text="Result", width=frame_width)
        self.frame3.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.frame3.grid_propagate(False)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.create_operation_selection_ui()

        # Load the default operation UI (Gaussian Elimination)
        self.load_ui_component("Gaussian Elimination")

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
        theme_checkbutton = ttk.Checkbutton(top_frame, text="Light Theme", command=self.toggle_theme)
        theme_checkbutton.pack(side="right", padx=5)

    def toggle_theme(self):
        current_theme = self.style.theme_use()
        new_theme = 'cosmo' if current_theme == 'solar' else 'solar'
        self.style.theme_use(new_theme)

    def create_operation_selection_ui(self):
        operations = [
            "Gaussian Elimination", 
            "Row Echelon", 
            "Matrix Addition", 
            "Vector Addition", 
            "Vector Multiplication", 
            "Transpose Matrix", 
            "Scalar Product",
            "Matrix Product",
            "Matrix Equation",
            "Matrix Product by Vector Sum",
            "Determinant of a Matrix",
            "Cramer's Rule",
            "Inverse of a Matrix",
            "Bisection Method",
        ]

        self.operation_combo = ttk.Combobox(self.frame1, values=operations, width=50)
        self.operation_combo.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        self.operation_combo.bind("<<ComboboxSelected>>", self.on_operation_selected)
        self.operation_combo.current(0)  # Set the default selection to Gaussian Elimination

        self.frame1.grid_columnconfigure(0, weight=1)  # Center the operation combo

    def on_operation_selected(self, event):
        selected_operation = self.operation_combo.get()
        self.load_ui_component(selected_operation)

    def load_ui_component(self, operation):
        for widget in self.frame2.winfo_children():
            widget.destroy()

        ui_factory = OperationUIFactory()
        ui_component = ui_factory.get_operation_ui(operation)
        if ui_component:
            ui_component.create_ui(self.frame2, self.frame3)
