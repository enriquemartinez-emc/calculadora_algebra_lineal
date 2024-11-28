import tkinter as tk
from factories.operation_factory import OperationFactory

class VectorMultiplicationUI:
    def __init__(self):
        self.frame = None
        self.linear_vector_entries = []
        self.columnar_vector_entries = []
        self.result_frame = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame)
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        # Vector size input
        self.size_frame = tk.Frame(self.control_frame)
        self.size_frame.pack(anchor="center", pady=10)

        self.vector_size_label = tk.Label(self.size_frame, text="Tamaño del Vector:")
        self.vector_size_label.pack(side="left")

        self.vector_size_spinbox = tk.Spinbox(self.size_frame, from_=2, to=10, command=self.update_vector_inputs)
        self.vector_size_spinbox.pack(side="left")
        self.vector_size_spinbox.delete(0, "end")
        self.vector_size_spinbox.insert(0, "3")

        self.linear_vector_frame = tk.Frame(self.control_frame)
        self.linear_vector_frame.pack(anchor="center", pady=10)

        self.linear_vector_label = tk.Label(self.linear_vector_frame, text="Vector Lineal:")
        self.linear_vector_label.grid(row=1, column=0, padx=5, pady=5)

        self.columnar_vector_frame = tk.Frame(self.control_frame)
        self.columnar_vector_frame.pack(anchor="center", pady=10)

        self.columnar_vector_label = tk.Label(self.columnar_vector_frame, text="Vector Columniar:")
        self.columnar_vector_label.grid(row=0, column=0, padx=5, pady=5)

        self.calculate_button = tk.Button(self.control_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

        self.update_vector_inputs()

    def update_vector_inputs(self):
        for widget in self.linear_vector_frame.winfo_children():
            if widget != self.linear_vector_label:
                widget.destroy()
        for widget in self.columnar_vector_frame.winfo_children():
            if widget != self.columnar_vector_label:
                widget.destroy()

        size = int(self.vector_size_spinbox.get())
        self.linear_vector_entries = [None] * size
        self.columnar_vector_entries = [None] * size

        for i in range(size):
            linear_entry = tk.Entry(self.linear_vector_frame, width=5)
            linear_entry.grid(row=1, column=i + 1, padx=5, pady=5)
            linear_entry.insert(0, 1)  # Default value
            self.linear_vector_entries[i] = linear_entry

            columnar_entry = tk.Entry(self.columnar_vector_frame, width=5)
            columnar_entry.grid(row=i + 1, column=0, padx=5, pady=5)
            columnar_entry.insert(0, 1)  # Default value
            self.columnar_vector_entries[i] = columnar_entry

    def calculate(self):
        linear_vector = [[0] * len(self.linear_vector_entries)]
        columnar_vector = [[0] for _ in range(len(self.columnar_vector_entries))]

        for i in range(len(self.linear_vector_entries)):
            linear_vector[0][i] = float(self.linear_vector_entries[i].get())
            columnar_vector[i][0] = float(self.columnar_vector_entries[i].get())

        operation = OperationFactory.get_operation("Vector Multiplication")
        if operation:
            result = operation.execute(linear_vector, columnar_vector)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if isinstance(result, str):  # Display error message if result is a string
            error_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            result_label = tk.Label(self.result_frame, text="Multiplicación de Vectores", font=("Helvetica", 12, "bold"))
            result_label.pack()

            for description, *details in result["steps"]:
                step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"))
                step_label.pack()
                if len(details) == 2:
                    vectors_label = tk.Label(self.result_frame, text=f"{details[0]} • {details[1]}", font=("Courier", 10))
                    vectors_label.pack()
                elif isinstance(details[0], list):  # Handle detailed steps of multiplication
                    for step in details[0]:
                        step_detail_label = tk.Label(self.result_frame, text=step, font=("Courier", 10))
                        step_detail_label.pack()
                else:
                    result_value_label = tk.Label(self.result_frame, text=str(details[0]), font=("Courier", 10))
                    result_value_label.pack()
