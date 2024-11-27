import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy.parsing.latex import parse_latex
from factories.operation_factory import OperationFactory

class BisectionMethodUI:
    def __init__(self):
        self.frame = None
        self.result_frame = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame)
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        # Function input
        self.function_label = tk.Label(self.control_frame, text="Function f(x):")
        self.function_label.pack(side="top")

        self.function_entry = tk.Entry(self.control_frame)
        self.function_entry.pack(side="top")

        # Lower limit input
        self.lower_limit_label = tk.Label(self.control_frame, text="Lower Limit:")
        self.lower_limit_label.pack(side="top")

        self.lower_limit_entry = tk.Entry(self.control_frame)
        self.lower_limit_entry.pack(side="top")

        # Upper limit input
        self.upper_limit_label = tk.Label(self.control_frame, text="Upper Limit:")
        self.upper_limit_label.pack(side="top")

        self.upper_limit_entry = tk.Entry(self.control_frame)
        self.upper_limit_entry.pack(side="top")

        # Allowed error input
        self.error_label = tk.Label(self.control_frame, text="Allowed Error:")
        self.error_label.pack(side="top")

        self.error_entry = tk.Entry(self.control_frame)
        self.error_entry.pack(side="top")

        self.calculate_button = tk.Button(self.control_frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack(side="top", pady=10)

    def calculate(self):
        function_str = self.function_entry.get()
        lower_limit = float(self.lower_limit_entry.get())
        upper_limit = float(self.upper_limit_entry.get())
        allowed_error = float(self.error_entry.get())

        # Convert LaTeX function to SymPy expression
        try:
            function_str = parse_latex(function_str)
        except:
            self.display_result({"error_message": "Invalid LaTeX function syntax."}, function_str)
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
            
            canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
