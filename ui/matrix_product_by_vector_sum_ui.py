import tkinter as tk
from random import randint
from factories.operation_factory import OperationFactory

class MatrixProductByVectorSumUI:
    def __init__(self):
        self.frame = None
        self.matrix_entries = []
        self.vector_entries = []
        self.result_frame = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame)
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        self.matrix_size_label = tk.Label(self.control_frame, text="Tamaño de la Matriz:")
        self.matrix_size_label.pack(anchor="center", pady=10)

        self.matrix_size_frame = tk.Frame(self.control_frame)
        self.matrix_size_frame.pack(anchor="center", pady=5)

        self.matrix_rows_label = tk.Label(self.matrix_size_frame, text="Filas:")
        self.matrix_rows_label.pack(side="left")

        self.matrix_rows_spinbox = tk.Spinbox(self.matrix_size_frame, from_=1, to=10, command=self.update_matrix_inputs)
        self.matrix_rows_spinbox.pack(side="left")
        self.matrix_rows_spinbox.delete(0, "end")
        self.matrix_rows_spinbox.insert(0, 2)

        self.matrix_columns_label = tk.Label(self.matrix_size_frame, text="Columnas:")
        self.matrix_columns_label.pack(side="left", padx=(20, 0))

        self.matrix_columns_spinbox = tk.Spinbox(self.matrix_size_frame, from_=1, to=10, command=self.update_matrix_inputs)
        self.matrix_columns_spinbox.pack(side="left")
        self.matrix_columns_spinbox.delete(0, "end")
        self.matrix_columns_spinbox.insert(0, 2)

        self.matrix_frame = tk.Frame(self.control_frame)
        self.matrix_frame.pack(anchor="center", pady=10)

        self.vector_size_frame = tk.Frame(self.control_frame)
        self.vector_size_frame.pack(anchor="center", pady=5)

        self.vector_size_label = tk.Label(self.vector_size_frame, text="Tamaño del Vector:")
        self.vector_size_label.pack(side="left")

        self.vector_size_spinbox = tk.Spinbox(self.vector_size_frame, from_=1, to=10, command=self.update_vector_inputs)
        self.vector_size_spinbox.pack(side="left")
        self.vector_size_spinbox.delete(0, "end")
        self.vector_size_spinbox.insert(0, 2)

        self.vectors_frame = tk.Frame(self.control_frame)
        self.vectors_frame.pack(anchor="center", pady=10)

        self.buttons_frame = tk.Frame(self.control_frame)
        self.buttons_frame.pack(anchor="center", pady=10)

        self.add_vector_button = tk.Button(self.buttons_frame, text="Añadir Vector", command=self.add_vector)
        self.add_vector_button.pack(side="left", padx=10)

        self.calculate_button = tk.Button(self.buttons_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(side="left", padx=10)

        self.update_matrix_inputs()
        self.update_vector_inputs()

    def update_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        rows = int(self.matrix_rows_spinbox.get())
        cols = int(self.matrix_columns_spinbox.get())
        self.matrix_entries = [[None] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                self.matrix_entries[i][j] = entry

    def update_vector_inputs(self):
        for widget in self.vectors_frame.winfo_children():
            widget.destroy()

        self.vector_entries = []

        # Add at least one vector by default
        self.add_vector()

    def add_vector(self):
        vector_index = len(self.vector_entries)
        vector_frame = tk.Frame(self.vectors_frame)
        vector_frame.pack(anchor="center", pady=5)

        size = int(self.vector_size_spinbox.get())
        vector = [None] * size

        vector_label = tk.Label(vector_frame, text=f"Vector {vector_index + 1}:")
        vector_label.grid(row=0, column=0, padx=5, pady=5)

        for i in range(size):
            entry = tk.Entry(vector_frame, width=5)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, randint(1, 10))  # Random default value
            vector[i] = entry

        if len(self.vector_entries) > 0:
            remove_button = tk.Button(vector_frame, text="Eliminar Vector", command=lambda: self.remove_vector(vector_frame, vector))
            remove_button.grid(row=0, column=2, padx=5, pady=5)

        self.vector_entries.append(vector)

    def remove_vector(self, vector_frame, vector):
        self.vector_entries.remove(vector)
        vector_frame.destroy()

    def calculate(self):
        matrix_rows = int(self.matrix_rows_spinbox.get())
        matrix_cols = int(self.matrix_columns_spinbox.get())

        matrix = [[0] * matrix_cols for _ in range(matrix_rows)]
        vectors = []

        for i in range(matrix_rows):
            for j in range(matrix_cols):
                matrix[i][j] = float(self.matrix_entries[i][j].get())

        for vector in self.vector_entries:
            vec = [float(entry.get()) for entry in vector]
            vectors.append(vec)

        operation = OperationFactory.get_operation("Matrix Product by Vector Sum")
        if operation:
            result = operation.execute(matrix, vectors)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if isinstance(result, str):  # Display error message if result is a string
            error_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            result_label = tk.Label(self.result_frame, text="Producto de Matriz por Suma de Vectores", font=("Helvetica", 14, "bold"))
            result_label.pack(pady=10)

            for description, details in result["steps"]:
                step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"))
                step_label.pack()
                if isinstance(details, list):
                    for detail in details:
                        detail_label = tk.Label(self.result_frame, text=detail, font=("Courier", 10))
                        detail_label.pack()
                else:
                    result_value_label = tk.Label(self.result_frame, text=str(details), font=("Courier", 10))
                    result_value_label.pack()
