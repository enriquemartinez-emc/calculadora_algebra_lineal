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

        self.size_label = tk.Label(self.size_frame, text="Square Matrix Size (n x n):")
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
        self.matrix_entries = [[None] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                self.matrix_entries[i][j] = entry

        self.matrix_frame.grid_columnconfigure(list(range(size)), weight=1)

    def calculate(self):
        size = int(self.size_spinbox.get())
        matrix = [[0] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                matrix[i][j] = float(self.matrix_entries[i][j].get())

        operation = OperationFactory.get_operation("Gaussian Elimination")
        if operation:
            result = operation.execute(matrix)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        result_label = tk.Label(self.result_frame, text="Results", font=("Helvetica", 12, "bold"))
        result_label.pack()

        original_label = tk.Label(self.result_frame, text="Original Matrix", font=("Helvetica", 10))
        original_label.pack()

        original_matrix_frame = tk.Frame(self.result_frame)
        original_matrix_frame.pack(anchor="n", fill="x")

        for row in result["original"]:
            row_label = tk.Label(original_matrix_frame, text=row, font=("Helvetica", 10))
            row_label.pack()

        steps_label = tk.Label(self.result_frame, text="Steps", font=("Helvetica", 10))
        steps_label.pack()

        for description, step in result["steps"]:
            step_frame = tk.Frame(self.result_frame)
            step_frame.pack(anchor="n", fill="x")
            description_label = tk.Label(step_frame, text=description, font=("Helvetica", 10))
            description_label.pack()
            for row in step:
                row_label = tk.Label(step_frame, text=row, font=("Helvetica", 10))
                row_label.pack()

        final_result_label = tk.Label(self.result_frame, text="Final Result", font=("Helvetica", 10))
        final_result_label.pack()

        result_matrix_frame = tk.Frame(self.result_frame)
        result_matrix_frame.pack(anchor="n", fill="x")

        for row in result["result"]:
            row_label = tk.Label(result_matrix_frame, text=row, font=("Helvetica", 10))
            row_label.pack()

        variables_label = tk.Label(self.result_frame, text="Variable Solutions", font=("Helvetica", 12, "bold"))
        variables_label.pack()

        variables_frame = tk.Frame(self.result_frame)
        variables_frame.pack(anchor="n", fill="x")

        for i, value in enumerate(result["variables"]):
            var_label = tk.Label(variables_frame, text=f"x{i+1} = {value}", font=("Helvetica", 10))
            var_label.pack()
