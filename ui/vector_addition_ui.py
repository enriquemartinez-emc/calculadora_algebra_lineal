import tkinter as tk
from factories.operation_factory import OperationFactory

class VectorAdditionUI:
    def __init__(self):
        self.frame = None
        self.vector_entries = []
        self.scalar_entries = []
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

        self.vectors_frame = tk.Frame(self.control_frame)
        self.vectors_frame.pack(anchor="center", pady=10)

        self.buttons_frame = tk.Frame(self.control_frame)
        self.buttons_frame.pack(anchor="center", pady=10)

        self.add_vector_button = tk.Button(self.buttons_frame, text="Agregar Vector", command=self.add_vector)
        self.add_vector_button.pack(side="left", padx=10)

        self.calculate_button = tk.Button(self.buttons_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(side="left", padx=10)

        self.update_vector_inputs()

    def update_vector_inputs(self):
        for widget in self.vectors_frame.winfo_children():
            widget.destroy()

        self.vector_entries = []
        self.scalar_entries = []

        # Add at least two vectors by default
        self.add_vector()
        self.add_vector()

    def add_vector(self):
        vector_index = len(self.vector_entries)
        vector_frame = tk.Frame(self.vectors_frame)
        vector_frame.pack(anchor="center", pady=10)

        scalar_label = tk.Label(vector_frame, text=f"Escalar para el Vector {vector_index + 1}:")
        scalar_label.pack(side="top")

        scalar_entry = tk.Entry(vector_frame)
        scalar_entry.pack(side="top")
        self.scalar_entries.append(scalar_entry)

        entries_frame = tk.Frame(vector_frame)
        entries_frame.pack(side="top")

        size = int(self.vector_size_spinbox.get())
        vector = [None] * size

        for i in range(size):
            entry = tk.Entry(entries_frame, width=5)
            entry.grid(row=0, column=i, padx=5, pady=5)
            entry.insert(0, 1)  # Default value
            vector[i] = entry

        self.vector_entries.append(vector)

    def calculate(self):
        vectors = []
        scalars = []

        for scalar_entry in self.scalar_entries:
            scalars.append(scalar_entry.get())

        size = int(self.vector_size_spinbox.get())
        for vector in self.vector_entries:
            vec = [0] * size
            for i in range(size):
                vec[i] = float(vector[i].get())
            vectors.append(vec)

        operation = OperationFactory.get_operation("Vector Addition")
        if operation:
            result = operation.execute(vectors, scalars)
            self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if isinstance(result, str):  # Display error message if result is a string
            error_label = tk.Label(self.result_frame, text=result, font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            result_label = tk.Label(self.result_frame, text="Suma de Vectores", font=("Helvetica", 12, "bold"))
            result_label.pack()

            for description, vector in result["steps"]:
                step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"))
                step_label.pack()
                vector_label = tk.Label(self.result_frame, text=str(vector), font=("Courier", 10))
                vector_label.pack()
