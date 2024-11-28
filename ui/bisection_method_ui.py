import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import sec, symbols, sympify, latex, sin, cos, tan, Function
from factories.operation_factory import OperationFactory
from threading import Timer

# Define sec as a SymPy function
class Sec(Function):
    @classmethod
    def eval(cls, x):
        return 1/cos(x)

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
            # Allow parsing of all trigonometric functions, including the custom Sec function
            x = symbols('x')  # Define x as a symbol
            equation = sympify(equation_text, locals={'sin': sin, 'cos': cos, 'tan': tan, 'sec': sec, 'x': x})
            latex_equation = latex(equation)
            self.equation_label_var.set(f"$$ {latex_equation} $$")
        except Exception as e:
            self.equation_label_var.set("Entrada no válida")

    def calculate(self):
        function_str = self.function_entry.get()
        lower_limit = float(self.lower_limit_entry.get())
        upper_limit = float(self.upper_limit_entry.get())
        allowed_error = float(self.error_entry.get())

        # Convert the function string to a SymPy expression
        try:
            x = symbols('x')  # Define x as a symbol
            # Allow parsing of all trigonometric functions, including the custom Sec function
            function_str = sympify(function_str, locals={'sin': sin, 'cos': cos, 'tan': tan, 'sec': Sec, 'x': x})
        except:
            self.display_result({"error_message": "Sintaxis de función no válida."}, function_str)
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
            result_label = tk.Label(self.result_frame, text="Iteraciones del Método de Bisección", font=("Helvetica", 14, "bold"))
            result_label.pack(pady=10)

            table_frame = tk.Frame(self.result_frame)
            table_frame.pack(fill="x")

            headers = ["Iteración", "xi-1", "xi", "xi+1", "f(xi-1)", "f(xi)", "f(xi+1)"]
            for header in headers:
                header_label = tk.Label(table_frame, text=header, font=("Helvetica", 10, "bold"), borderwidth=1, relief="solid")
                header_label.grid(row=0, column=headers.index(header), sticky="nsew")

            for i, (lower, mid, upper, f_lower, f_mid, f_upper) in enumerate(plot_data["iterations"]):
                tk.Label(table_frame, text=i + 1, font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=0, sticky="nsew")
                tk.Label(table_frame, text=f"{lower:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=1, sticky="nsew")
                tk.Label(table_frame, text=f"{mid:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=2, sticky="nsew")
                tk.Label(table_frame, text=f"{upper:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=3, sticky="nsew")
                tk.Label(table_frame, text=f"{f_lower:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=4, sticky="nsew")
                tk.Label(table_frame, text=f"{f_mid:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=5, sticky="nsew")
                tk.Label(table_frame, text=f"{f_upper:.6f}", font=("Helvetica", 10), borderwidth=1, relief="solid").grid(row=i + 1, column=6, sticky="nsew")

            root_label = tk.Label(self.result_frame, text=f"Raíz aproximada: {plot_data['root']:.6f}", font=("Helvetica", 12, "bold"), wraplength=self.result_frame.winfo_width())
            root_label.pack(pady=10)

            operation = OperationFactory.get_operation("Bisection Method")
            fig = operation.generate_plot(plot_data, function_str)

            # Create a frame to hold the canvas
            canvas_frame = tk.Frame(self.result_frame)
            canvas_frame.pack(side="top", fill="both", expand=True)

            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
