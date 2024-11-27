import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from factories.operation_factory import OperationFactory
import base64
from io import BytesIO

class FalsePositionMethodUI:
    def __init__(self):
        self.frame = None
        self.result_frame = None

    def create_ui(self, parent, result_frame):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(parent)
        self.frame.pack(anchor="n", fill="both", expand=True)

        self.result_frame = result_frame

        self.control_frame = tk.LabelFrame(self.frame, text="False Position Method")
        self.control_frame.pack(anchor="center", padx=40, pady=20, fill="x")

        self.func_label = tk.Label(self.control_frame, text="Function in terms of 'x':")
        self.func_label.pack(anchor="w")
        self.func_entry = tk.Entry(self.control_frame, width=50)
        self.func_entry.pack(anchor="w")

        self.lower_limit_label = tk.Label(self.control_frame, text="Lower Limit:")
        self.lower_limit_label.pack(anchor="w")
        self.lower_limit_entry = tk.Entry(self.control_frame, width=20)
        self.lower_limit_entry.pack(anchor="w")

        self.upper_limit_label = tk.Label(self.control_frame, text="Upper Limit:")
        self.upper_limit_label.pack(anchor="w")
        self.upper_limit_entry = tk.Entry(self.control_frame, width=20)
        self.upper_limit_entry.pack(anchor="w")

        self.error_label = tk.Label(self.control_frame, text="Allowed Error:")
        self.error_label.pack(anchor="w")
        self.error_entry = tk.Entry(self.control_frame, width=20)
        self.error_entry.pack(anchor="w")

        self.calculate_button = tk.Button(self.control_frame, text="Calculate", command=self.calculate)
        self.calculate_button.pack(anchor="center", pady=10)

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

        result_label = tk.Label(self.result_frame, text="False Position Method Result", font=("Helvetica", 14, "bold"))
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
