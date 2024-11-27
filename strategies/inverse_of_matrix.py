from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy
from strategies.determinant_of_matrix import DeterminantOfMatrix

class InverseOfMatrix(MathOperationStrategy):
    def execute(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])

        if rows != cols:
            return "The entered matrix is not square."

        determinant_strategy = DeterminantOfMatrix()
        determinant_result = determinant_strategy.execute(matrix)

        if isinstance(determinant_result, dict):
            determinant = determinant_result['result']
        else:
            return determinant_result

        if determinant == 0:
            return "Since the matrix is singular (determinant = 0) it has no inverse"

        inverse_matrix = self.adjoint(matrix)
        for i in range(rows):
            for j in range(cols):
                inverse_matrix[i][j] = inverse_matrix[i][j] / determinant

        steps = [
            ("Original Matrix:", self.format_matrix(matrix)),
            ("Determinant of the Matrix:", self.format_value(determinant)),
            ("Inverse Matrix Calculation Steps:", "Calculated the adjoint matrix and divided each element by the determinant."),
            ("Inverse Matrix:", self.format_matrix(inverse_matrix))
        ]

        return {
            "result": self.format_matrix(inverse_matrix),
            "steps": steps
        }

    def adjoint(self, matrix):
        rows = len(matrix)
        adj_matrix = [[0] * rows for _ in range(rows)]

        for i in range(rows):
            for j in range(rows):
                minor = [[matrix[x][y] for y in range(rows) if y != j] for x in range(rows) if x != i]
                determinant_strategy = DeterminantOfMatrix()
                determinant_result = determinant_strategy.execute(minor)
                cofactor = determinant_result['result']
                adj_matrix[j][i] = (-1) ** (i + j) * cofactor

        return adj_matrix

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]

    def format_value(self, value):
        if isinstance(value, Fraction):
            return int(value) if value.denominator == 1 else float(value)
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
