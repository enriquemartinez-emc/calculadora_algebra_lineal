import tkinter as tk
from random import randint
from tkinter import messagebox
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

        self.matrix_size_frame = tk.Frame(self.control_frame)
        self.matrix_size_frame.pack(anchor="center", pady=5)

        self.matrix_size_label = tk.Label(self.matrix_size_frame, text="Matrix Size:")
        self.matrix_size_label.pack(side="left")

        self.matrix_size_spinbox = tk.Spinbox(self.matrix_size_frame, from_=2, to=10, command=self.update_matrix_inputs)
        self.matrix_size_spinbox.pack(side="left")
        self.matrix_size_spinbox.delete(0, "end")
        self.matrix_size_spinbox.insert(0, "2")

        self.matrix_frame = tk.Frame(self.control_frame)
        self.matrix_frame.pack(anchor="center", pady=10)

        self.calculate_button = tk.Button(self.control_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

        self.update_matrix_inputs()

    def update_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        size = int(self.matrix_size_spinbox.get())
        self.matrix_entries = [[None] * (size + 1) for _ in range(size)]

        for i in range(size):
            for j in range(size + 1):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.insert(0, randint(1, 10))  # Random default value
                self.matrix_entries[i][j] = entry

    def calculate(self):
        size = int(self.matrix_size_spinbox.get())
        matrix = [[0] * (size + 1) for _ in range(size)]

        for i in range(size):
            for j in range(size + 1):
                matrix[i][j] = float(self.matrix_entries[i][j].get())

        if size + 1 != len(matrix[0]):
            messagebox.showerror("Error", "La matriz ingresada debe ser cuadrada y aumentada.")
            return

        operation = OperationFactory.get_operation("Gaussian Elimination")
        if operation:
            result = operation.execute(matrix)
            if isinstance(result, str):
                messagebox.showerror("Error", result)
            else:
                self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        result_label = tk.Label(self.result_frame, text="Resultado de la Eliminación Gaussiana", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=10)

        for description, details in result["steps"]:
            step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"))
            step_label.pack()
            matrix_label = tk.Label(self.result_frame, text=details, font=("Courier", 10))
            matrix_label.pack()

        final_result_label = tk.Label(self.result_frame, text="Resultado Final:", font=("Helvetica", 14, "bold"), fg="blue")
        final_result_label.pack(pady=10)
        inverse_matrix_label = tk.Label(self.result_frame, text=result["result"], font=("Courier", 10, "bold"), fg="blue")
        inverse_matrix_label.pack()
