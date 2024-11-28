from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class RowEchelonForm(MathOperationStrategy):
    def execute(self, augmented_matrix):
        rows = len(augmented_matrix)
        cols = len(augmented_matrix[0])

        if cols <= rows:
            return "La matriz ingresada debe ser aumentada."

        augmented_matrix = [[Fraction(cell) for cell in row] for row in augmented_matrix]

        steps = [("Matriz Inicial:", self.format_matrix(augmented_matrix))]

        for i in range(min(rows, cols - 1)):
            self.pivot(augmented_matrix, i, steps)
            self.eliminate_below(augmented_matrix, i, steps)

        for i in range(rows - 1, -1, -1):
            leading_value = next((augmented_matrix[i][j] for j in range(cols) if augmented_matrix[i][j] != 0), None)
            if leading_value and leading_value != 1:
                augmented_matrix[i] = [val / leading_value for val in augmented_matrix[i]]
                steps.append((f"Normalizar Fila {i + 1} dividiendo por {self.format_value(leading_value)}", self.format_matrix(augmented_matrix)))
            self.eliminate_above(augmented_matrix, i, steps)

        return {
            "result": self.format_matrix(augmented_matrix),
            "steps": steps
        }

    def pivot(self, matrix, pivot_index, steps):
        max_row = max(range(pivot_index, len(matrix)), key=lambda r: abs(matrix[r][pivot_index]))
        if pivot_index != max_row:
            matrix[pivot_index], matrix[max_row] = matrix[max_row], matrix[pivot_index]
            steps.append((f"Intercambiar Fila {pivot_index + 1} con Fila {max_row + 1}", self.format_matrix(matrix)))

    def eliminate_below(self, matrix, pivot_index, steps):
        rows = len(matrix)
        cols = len(matrix[0])
        pivot_value = matrix[pivot_index][pivot_index]
        for i in range(pivot_index + 1, rows):
            ratio = matrix[i][pivot_index] / pivot_value
            matrix[i] = [matrix[i][j] - ratio * matrix[pivot_index][j] for j in range(cols)]
            steps.append((f"Fila {i + 1} = Fila {i + 1} - ({self.format_value(ratio)}) * Fila {pivot_index + 1}", self.format_matrix(matrix)))

    def eliminate_above(self, matrix, pivot_index, steps):
        for i in range(pivot_index - 1, -1, -1):
            ratio = matrix[i][pivot_index]
            matrix[i] = [matrix[i][j] - ratio * matrix[pivot_index][j] for j in range(len(matrix[0]))]
            steps.append((f"Fila {i + 1} = Fila {i + 1} - ({self.format_value(ratio)}) * Fila {pivot_index + 1}", self.format_matrix(matrix)))

    def format_matrix(self, matrix):
        return '\n'.join(['[' + ' '.join(f"{self.format_value(cell):>8}" for cell in row) + ']' for row in matrix])

    def format_value(self, value):
        return int(value) if value.denominator == 1 else value
