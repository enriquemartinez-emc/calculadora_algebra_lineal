import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from factories.operation_factory import OperationFactory
import base64
from io import BytesIO
from sympy import latex, symbols, sympify
from threading import Timer

class SecantMethodUI:
    def __init__(self):
        self.frame = None
        self.result_frame = None
        self.equation_label_var = None
        self.update_timer = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame, text="Método de la Secante")
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        # Function input
        self.func_label = tk.Label(self.control_frame, text="Función f(x):")
        self.func_label.pack(side="top")

        self.func_entry = tk.Entry(self.control_frame)
        self.func_entry.pack(side="top")
        self.func_entry.bind("<KeyRelease>", self.update_equation_label)

        self.equation_label_var = tk.StringVar()
        self.equation_label = tk.Label(self.control_frame, textvariable=self.equation_label_var, font=("Helvetica", 12), fg="blue")
        self.equation_label.pack(side="top", pady=5)

        # Initial values input
        self.initial_value1_label = tk.Label(self.control_frame, text="Valor Inicial 1:")
        self.initial_value1_label.pack(side="top")

        self.initial_value1_entry = tk.Entry(self.control_frame)
        self.initial_value1_entry.pack(side="top")

        self.initial_value2_label = tk.Label(self.control_frame, text="Valor Inicial 2:")
        self.initial_value2_label.pack(side="top")

        self.initial_value2_entry = tk.Entry(self.control_frame)
        self.initial_value2_entry.pack(side="top")

        # Iterations input
        self.iterations_label = tk.Label(self.control_frame, text="Número de Iteraciones:")
        self.iterations_label.pack(side="top")

        self.iterations_entry = tk.Entry(self.control_frame)
        self.iterations_entry.pack(side="top")

        # Allowed error input
        self.error_label = tk.Label(self.control_frame, text="Error Permitido:")
        self.error_label.pack(side="top")

        self.error_entry = tk.Entry(self.control_frame)
        self.error_entry.pack(side="top")

        self.calculate_button = tk.Button(self.control_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(side="top", pady=10)

    def update_equation_label(self, event):
        if self.update_timer:
            self.update_timer.cancel()

        self.update_timer = Timer(0.5, self.display_equation)
        self.update_timer.start()

    def display_equation(self):
        equation_text = self.func_entry.get()
        try:
            # Allow parsing of the function input
            x = symbols('x')
            equation = sympify(equation_text, locals={'x': x})
            latex_equation = latex(equation)
            self.equation_label_var.set(f"$$ {latex_equation} $$")
        except Exception as e:
            self.equation_label_var.set("Entrada no válida")

    def calculate(self):
        func_str = self.func_entry.get()
        initial_value1 = float(self.initial_value1_entry.get())
        initial_value2 = float(self.initial_value2_entry.get())
        iterations = int(self.iterations_entry.get())
        allowed_error = float(self.error_entry.get())

        operation = OperationFactory.get_operation("Secant Method")
        if operation:
            result = operation.execute(func_str, initial_value1, initial_value2, iterations, allowed_error)
            if isinstance(result, str):
                messagebox.showerror("Error", result)
            else:
                self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        result_label = tk.Label(self.result_frame, text="Resultado del Método de la Secante", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=10)

        table_frame = tk.Frame(self.result_frame)
        table_frame.pack(fill="x")

        headers = ["Iteración", "xi-1", "xi", "xi+1", "eA", "f(xi-1)", "f(xi)"]
        for header in headers:
            header_label = tk.Label(table_frame, text=header, font=("Helvetica", 10, "bold"), borderwidth=1, relief="solid")
            header_label.grid(row=0, column=headers.index(header), sticky="nsew")

        for i, (xi_minus1, xi, xi_plus1, ea, f_xi_minus1, f_xi) in enumerate(result["iterations"]):
            tk.Label(table_frame, text=i + 1, font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=0, sticky="nsew")
            tk.Label(table_frame, text=f"{xi_minus1:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=1, sticky="nsew")
            tk.Label(table_frame, text=f"{xi:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=2, sticky="nsew")
            tk.Label(table_frame, text=f"{xi_plus1:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=3, sticky="nsew")
            tk.Label(table_frame, text=f"{ea:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=4, sticky="nsew")
            tk.Label(table_frame, text=f"{f_xi_minus1:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=5, sticky="nsew")
            tk.Label(table_frame, text=f"{f_xi:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=6, sticky="nsew")

        root_label = tk.Label(self.result_frame, text=f"Raíz aproximada: {result['result']}", font=("Helvetica", 12, "bold"))
        root_label.pack(pady=10)

        # Display the plot
        plot_data = base64.b64decode(result["plot_url"])
        image = Image.open(BytesIO(plot_data))
        photo = ImageTk.PhotoImage(image)
        plot_label = tk.Label(self.result_frame, image=photo)
        plot_label.image = photo
        plot_label.pack()
