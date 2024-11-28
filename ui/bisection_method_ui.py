import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import latex, sympify
from sympy.parsing.latex import parse_latex
from factories.operation_factory import OperationFactory
from threading import Timer

class BisectionMethodUI:
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

        self.control_frame = tk.LabelFrame(self.frame)
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        # Function input
        self.function_label = tk.Label(self.control_frame, text="Función f(x):")
        self.function_label.pack(side="top")

        self.function_entry = tk.Entry(self.control_frame)
        self.function_entry.pack(side="top")
        self.function_entry.bind("<KeyRelease>", self.update_equation_label)

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
        equation_text = self.function_entry.get()
        try:
            equation = parse_latex(equation_text)
            normal_equation = equation
            self.equation_label_var.set(normal_equation)
        except Exception as e:
            self.equation_label_var.set("Entrada no válida")

    def calculate(self):
        function_str = self.function_entry.get()
        lower_limit = float(self.lower_limit_entry.get())
        upper_limit = float(self.upper_limit_entry.get())
        allowed_error = float(self.error_entry.get())

        # Convert LaTeX function to SymPy expression
        try:
            function_str = parse_latex(function_str)
        except:
            self.display_result({"error_message": "Sintaxis de función LaTeX no válida."}, function_str)
            return

        operation = OperationFactory.get_operation("Bisection Method")
        if operation:
            plot_data = operation.execute(str(function_str), lower_limit, upper_limit, allowed_error)
            self.display_result(plot_data, function_str)

    def display_result(self, plot_data, function_str):
        if self.result_frame:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if plot_data.get("error_message"):
            error_label = tk.Label(self.result_frame, text=plot_data["error_message"], font=("Helvetica", 12, "bold"), fg="red")
            error_label.pack()
        else:
            operation = OperationFactory.get_operation("Bisection Method")
            fig = operation.generate_plot(plot_data, str(function_str))

            # Create a frame to hold the canvas
            canvas_frame = tk.Frame(self.result_frame)
            canvas_frame.pack(side="top", fill="both", expand=True)

            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
