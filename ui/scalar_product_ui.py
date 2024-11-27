import tkinter as tk
from random import randint
from factories.operation_factory import OperationFactory

class ScalarProductUI:
    def __init__(self):
        self.frame = None
        self.matrix_entries = []
        self.scalar_entry = None
        self.result_frame = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame)
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        self.input_type_var = tk.StringVar(value="matrix")

        self.matrix_size_label = tk.Label(self.control_frame, text="Matrix/Vector Size:")
        self.matrix_size_label.pack(side="top")

        self.rows_label = tk.Label(self.control_frame, text="Rows:")
        self.rows_label.pack(side="left")

        self.rows_spinbox = tk.Spinbox(self.control_frame, from_=1, to=10, command=self.update_matrix_inputs)
        self.rows_spinbox.pack(side="left")

        self.columns_label = tk.Label(self.control_frame, text="Columns:")
        self.columns_label.pack(side="left", padx=(20, 0))

        self.columns_spinbox = tk.Spinbox(self.control_frame, from_=1, to=10, command=self.update_matrix_inputs)
        self.columns_spinbox.pack(side="left")

        self.scalar_label = tk.Label(self.control_frame, text="Scalar:")
        self.scalar_label.pack(side="top", pady=(10, 0))

        self.scalar_entry = tk.Entry(self.control_frame)
        self.scalar_entry.pack(side="top")

        self.matrix_frame = tk.Frame(self.control_frame)
        self.matrix_frame.pack(anchor="center", pady=10)

        self.calculate_button = tk.Button(self.control_frame, text="Calculate Scalar Product", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

        self.update_matrix_inputs()

    def update_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        rows = int(self.rows_spinbox.get())
        cols = int(self.columns_spinbox.get())
        self.matrix_entries = [[None] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                self.matrix_entries[i][j] = entry

    def calculate(self):
        rows = int(self.rows_spinbox.get())
        cols = int(self.columns_spinbox.get())
        matrix_or_vector = [[0] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                matrix_or_vector[i][j] = float(self.matrix_entries[i][j].get())

        scalar = self.scalar_entry.get()

        operation = OperationFactory.get_operation("Scalar Product")
        if operation:
            result = operation.execute(matrix_or_vector, scalar)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if isinstance(result, str):  # Display error message if result is a string
            error_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            result_label = tk.Label(self.result_frame, text="Producto Escalar", font=("Helvetica", 14, "bold"))
            result_label.pack(pady=10)

            for description, matrix_or_value in result["steps"]:
                step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"))
                step_label.pack()
                value_label = tk.Label(self.result_frame, text=str(matrix_or_value), font=("Courier", 10))
                value_label.pack()
