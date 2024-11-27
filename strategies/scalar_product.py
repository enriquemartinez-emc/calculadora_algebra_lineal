from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class ScalarProduct(MathOperationStrategy):
    def execute(self, matrix_or_vector, scalar):
        try:
            scalar = Fraction(scalar)
        except ValueError:
            return "The entered scalar must be an integer, a number with decimals or a fraction, it cannot contain letters or special characters."

        if isinstance(matrix_or_vector[0], list):
            result = [[scalar * cell for cell in row] for row in matrix_or_vector]
        else:
            result = [scalar * cell for cell in matrix_or_vector]

        steps = [
            ("Matriz o Vector Original:", self.format_matrix_or_vector(matrix_or_vector)),
            ("Escalar:", self.format_value(scalar)),
            ("Producto Escalar:", self.format_matrix_or_vector(result))
        ]

        return {
            "result": self.format_matrix_or_vector(result),
            "steps": steps
        }

    def format_matrix_or_vector(self, matrix_or_vector):
        if isinstance(matrix_or_vector[0], list):
            return [[self.format_value(cell) for cell in row] for row in matrix_or_vector]
        else:
            return [self.format_value(cell) for cell in matrix_or_vector]

    def format_value(self, value):
        if isinstance(value, Fraction):
            return int(value) if value.denominator == 1 else float(value)
        return int(value) if isinstance(value, float) and value.is_integer() else value
