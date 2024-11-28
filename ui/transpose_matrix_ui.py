import tkinter as tk
from random import randint
from factories.operation_factory import OperationFactory

class TransposeMatrixUI:
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

        self.matrix_frame = tk.Frame(self.control_frame)
        self.matrix_frame.pack(anchor="center", pady=10)

        self.calculate_button = tk.Button(self.control_frame, text="Transponer", command=self.calculate)
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
        matrix = [[0] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = float(self.matrix_entries[i][j].get())

        operation = OperationFactory.get_operation("Transpose Matrix")
        if operation:
            result = operation.execute(matrix)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        result_label = tk.Label(self.result_frame, text="Matriz Transpuesta", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=10)

        self.create_matrix_section("Matriz Original", result["steps"][0][1])
        self.create_matrix_section("Matriz Transpuesta", result["steps"][1][1])

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
