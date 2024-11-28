from sympy import sympify, Symbol, diff, lambdify
from strategies.math_operation_strategy import MathOperationStrategy
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class NewtonRaphsonMethod(MathOperationStrategy):
    def execute(self, func_str, initial_value, iterations, allowed_error):
        x = Symbol('x')
        
        try:
            func = sympify(func_str)
        except:
            return "La función ingresada debe estar definida en términos de 'x'. Por favor, verifique."

        if not all(str(symbol) == 'x' for symbol in func.free_symbols):
            return "La función ingresada debe estar definida en términos de 'x'. Por favor, verifique."

        if allowed_error < 0:
            return "El error permitido no puede ser un valor negativo."

        f = lambdify(x, func)
        f_prime = lambdify(x, diff(func, x))

        current_value = initial_value
        iteration_steps = []
        x_vals = [current_value]
        y_vals = [f(current_value)]

        for i in range(iterations):
            f_current = f(current_value)
            f_prime_current = f_prime(current_value)

            if f_prime_current == 0:
                return "La derivada es cero, el método falla."

            next_value = current_value - f_current / f_prime_current
            ea = abs((next_value - current_value) / next_value) if next_value != 0 else float('inf')
            iteration_steps.append((i + 1, current_value, next_value, ea, f_current, f_prime_current))
            x_vals.append(next_value)
            y_vals.append(f(next_value))

            if ea < allowed_error:
                plot_url = self.plot_results(func, x_vals, y_vals)
                return {
                    "result": self.format_value(next_value),
                    "iterations": iteration_steps,
                    "plot_url": plot_url
                }

            current_value = next_value

        plot_url = self.plot_results(func, x_vals, y_vals)
        return {
            "result": self.format_value(current_value),
            "iterations": iteration_steps,
            "plot_url": plot_url
        }

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
        plt.title('Newton-Raphson Method')
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
