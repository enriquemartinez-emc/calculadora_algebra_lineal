import tkinter as tk
from random import randint
from factories.operation_factory import OperationFactory

class MatrixEquationUI:
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

        self.matrix_size_frame = tk.Frame(self.control_frame)
        self.matrix_size_frame.pack(anchor="center", pady=5)

        self.matrix_size_label = tk.Label(self.matrix_size_frame, text="Matrix Size:")
        self.matrix_size_label.pack(side="left")

        self.matrix_rows_label = tk.Label(self.matrix_size_frame, text="Rows:")
        self.matrix_rows_label.pack(side="left")

        self.matrix_rows_spinbox = tk.Spinbox(self.matrix_size_frame, from_=1, to=10, command=self.update_matrix_inputs)
        self.matrix_rows_spinbox.pack(side="left")

        self.matrix_columns_label = tk.Label(self.matrix_size_frame, text="Columns:")
        self.matrix_columns_label.pack(side="left", padx=(20, 0))

        self.matrix_columns_spinbox = tk.Spinbox(self.matrix_size_frame, from_=1, to=10, command=self.update_matrix_inputs)
        self.matrix_columns_spinbox.pack(side="left")

        self.matrix_frame = tk.Frame(self.control_frame)
        self.matrix_frame.pack(anchor="center", pady=10)

        self.vector_size_frame = tk.Frame(self.control_frame)
        self.vector_size_frame.pack(anchor="center", pady=5)

        self.vector_size_label = tk.Label(self.vector_size_frame, text="Vector Size:")
        self.vector_size_label.pack(side="left")

        self.vector_size_spinbox = tk.Spinbox(self.vector_size_frame, from_=1, to=10, command=self.update_vector_inputs)
        self.vector_size_spinbox.pack(side="left")

        self.vector_frame = tk.Frame(self.control_frame)
        self.vector_frame.pack(anchor="center", pady=10)

        self.calculate_button = tk.Button(self.control_frame, text="Calculate Matrix Equation", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

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
        for widget in self.vector_frame.winfo_children():
            widget.destroy()

        size = int(self.vector_size_spinbox.get())
        self.vector_entries = [None] * size

        for i in range(size):
            entry = tk.Entry(self.vector_frame, width=5)
            entry.grid(row=i, column=0, padx=5, pady=5)
            entry.insert(0, randint(1, 10))  # Random default value
            self.vector_entries[i] = entry

    def calculate(self):
        matrix_rows = int(self.matrix_rows_spinbox.get())
        matrix_cols = int(self.matrix_columns_spinbox.get())
        vector_size = int(self.vector_size_spinbox.get())

        matrix = [[0] * matrix_cols for _ in range(matrix_rows)]
        vector = [0] * vector_size

        for i in range(matrix_rows):
            for j in range(matrix_cols):
                matrix[i][j] = float(self.matrix_entries[i][j].get())

        for i in range(vector_size):
            vector[i] = float(self.vector_entries[i].get())

        operation = OperationFactory.get_operation("Matrix Equation")
        if operation:
            result = operation.execute(matrix, vector)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if isinstance(result, str):  # Display error message if result is a string
            error_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            result_label = tk.Label(self.result_frame, text="Ecuación de Matriz", font=("Helvetica", 14, "bold"))
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
