from sympy import sympify, Symbol, lambdify
from strategies.math_operation_strategy import MathOperationStrategy
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class SecantMethod(MathOperationStrategy):
    def execute(self, func_str, initial_value1, initial_value2, iterations, allowed_error):
        x = Symbol('x')
        
        try:
            func = sympify(func_str)
        except:
            return "The entered function must be defined in terms of ‘x’, please check."

        if not all(str(symbol) == 'x' for symbol in func.free_symbols):
            return "The entered function must be defined in terms of ‘x’, please check."

        if allowed_error < 0:
            return "The error to be considered cannot be a negative value"

        f = lambdify(x, func)

        current_value1 = initial_value1
        current_value2 = initial_value2
        steps = []
        x_vals = [current_value1, current_value2]
        y_vals = [f(current_value1), f(current_value2)]

        for i in range(iterations):
            f_value1 = f(current_value1)
            f_value2 = f(current_value2)

            if f_value1 == f_value2:
                return "The method fails due to division by zero."

            next_value = current_value2 - f_value2 * (current_value2 - current_value1) / (f_value2 - f_value1)
            steps.append(f"Iteration {i+1}: Current value1: {self.format_value(current_value1)}, Current value2: {self.format_value(current_value2)}, f(Current value1): {self.format_value(f_value1)}, f(Current value2): {self.format_value(f_value2)}, Next value: {self.format_value(next_value)}")
            x_vals.append(next_value)
            y_vals.append(f(next_value))

            if abs(next_value - current_value2) < allowed_error:
                plot_url = self.plot_results(func, x_vals, y_vals)
                return {
                    "result": self.format_value(next_value),
                    "steps": steps,
                    "plot_url": plot_url
                }

            current_value1 = current_value2
            current_value2 = next_value

        return f"A root of the function was not found with the initial values {self.format_value(initial_value1)} and {self.format_value(initial_value2)} in {iterations} iterations."

    def plot_results(self, func, x_vals, y_vals):
        x = Symbol('x')
        f = lambdify(x, func)
        x_range = [x_vals[0] + i * (x_vals[-1] - x_vals[0]) / 400 for i in range(401)]
        y_range = [f(x) for x in x_range]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_range, y_range, label=str(func))
        plt.scatter(x_vals, y_vals, color='red')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.title('Secant Method')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        plt.grid(True)

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_data = buf.getvalue()
        buf.close()
        
        plot_url = base64.b64encode(plot_data).decode('utf-8')
        return plot_url

    def format_value(self, value):
        return int(value) if isinstance(value, float) and value.is_integer() else value
