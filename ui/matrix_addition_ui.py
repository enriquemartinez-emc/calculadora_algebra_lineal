import tkinter as tk
from random import randint
from factories.operation_factory import OperationFactory

class MatrixAdditionUI:
    def __init__(self):
        self.frame = None
        self.matrix_entries = []

    def create_ui(self, parent):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack()

        # Matrix size input
        self.size_label = tk.Label(self.frame, text="Matrix Size:")
        self.size_label.pack(side="left")

        self.size_spinbox = tk.Spinbox(self.frame, from_=2, to=10, command=self.update_matrix_inputs)
        self.size_spinbox.pack(side="left")

        # Placeholder for matrix input entries
        self.matrix_frame = tk.Frame(self.frame)
        self.matrix_frame.pack()

        self.calculate_button = tk.Button(self.frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack(side="left")

        self.update_matrix_inputs()

    def update_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        size = int(self.size_spinbox.get())
        self.matrix_entries = [[None] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                self.matrix_entries[i][j] = tk.Entry(self.matrix_frame, width=5)
                self.matrix_entries[i][j].grid(row=i, column=j)
                self.matrix_entries[i][j].insert(0, randint(1, 10))  # Random default value

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
        if self.frame:
            for widget in self.frame.winfo_children():
                widget.destroy()

        original_label = tk.Label(self.frame, text="Original Matrix")
        original_label.pack()

        original_matrix_frame = tk.Frame(self.frame)
        original_matrix_frame.pack()

        for row in result["original"]:
            row_label = tk.Label(original_matrix_frame, text=row)
            row_label.pack()

        steps_label = tk.Label(self.frame, text="Steps")
        steps_label.pack()

        for description, step in result["steps"]:
            step_frame = tk.Frame(self.frame)
            step_frame.pack()
            description_label = tk.Label(step_frame, text=description, font=("Helvetica", 12, "bold"))
            description_label.pack()
            for row in step:
                row_label = tk.Label(step_frame, text=row)
                row_label.pack()

        result_label = tk.Label(self.frame, text="Final Result")
        result_label.pack()

        result_matrix_frame = tk.Frame(self.frame)
        result_matrix_frame.pack()

        for row in result["result"]:
            row_label = tk.Label(result_matrix_frame, text=row)
            row_label.pack()
