import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from factories.operation_factory import OperationFactory
import base64
from io import BytesIO

class SecantMethodUI:
    def __init__(self):
        self.frame = None
        self.result_frame = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame, text="Secant Method")
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        self.func_label = tk.Label(self.control_frame, text="Function in terms of 'x':")
        self.func_label.pack(anchor="w")
        self.func_entry = tk.Entry(self.control_frame, width=50)
        self.func_entry.pack(anchor="w")

        self.initial_value1_label = tk.Label(self.control_frame, text="Initial Value 1:")
        self.initial_value1_label.pack(anchor="w")
        self.initial_value1_entry = tk.Entry(self.control_frame, width=20)
        self.initial_value1_entry.pack(anchor="w")

        self.initial_value2_label = tk.Label(self.control_frame, text="Initial Value 2:")
        self.initial_value2_label.pack(anchor="w")
        self.initial_value2_entry = tk.Entry(self.control_frame, width=20)
        self.initial_value2_entry.pack(anchor="w")

        self.iterations_label = tk.Label(self.control_frame, text="Number of Iterations:")
        self.iterations_label.pack(anchor="w")
        self.iterations_entry = tk.Entry(self.control_frame, width=20)
        self.iterations_entry.pack(anchor="w")

        self.error_label = tk.Label(self.control_frame, text="Allowed Error:")
        self.error_label.pack(anchor="w")
        self.error_entry = tk.Entry(self.control_frame, width=20)
        self.error_entry.pack(anchor="w")

        self.calculate_button = tk.Button(self.control_frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

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

        result_label = tk.Label(self.result_frame, text="Secant Method Result", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=10)

        for description in result["steps"]:
            step_label = tk.Label(self.result_frame, text=description, font=("Helvetica", 10, "italic"))
            step_label.pack()

        final_result_label = tk.Label(self.result_frame, text=f"Root: {result['result']}", font=("Courier", 12, "bold"))
        final_result_label.pack(pady=10)

        # Display the plot
        plot_data = base64.b64decode(result["plot_url"])
        image = Image.open(BytesIO(plot_data))
        photo = ImageTk.PhotoImage(image)
        plot_label = tk.Label(self.result_frame, image=photo)
        plot_label.image = photo
        plot_label.pack()
