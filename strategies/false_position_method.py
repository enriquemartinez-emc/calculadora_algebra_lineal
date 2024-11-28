from fractions import Fraction
from sympy import sympify, Symbol, lambdify
from strategies.math_operation_strategy import MathOperationStrategy
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class FalsePositionMethod(MathOperationStrategy):
    def execute(self, func_str, lower_limit, upper_limit, allowed_error):
        x = Symbol('x')
        
        try:
            func = sympify(func_str)
        except:
            return "La función ingresada debe estar definida en términos de 'x'. Por favor, verifique."

        if not all(str(symbol) == 'x' for symbol in func.free_symbols):
            return "La función ingresada debe estar definida en términos de 'x'. Por favor, verifique."

        if lower_limit >= upper_limit:
            return "El límite inferior debe ser menor y diferente del límite superior."

        if allowed_error < 0:
            return "El error permitido no puede ser un valor negativo."

        f = lambdify(x, func)

        if f(lower_limit) * f(upper_limit) > 0:
            return "El intervalo ingresado no contiene una raíz de la función."

        x_vals = []
        y_vals = []
        steps = []
        iteration_data = []

        while True:
            f_lower = f(lower_limit)
            f_upper = f(upper_limit)
            midpoint = upper_limit - (f_upper * (lower_limit - upper_limit)) / (f_lower - f_upper)
            f_mid = f(midpoint)
            x_vals.append(midpoint)
            y_vals.append(f_mid)

            iteration_data.append((lower_limit, upper_limit, midpoint, f_lower, f_upper, f_mid))
            steps.append(f"Límite inferior: {self.format_value(lower_limit)}, Límite superior: {self.format_value(upper_limit)}, Punto medio: {self.format_value(midpoint)}, f(Punto medio): {self.format_value(f_mid)}")

            if abs(f_mid) < allowed_error:
                break

            if f_lower * f_mid < 0:
                upper_limit = midpoint
            elif f_upper * f_mid < 0:
                lower_limit = midpoint
            else:
                return "El intervalo ingresado no contiene una raíz de la función."

        plot_url = self.plot_results(func, lower_limit, upper_limit, x_vals, y_vals)

        return {
            "result": self.format_value(midpoint),
            "iterations": iteration_data,
            "plot_url": plot_url
        }

    def plot_results(self, func, lower_limit, upper_limit, x_vals, y_vals):
        x = Symbol('x')
        f = lambdify(x, func)
        x_range = [lower_limit + i * (upper_limit - lower_limit) / 400 for i in range(401)]
        y_range = [f(x) for x in x_range]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_range, y_range, label=str(func))
        plt.scatter(x_vals, y_vals, color='red')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.title('Método de Falsa Posición')
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
        if isinstance(value, Fraction):
            return int(value) if value.denominator == 1 else float(value)
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
