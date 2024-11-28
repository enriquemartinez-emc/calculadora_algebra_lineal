from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy
from strategies.determinant_of_matrix import DeterminantOfMatrix

class CramersRule(MathOperationStrategy):
    def execute(self, augmented_matrix):
        rows = len(augmented_matrix)
        cols = len(augmented_matrix[0])

        if rows + 1 != cols:
            return "La matriz ingresada debe ser cuadrada y aumentada."

        coefficient_matrix, interchange_count = self.get_coefficient_matrix_and_interchanges(augmented_matrix)
        determinant_strategy = DeterminantOfMatrix()
        determinant_result = determinant_strategy.execute(coefficient_matrix)

        if isinstance(determinant_result, dict):
            determinant = determinant_result['result']
        else:
            return determinant_result

        if determinant == 0:
            return "Dado que el determinante de la matriz es 0, no se puede aplicar la regla de Cramer."

        steps = [
            ("Matriz Augmentada Original:", self.format_matrix(augmented_matrix)),
            ("Determinante de la Matriz de Coeficientes:", self.format_value(determinant))
        ]

        solutions = []
        for i in range(rows):
            modified_matrix = [row[:] for row in coefficient_matrix]
            for j in range(rows):
                modified_matrix[j][i] = augmented_matrix[j][-1]
            steps.append((f"Reemplazando la Columna {i+1} con términos independientes:", self.format_matrix(modified_matrix)))
            modified_determinant_result = determinant_strategy.execute(modified_matrix)
            modified_determinant = modified_determinant_result['result']
            solution = Fraction(modified_determinant, determinant)
            solutions.append(solution)
            steps.append((f"Determinante de la Matriz Modificada:", self.format_value(modified_determinant)))
            steps.append((f"Solución para x{i+1}:", f"{self.format_value(modified_determinant)}/{self.format_value(determinant)} = {self.format_value(solution)}"))

        steps.append(("Soluciones:", [self.format_value(solution) for solution in solutions]))

        return {
            "result": [self.format_value(solution) for solution in solutions],
            "steps": steps
        }

    def get_coefficient_matrix_and_interchanges(self, augmented_matrix):
        """Extract the coefficient matrix and count the number of row interchanges required to get the matrix to echelon form"""
        coefficient_matrix = [row[:-1] for row in augmented_matrix]
        interchange_count = 0
        for i in range(len(coefficient_matrix)):
            for j in range(i + 1, len(coefficient_matrix)):
                if coefficient_matrix[i][i] == 0 and coefficient_matrix[j][i] != 0:
                    coefficient_matrix[i], coefficient_matrix[j] = coefficient_matrix[j], coefficient_matrix[i]
                    interchange_count += 1
        return coefficient_matrix, interchange_count

    def format_matrix(self, matrix):
        formatted_matrix = []
        for row in matrix:
            formatted_row = " ".join(f"{int(cell):>8}" if isinstance(cell, (int, float, Fraction)) else f"{cell:>8}" for cell in row)
            formatted_matrix.append(f"[{formatted_row}]")
        return "\n".join(formatted_matrix)

    def format_value(self, value):
        if isinstance(value, Fraction) or isinstance(value, int):
            return int(value) if isinstance(value, Fraction) and value.denominator == 1 else value
        if isinstance(value, float):
            value = Fraction(value).limit_denominator()
        return value
