import tkinter as tk
from random import randint
from factories.operation_factory import OperationFactory

class MatrixProductUI:
    def __init__(self):
        self.frame = None
        self.matrix1_entries = []
        self.matrix2_entries = []
        self.result_frame = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame)
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        self.matrix1_size_label = tk.Label(self.control_frame, text="Tamaño de la Matriz 1:")
        self.matrix1_size_label.pack(anchor="center", pady=10)

        self.matrix1_size_frame = tk.Frame(self.control_frame)
        self.matrix1_size_frame.pack(anchor="center", pady=5)

        self.matrix1_rows_label = tk.Label(self.matrix1_size_frame, text="Filas:")
        self.matrix1_rows_label.pack(side="left")

        self.matrix1_rows_spinbox = tk.Spinbox(self.matrix1_size_frame, from_=1, to=10, command=self.update_matrix1_inputs)
        self.matrix1_rows_spinbox.pack(side="left")
        self.matrix1_rows_spinbox.delete(0, "end")
        self.matrix1_rows_spinbox.insert(0, 2)

        self.matrix1_columns_label = tk.Label(self.matrix1_size_frame, text="Columnas:")
        self.matrix1_columns_label.pack(side="left", padx=(20, 0))

        self.matrix1_columns_spinbox = tk.Spinbox(self.matrix1_size_frame, from_=1, to=10, command=self.update_matrix1_inputs)
        self.matrix1_columns_spinbox.pack(side="left")
        self.matrix1_columns_spinbox.delete(0, "end")
        self.matrix1_columns_spinbox.insert(0, 2)

        self.matrix1_frame = tk.Frame(self.control_frame)
        self.matrix1_frame.pack(anchor="center", pady=10)

        self.matrix2_size_label = tk.Label(self.control_frame, text="Tamaño de la Matriz 2:")
        self.matrix2_size_label.pack(anchor="center", pady=10)

        self.matrix2_size_frame = tk.Frame(self.control_frame)
        self.matrix2_size_frame.pack(anchor="center", pady=5)

        self.matrix2_rows_label = tk.Label(self.matrix2_size_frame, text="Filas:")
        self.matrix2_rows_label.pack(side="left")

        self.matrix2_rows_spinbox = tk.Spinbox(self.matrix2_size_frame, from_=1, to=10, command=self.update_matrix2_inputs)
        self.matrix2_rows_spinbox.pack(side="left")
        self.matrix2_rows_spinbox.delete(0, "end")
        self.matrix2_rows_spinbox.insert(0, 2)

        self.matrix2_columns_label = tk.Label(self.matrix2_size_frame, text="Columnas:")
        self.matrix2_columns_label.pack(side="left", padx=(20, 0))

        self.matrix2_columns_spinbox = tk.Spinbox(self.matrix2_size_frame, from_=1, to=10, command=self.update_matrix2_inputs)
        self.matrix2_columns_spinbox.pack(side="left")
        self.matrix2_columns_spinbox.delete(0, "end")
        self.matrix2_columns_spinbox.insert(0, 2)

        self.matrix2_frame = tk.Frame(self.control_frame)
        self.matrix2_frame.pack(anchor="center", pady=10)

        self.calculate_button = tk.Button(self.control_frame, text="Calcular Producto de Matrices", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

        self.update_matrix1_inputs()
        self.update_matrix2_inputs()

    def update_matrix1_inputs(self):
        for widget in self.matrix1_frame.winfo_children():
            widget.destroy()

        rows = int(self.matrix1_rows_spinbox.get())
        cols = int(self.matrix1_columns_spinbox.get())
        self.matrix1_entries = [[None] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                entry = tk.Entry(self.matrix1_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                self.matrix1_entries[i][j] = entry

    def update_matrix2_inputs(self):
        for widget in self.matrix2_frame.winfo_children():
            widget.destroy()

        rows = int(self.matrix2_rows_spinbox.get())
        cols = int(self.matrix2_columns_spinbox.get())
        self.matrix2_entries = [[None] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                entry = tk.Entry(self.matrix2_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                self.matrix2_entries[i][j] = entry

    def calculate(self):
        matrix1_rows = int(self.matrix1_rows_spinbox.get())
        matrix1_cols = int(self.matrix1_columns_spinbox.get())
        matrix2_rows = int(self.matrix2_rows_spinbox.get())
        matrix2_cols = int(self.matrix2_columns_spinbox.get())

        matrix1 = [[0] * matrix1_cols for _ in range(matrix1_rows)]
        matrix2 = [[0] * matrix2_cols for _ in range(matrix2_rows)]

        for i in range(matrix1_rows):
            for j in range(matrix1_cols):
                matrix1[i][j] = float(self.matrix1_entries[i][j].get())

        for i in range(matrix2_rows):
            for j in range(matrix2_cols):
                matrix2[i][j] = float(self.matrix2_entries[i][j].get())

        operation = OperationFactory.get_operation("Matrix Product")
        if operation:
            result = operation.execute(matrix1, matrix2)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if isinstance(result, str):  # Display error message if result is a string
            error_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            result_label = tk.Label(self.result_frame, text="Producto de Matrices", font=("Helvetica", 14, "bold"))
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
