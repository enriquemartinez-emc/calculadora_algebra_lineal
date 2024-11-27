from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class MatrixEquation(MathOperationStrategy):
    def execute(self, matrix, vector):
        if len(matrix[0]) != len(vector):
            return "The number of columns in the matrix must equal the number of rows in the vector."

        try:
            vector = [Fraction(val) for val in vector]
        except ValueError:
            return "Vector values must be integers, numbers with decimals, or fractions."

        result = [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]
        steps = [
            ("Matriz Original:", self.format_matrix(matrix)),
            ("Vector Original:", self.format_vector(vector))
        ]

        for i in range(len(matrix)):
            description = f"Calculando elemento en la fila {i+1} de la matriz resultante:"
            computations = [f"{self.format_value(matrix[i][j])} * {self.format_value(vector[j])}" for j in range(len(vector))]
            steps.append((description, computations))

        steps.append(("Resultado:", self.format_vector(result)))

        return {
            "result": self.format_vector(result),
            "steps": steps
        }

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]

    def format_vector(self, vector):
        return [self.format_value(cell) for cell in vector]

    def format_value(self, value):
        if isinstance(value, Fraction):
            return int(value) if value.denominator == 1 else float(value)
        return int(value) if isinstance(value, float) and value.is_integer() else value
