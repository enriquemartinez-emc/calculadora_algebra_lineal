import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from factories.operation_factory import OperationFactory
import base64
from io import BytesIO
from sympy import latex, symbols, sympify
from threading import Timer

class FalsePositionMethodUI:
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

        self.control_frame = tk.LabelFrame(self.frame, text="Método de Falsa Posición")
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

        # Lower limit input
        self.lower_limit_label = tk.Label(self.control_frame, text="Límite Inferior:")
        self.lower_limit_label.pack(side="top")

        self.lower_limit_entry = tk.Entry(self.control_frame)
        self.lower_limit_entry.pack(side="top")

        # Upper limit input
        self.upper_limit_label = tk.Label(self.control_frame, text="Límite Superior:")
        self.upper_limit_label.pack(side="top")

        self.upper_limit_entry = tk.Entry(self.control_frame)
        self.upper_limit_entry.pack(side="top")

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
        lower_limit = float(self.lower_limit_entry.get())
        upper_limit = float(self.upper_limit_entry.get())
        allowed_error = float(self.error_entry.get())

        operation = OperationFactory.get_operation("False Position Method")
        if operation:
            result = operation.execute(func_str, lower_limit, upper_limit, allowed_error)
            if isinstance(result, str):
                messagebox.showerror("Error", result)
            else:
                self.display_result(result)

    def display_result(self, result):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        result_label = tk.Label(self.result_frame, text="Resultado del Método de Falsa Posición", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=10)

        table_frame = tk.Frame(self.result_frame)
        table_frame.pack(fill="x")

        headers = ["Iteración", "a", "b", "c", "f(a)", "f(b)", "f(c)"]
        for header in headers:
            header_label = tk.Label(table_frame, text=header, font=("Helvetica", 10, "bold"), borderwidth=1, relief="solid")
            header_label.grid(row=0, column=headers.index(header), sticky="nsew")

        for i, (a, b, c, fa, fb, fc) in enumerate(result["iterations"]):
            tk.Label(table_frame, text=i + 1, font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=0, sticky="nsew")
            tk.Label(table_frame, text=f"{a:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=1, sticky="nsew")
            tk.Label(table_frame, text=f"{b:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=2, sticky="nsew")
            tk.Label(table_frame, text=f"{c:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=3, sticky="nsew")
            tk.Label(table_frame, text=f"{fa:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=4, sticky="nsew")
            tk.Label(table_frame, text=f"{fb:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=5, sticky="nsew")
            tk.Label(table_frame, text=f"{fc:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=6, sticky="nsew")

        root_label = tk.Label(self.result_frame, text=f"Raíz aproximada: {result['result']}", font=("Helvetica", 12, "bold"))
        root_label.pack(pady=10)

        # Display the plot
        plot_data = base64.b64decode(result["plot_url"])
        image = Image.open(BytesIO(plot_data))
        photo = ImageTk.PhotoImage(image)
        plot_label = tk.Label(self.result_frame, image=photo)
        plot_label.image = photo
        plot_label.pack()
