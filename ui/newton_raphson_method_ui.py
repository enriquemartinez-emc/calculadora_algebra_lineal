import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from factories.operation_factory import OperationFactory
import base64
from io import BytesIO
from sympy import latex, sympify
from sympy.parsing.latex import parse_latex
from threading import Timer

class NewtonRaphsonMethodUI:
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

        self.control_frame = tk.LabelFrame(self.frame, text="Método de Newton-Raphson")
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        self.func_label = tk.Label(self.control_frame, text="Función f(x):")
        self.func_label.pack(anchor="center")
        self.func_entry = tk.Entry(self.control_frame, width=20)
        self.func_entry.pack(anchor="center")
        self.func_entry.bind("<KeyRelease>", self.update_equation_label)

        self.equation_label_var = tk.StringVar()
        self.equation_label = tk.Label(self.control_frame, textvariable=self.equation_label_var, font=("Helvetica", 12), fg="blue")
        self.equation_label.pack(anchor="center", pady=5)

        self.initial_value_label = tk.Label(self.control_frame, text="Valor Inicial:")
        self.initial_value_label.pack(anchor="center")
        self.initial_value_entry = tk.Entry(self.control_frame, width=20)
        self.initial_value_entry.pack(anchor="center")

        self.iterations_label = tk.Label(self.control_frame, text="Número de Iteraciones:")
        self.iterations_label.pack(anchor="center")
        self.iterations_entry = tk.Entry(self.control_frame, width=20)
        self.iterations_entry.pack(anchor="center")

        self.error_label = tk.Label(self.control_frame, text="Error Permitido:")
        self.error_label.pack(anchor="center")
        self.error_entry = tk.Entry(self.control_frame, width=20)
        self.error_entry.pack(anchor="center")

        self.calculate_button = tk.Button(self.control_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

    def update_equation_label(self, event):
        if self.update_timer:
            self.update_timer.cancel()

        self.update_timer = Timer(0.5, self.display_equation)
        self.update_timer.start()

    def display_equation(self):
        equation_text = self.func_entry.get()
        try:
            equation = parse_latex(equation_text)
            normal_equation = latex(equation)
            self.equation_label_var.set(normal_equation)
        except Exception as e:
            self.equation_label_var.set("Entrada no válida")

    def calculate(self):
        func_str = self.func_entry.get()
        initial_value = float(self.initial_value_entry.get())
        iterations = int(self.iterations_entry.get())
        allowed_error = float(self.error_entry.get())

        operation = OperationFactory.get_operation("Newton Raphson Method")
        if operation:
            result = operation.execute(func_str, initial_value, iterations, allowed_error)
            if isinstance(result, str):
                messagebox.showerror("Error", result)
            else:
                self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        result_label = tk.Label(self.result_frame, text="Resultado del Método de Newton-Raphson", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=10)

        for description in result["steps"]:
            step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"))
            step_label.pack()

        final_result_label = tk.Label(self.result_frame, text=f"Raíz: {result['result']}", font=("Courier", 12, "bold"))
        final_result_label.pack(pady=10)

        # Display the plot
        plot_data = base64.b64decode(result["plot_url"])
        image = Image.open(BytesIO(plot_data))
        photo = ImageTk.PhotoImage(image)
        plot_label = tk.Label(self.result_frame, image=photo)
        plot_label.image = photo
        plot_label.pack()
