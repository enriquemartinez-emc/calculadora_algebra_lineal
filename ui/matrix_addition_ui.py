import tkinter as tk
from ttkbootstrap.dialogs import Messagebox
from random import randint
from fractions import Fraction
from factories.operation_factory import OperationFactory

class MatrixAdditionUI:
    def __init__(self):
        self.frame = None
        self.matrix_entries = []
        self.scalar_entries = []
        self.result_frame = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame)
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        # Matrix size input
        self.size_frame = tk.Frame(self.control_frame)
        self.size_frame.pack(anchor="center", pady=10)

        self.matrix_size_label = tk.Label(self.size_frame, text="Tamaño de la Matriz:")
        self.matrix_size_label.pack(side="top")

        self.rows_label = tk.Label(self.size_frame, text="Filas:")
        self.rows_label.pack(side="left")

        self.rows_spinbox = tk.Spinbox(self.size_frame, from_=2, to=10, command=self.update_matrix_inputs)
        self.rows_spinbox.pack(side="left")

        self.columns_label = tk.Label(self.size_frame, text="Columnas:")
        self.columns_label.pack(side="left", padx=(20, 0))

        self.columns_spinbox = tk.Spinbox(self.size_frame, from_=2, to=10, command=self.update_matrix_inputs)
        self.columns_spinbox.pack(side="left")

        self.matrices_frame = tk.Frame(self.control_frame)
        self.matrices_frame.pack(anchor="center", pady=10)

        self.buttons_frame = tk.Frame(self.control_frame)
        self.buttons_frame.pack(anchor="center", pady=10)

        self.add_matrix_button = tk.Button(self.buttons_frame, text="Añadir Matriz", command=self.add_matrix)
        self.add_matrix_button.pack(side="left", padx=10)

        self.calculate_button = tk.Button(self.buttons_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(side="left", padx=10)

        self.update_matrix_inputs()

    def update_matrix_inputs(self):
        for widget in self.matrices_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []
        self.scalar_entries = []

        # Add at least two matrices by default
        self.add_matrix()
        self.add_matrix()

    def add_matrix(self):
        matrix_index = len(self.matrix_entries)
        matrix_frame = tk.Frame(self.matrices_frame)
        matrix_frame.pack(anchor="center", pady=10)

        scalar_label = tk.Label(matrix_frame, text=f"Escalar para Matriz {matrix_index + 1}:")
        scalar_label.pack(side="top")

        scalar_entry = tk.Entry(matrix_frame)
        scalar_entry.pack(side="top")
        self.scalar_entries.append(scalar_entry)

        entries_frame = tk.Frame(matrix_frame)
        entries_frame.pack(side="top")

        rows = int(self.rows_spinbox.get())
        cols = int(self.columns_spinbox.get())
        matrix = [[None] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                entry = tk.Entry(entries_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                matrix[i][j] = entry

        self.matrix_entries.append(matrix)

        if len(self.matrix_entries) > 2:
            remove_button = tk.Button(matrix_frame, text="Eliminar Matriz", command=lambda: self.remove_specific_matrix(matrix_frame, matrix, scalar_entry))
            remove_button.pack(side="top", pady=5)

    def remove_specific_matrix(self, matrix_frame, matrix, scalar_entry):
        self.matrix_entries.remove(matrix)
        self.scalar_entries.remove(scalar_entry)
        matrix_frame.destroy()

    def calculate(self):
        matrices = []
        scalars = []
        rows = int(self.rows_spinbox.get())
        cols = int(self.columns_spinbox.get())

        try:
            for scalar_entry in self.scalar_entries:
                scalars.append(Fraction(scalar_entry.get()))
        except ValueError:
            Messagebox.show_error("Los escalares deben ser enteros, números con decimales o fracciones; no deben contener letras ni caracteres especiales.", "Error", parent=self.frame)
            return

        for matrix in self.matrix_entries:
            mat = [[0] * cols for _ in range(rows)]
            for i in range(rows):
                for j in range(cols):
                    mat[i][j] = float(matrix[i][j].get())
            matrices.append(mat)

        if not all(len(matrix) == len(matrices[0]) and len(matrix[0]) == len(matrices[0][0]) for matrix in matrices):
            Messagebox.show_error("Todas las matrices deben tener las mismas dimensiones.", "Error", parent=self.frame)
            return

        operation = OperationFactory.get_operation("Matrix Addition")
        if operation:
            result = operation.execute(matrices, scalars)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if isinstance(result, str):  # Display error message if result is a string
            error_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            result_label = tk.Label(self.result_frame, text="Suma de Matrices", font=("Helvetica", 12, "bold"))
            result_label.pack()

            for description, step in result["steps"]:
                step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"), wraplength=self.result_frame.winfo_width())
                step_label.pack()
                step_matrix_frame = tk.Frame(self.result_frame)
                step_matrix_frame.pack(anchor="n", fill="x")
                step_matrix = '\n'.join(['[' + ' '.join(f"{cell:>8}" for cell in row) + ']' for row in step])
                step_matrix_label = tk.Label(step_matrix_frame, text=step_matrix, font=("Courier", 10), justify="left", wraplength=self.result_frame.winfo_width())
                step_matrix_label.pack()

            detailed_label = tk.Label(self.result_frame, text="Cada entrada en la matriz resultante es la suma de las entradas correspondientes de todas las matrices de entrada, multiplicada por su respectivo escalar.", font=("Helvetica", 10), wraplength=self.result_frame.winfo_width())
            detailed_label.pack()
