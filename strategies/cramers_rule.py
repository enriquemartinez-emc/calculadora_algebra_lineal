from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy
from strategies.determinant_of_matrix import DeterminantOfMatrix

class CramersRule(MathOperationStrategy):
    def execute(self, augmented_matrix):
        rows = len(augmented_matrix)
        cols = len(augmented_matrix[0])

        if rows + 1 != cols:
            return "The entered matrix must be square and augmented."

        coefficient_matrix = [row[:-1] for row in augmented_matrix]
        determinant_strategy = DeterminantOfMatrix()
        determinant_result = determinant_strategy.execute(coefficient_matrix)

        if isinstance(determinant_result, dict):
            determinant = determinant_result['result']
        else:
            return determinant_result

        if determinant == 0:
            return "Since the determinant of the matrix is 0, Cramer's rule cannot be applied"

        steps = [
            ("Original Augmented Matrix:", self.format_matrix(augmented_matrix)),
            ("Determinant of the Coefficient Matrix:", self.format_value(determinant))
        ]

        solutions = []
        for i in range(rows):
            modified_matrix = [row[:] for row in coefficient_matrix]
            for j in range(rows):
                modified_matrix[j][i] = augmented_matrix[j][-1]
            modified_determinant_result = determinant_strategy.execute(modified_matrix)
            modified_determinant = modified_determinant_result['result']
            solution = modified_determinant / determinant
            solutions.append(solution)
            steps.append((f"Determinant of the Matrix with Column {i+1} Replaced:", self.format_value(modified_determinant)))

        steps.append(("Solutions:", [self.format_value(solution) for solution in solutions]))

        return {
            "result": [self.format_value(solution) for solution in solutions],
            "steps": steps
        }

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]

    def format_value(self, value):
        if isinstance(value, Fraction) or isinstance(value, int):
            return int(value) if isinstance(value, Fraction) and value.denominator == 1 else value
        return value if value.is_integer() else float(value)
