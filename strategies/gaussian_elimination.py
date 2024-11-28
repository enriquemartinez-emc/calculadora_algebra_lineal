from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class GaussianElimination(MathOperationStrategy):
    def execute(self, augmented_matrix):
        rows = len(augmented_matrix)
        cols = len(augmented_matrix[0])

        if rows + 1 != cols:
            return "La matriz ingresada debe ser cuadrada y aumentada."

        augmented_matrix = [[Fraction(cell) for cell in row] for row in augmented_matrix]

        steps = [("Matriz Inicial:", self.format_matrix(augmented_matrix))]

        for i in range(rows):
            self.pivot(augmented_matrix, i, steps)

            for j in range(i + 1, rows):
                ratio = augmented_matrix[j][i] / augmented_matrix[i][i]
                augmented_matrix[j] = [augmented_matrix[j][k] - ratio * augmented_matrix[i][k] for k in range(cols)]
                steps.append((f"Fila {j + 1} = Fila {j + 1} - ({self.format_value(ratio)}) * Fila {i + 1}", self.format_matrix(augmented_matrix)))

        for i in range(rows - 1, -1, -1):
            ratio = augmented_matrix[i][i]
            augmented_matrix[i] = [augmented_matrix[i][k] / ratio for k in range(cols)]
            steps.append((f"Normalizar Fila {i + 1} dividiendo por {self.format_value(ratio)}", self.format_matrix(augmented_matrix)))

            for j in range(i):
                ratio = augmented_matrix[j][i]
                augmented_matrix[j] = [augmented_matrix[j][k] - ratio * augmented_matrix[i][k] for k in range(cols)]
                steps.append((f"Fila {j + 1} = Fila {j + 1} - ({self.format_value(ratio)}) * Fila {i + 1}", self.format_matrix(augmented_matrix)))

        return {
            "result": self.format_matrix(augmented_matrix),
            "steps": steps
        }

    def pivot(self, matrix, pivot_index, steps):
        max_row = max(range(pivot_index, len(matrix)), key=lambda r: abs(matrix[r][pivot_index]))
        if pivot_index != max_row:
            matrix[pivot_index], matrix[max_row] = matrix[max_row], matrix[pivot_index]
            steps.append((f"Intercambiar Fila {pivot_index + 1} con Fila {max_row + 1}", self.format_matrix(matrix)))

    def format_matrix(self, matrix):
        return '\n'.join(['[' + ' '.join(f"{self.format_value(cell):>8}" for cell in row) + ']' for row in matrix])

    def format_value(self, value):
        return int(value) if value.denominator == 1 else value
