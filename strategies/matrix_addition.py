from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class MatrixAddition(MathOperationStrategy):
    def execute(self, matrices, scalars):
        if not self.validate_matrices(matrices):
            return "All matrices must have the same dimensions."

        try:
            scalars = [Fraction(scalar) for scalar in scalars]
        except ValueError:
            return "Scalars must be integers, numbers with decimals, or fractions; they must not contain letters or special characters."

        rows, cols = len(matrices[0]), len(matrices[0][0])
        result_matrix = [[Fraction(0) for _ in range(cols)] for _ in range(rows)]
        steps = []

        for matrix_index, (matrix, scalar) in enumerate(zip(matrices, scalars)):
            description = f"Multiplying matrix {matrix_index + 1} by scalar {scalar}."
            steps.append((description, self.format_matrix([[scalar * cell for cell in row] for row in matrix])))
            for i in range(rows):
                for j in range(cols):
                    result_matrix[i][j] += scalar * matrix[i][j]

        steps.append(("Final Result", self.format_matrix(result_matrix)))

        result = self.format_matrix(result_matrix)
        return {
            "result": result,
            "steps": steps
        }

    def validate_matrices(self, matrices):
        rows, cols = len(matrices[0]), len(matrices[0][0])
        for matrix in matrices:
            if len(matrix) != rows or any(len(row) != cols for row in matrix):
                return False
        return True

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]

    def format_value(self, value):
        if isinstance(value, Fraction):
            return value
        if value.is_integer():
            return int(value)
        return Fraction(value).limit_denominator()
