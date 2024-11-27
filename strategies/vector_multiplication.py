from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class VectorMultiplication(MathOperationStrategy):
    def execute(self, linear_vector, columnar_vector):
        if len(linear_vector[0]) != len(columnar_vector):
            return "The number of columns in the linear vector must equal the number of rows in the columnar vector."

        try:
            linear_vector = [[Fraction(val) for val in linear_vector[0]]]
            columnar_vector = [[Fraction(row[0])] for row in columnar_vector]
        except ValueError:
            return "Vector values must be integers, numbers with decimals, or fractions."

        result = sum(linear_vector[0][i] * columnar_vector[i][0] for i in range(len(columnar_vector)))

        steps = [
            ("Multiplicación de vectores:", f"{self.clean_format_vector(linear_vector[0])} • {self.clean_format_vector([row[0] for row in columnar_vector])}"),
            ("Paso 1: Producto escalar", [f"{self.clean_format_value(linear_vector[0][i])} * {self.clean_format_value(columnar_vector[i][0])} = {self.clean_format_value(linear_vector[0][i] * columnar_vector[i][0])}" for i in range(len(columnar_vector))]),
            ("Resultado:", self.clean_format_value(result))
        ]

        return {
            "result": self.clean_format_value(result),
            "steps": steps
        }

    def clean_format_vector(self, vector):
        return [self.clean_format_value(component) for component in vector]

    def clean_format_value(self, value):
        if isinstance(value, Fraction):
            return float(value) if value.denominator != 1 else int(value)
        return value
