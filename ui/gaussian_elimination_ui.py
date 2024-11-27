import tkinter as tk
from tkinter import ttk
from random import randint
from factories.operation_factory import OperationFactory

class GaussianEliminationUI:
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

        # Matrix size input
        self.size_frame = tk.Frame(self.control_frame)
        self.size_frame.pack(anchor="center", pady=10)

        self.size_label = tk.Label(self.size_frame, text="Number of Variables (Rows):")
        self.size_label.pack(side="left")

        self.size_spinbox = tk.Spinbox(self.size_frame, from_=2, to=10, command=self.update_matrix_inputs)
        self.size_spinbox.pack(side="left")

        # Placeholder for matrix input entries
        self.matrix_frame = tk.Frame(self.control_frame)
        self.matrix_frame.pack(anchor="center", pady=10)

        self.calculate_button = tk.Button(self.control_frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

        self.update_matrix_inputs()

    def update_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        size = int(self.size_spinbox.get())
        self.matrix_entries = [[None] * (size + 1) for _ in range(size)]  # Augmented matrix (size + 1 columns)

        for i in range(size):
            for j in range(size + 1):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                self.matrix_entries[i][j] = entry

        self.matrix_frame.grid_columnconfigure(list(range(size + 1)), weight=1)

    def calculate(self):
        size = int(self.size_spinbox.get())
        matrix = [[0] * (size + 1) for _ in range(size)]  # Augmented matrix (size + 1 columns)

        for i in range(size):
            for j in range(size + 1):
                matrix[i][j] = float(self.matrix_entries[i][j].get())

        operation = OperationFactory.get_operation("Gaussian Elimination")
        if operation:
            result = operation.execute(matrix)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        result_label = tk.Label(self.result_frame, text="Results", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=10)

        self.create_matrix_section("Original Matrix", result["original"])
        self.create_matrix_steps_section(result["steps"])
        self.create_matrix_section("Final Result", result["result"])
        self.create_variables_section(result["variables"])

    def create_matrix_section(self, title, matrix):
        section_label = tk.Label(self.result_frame, text=title, font=("Helvetica", 12, "bold"))
        section_label.pack(pady=5)

        matrix_frame = tk.Frame(self.result_frame, relief=tk.SOLID, borderwidth=1)
        matrix_frame.pack(pady=5)

        max_col_widths = [max(len(str(matrix[i][j])) for i in range(len(matrix))) for j in range(len(matrix[0]))]

        for row in matrix:
            row_text = "  ".join(f"{str(cell).rjust(max_col_widths[j])}" for j, cell in enumerate(row))
            row_label = tk.Label(matrix_frame, text=f"[ {row_text} ]", font=("Courier", 10))
            row_label.pack()

    def create_matrix_steps_section(self, steps):
        steps_label = tk.Label(self.result_frame, text="Steps", font=("Helvetica", 12, "bold"))
        steps_label.pack(pady=5)

        for description, matrix in steps:
            step_frame = tk.Frame(self.result_frame, relief=tk.SOLID, borderwidth=1, pady=5)
            step_frame.pack(pady=5)

            description_label = tk.Label(step_frame, text=description, font=("Helvetica", 10, "italic"))
            description_label.pack(pady=2)

            matrix_frame = tk.Frame(step_frame)
            matrix_frame.pack()

            max_col_widths = [max(len(str(matrix[i][j])) for i in range(len(matrix))) for j in range(len(matrix[0]))]

            for row in matrix:
                row_text = "  ".join(f"{str(cell).rjust(max_col_widths[j])}" for j, cell in enumerate(row))
                row_label = tk.Label(matrix_frame, text=f"[ {row_text} ]", font=("Courier", 10))
                row_label.pack()

    def create_variables_section(self, variables):
        variables_label = tk.Label(self.result_frame, text="Variable Solutions", font=("Helvetica", 12, "bold"))
        variables_label.pack(pady=5)

        variables_frame = tk.Frame(self.result_frame, relief=tk.SOLID, borderwidth=1)
        variables_frame.pack(pady=5)

        for i, value in enumerate(variables):
            var_label = tk.Label(variables_frame, text=f"x{i+1} = {value}", font=("Courier", 10))
            var_label.pack()
