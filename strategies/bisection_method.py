import sympy as sp
import matplotlib.pyplot as plt
from strategies.math_operation_strategy import MathOperationStrategy

class BisectionMethod(MathOperationStrategy):
    def execute(self, function_str, lower_limit, upper_limit, allowed_error):
        x = sp.symbols('x')

        # Validate function
        try:
            function = sp.sympify(function_str)
            if len(function.free_symbols) > 1 or (function.free_symbols and list(function.free_symbols)[0] != x):
                return "La función ingresada debe estar definida en términos de 'x'."
        except sp.SympifyError:
            return "La función ingresada debe estar definida en términos de 'x'."

        # Validate limits
        if lower_limit >= upper_limit:
            return "El límite inferior debe ser menor y diferente del límite superior."

        # Validate allowed error
        if allowed_error <= 0:
            return "El error permitido no puede ser un valor negativo."

        def f(val):
            return float(function.subs(x, val))

        iterations = []
        error_message = None

        original_lower_limit = lower_limit
        original_upper_limit = upper_limit

        while (upper_limit - lower_limit) / 2 > allowed_error:
            midpoint = (lower_limit + upper_limit) / 2
            f_lower = f(lower_limit)
            f_mid = f(midpoint)
            f_upper = f(upper_limit)

            iterations.append((lower_limit, midpoint, upper_limit, f_lower, f_mid, f_upper))

            if (f_lower * f_mid > 0) and (f_upper * f_mid > 0):
                error_message = "El intervalo no contiene raíces de la función."
                break

            if f_lower * f_mid <= 0:
                upper_limit = midpoint
            else:
                lower_limit = midpoint

        root = (lower_limit + upper_limit) / 2
        plot_data = {
            "iterations": iterations,
            "error_message": error_message,
            "root": root,
            "lower_limit": original_lower_limit,
            "upper_limit": original_upper_limit
        }

        return plot_data

    def generate_plot(self, plot_data, function_str):
        x = sp.symbols('x')
        function = sp.sympify(function_str)
        f = sp.lambdify(x, function, "math")

        fig, ax = plt.subplots()

        # Plot function
        lower_limit = plot_data["lower_limit"]
        upper_limit = plot_data["upper_limit"]

        x_vals = [lower_limit + i * (upper_limit - lower_limit) / 400 for i in range(401)]
        y_vals = [f(val) for val in x_vals]
        ax.plot(x_vals, y_vals, label=f'Función: {function_str}')

        # Highlight iterations
        for i, (lower, mid, upper, f_lower, f_mid, f_upper) in enumerate(plot_data["iterations"]):
            ax.plot([lower, upper], [f_lower, f_upper], 'o-', label=f'Iteración {i+1}')

        root = plot_data["root"]
        ax.plot(root, f(root), 'r*', label='Raíz Aproximada')

        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        ax.legend()
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Método de Bisección')

        return fig
