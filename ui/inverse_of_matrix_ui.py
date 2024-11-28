import tkinter as tk
from random import randint
from fractions import Fraction
from factories.operation_factory import OperationFactory

class InverseOfMatrixUI:
    def __init__(self):
        self.frame = None
        self.matrix_entries = []
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

        self.matrix_size_label = tk.Label(self.matrix_size_frame, text="Tamaño de la Matriz:")
        self.matrix_size_label.pack(side="left")

        self.matrix_size_spinbox = tk.Spinbox(self.matrix_size_frame, from_=2, to=10, command=self.update_matrix_inputs)
        self.matrix_size_spinbox.pack(side="left")

        self.matrix_frame = tk.Frame(self.control_frame)
        self.matrix_frame.pack(anchor="center", pady=10)

        self.calculate_button = tk.Button(self.control_frame, text="Calcular Inversa", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

        self.update_matrix_inputs()

    def update_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        size = int(self.matrix_size_spinbox.get())
        self.matrix_entries = [[None] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                self.matrix_entries[i][j] = entry

    def calculate(self):
        size = int(self.matrix_size_spinbox.get())
        matrix = [[0] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                matrix[i][j] = Fraction(self.matrix_entries[i][j].get())

        operation = OperationFactory.get_operation("Inverse of a Matrix")
        if operation:
            result = operation.execute(matrix)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if isinstance(result, str):  # Display error message if result is a string
            error_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            result_label = tk.Label(self.result_frame, text="Inversa de la Matriz", font=("Helvetica", 14, "bold"))
            result_label.pack(pady=10)

            if isinstance(result, dict):
                for description, details in result["steps"]:
                    step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"), wraplength=self.result_frame.winfo_width())
                    step_label.pack()
                    if isinstance(details, list):
                        matrix_frame = tk.Frame(self.result_frame, relief=tk.SOLID, borderwidth=1)
                        matrix_frame.pack(pady=5)
                        max_col_widths = [max(len(str(details[i][j])) for i in range(len(details))) for j in range(len(details[0]))]

                        for row in details:
                            row_text = "  ".join(f"{str(cell).rjust(max_col_widths[j])}" for j, cell in enumerate(row))
                            row_label = tk.Label(matrix_frame, text=f"[ {row_text} ]", font=("Courier", 10))
                            row_label.pack()
                    else:
                        result_value_label = tk.Label(self.result_frame, text=str(details), font=("Courier", 10))
                        result_value_label.pack()
