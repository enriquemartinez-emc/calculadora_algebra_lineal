from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class DeterminantOfMatrix(MathOperationStrategy):
    def execute(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        
        if rows != cols:
            return "The matrix entered must be square."

        matrix = [[Fraction(cell) for cell in row] for row in matrix]
        steps = [("Matriz Original:", self.format_matrix(matrix))]
        exchanges = 0

        for i in range(rows):
            max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            if i != max_row:
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                exchanges += 1
                steps.append((f"Intercambié la fila {i+1} con la fila {max_row+1}", self.format_matrix(matrix)))
            for j in range(i + 1, rows):
                if matrix[i][i] == 0:
                    continue
                ratio = matrix[j][i] / matrix[i][i]
                for k in range(i, cols):
                    matrix[j][k] -= ratio * matrix[i][k]
                steps.append((f"Realicé la operación R{j+1} = R{j+1} - ({self.format_value(ratio)}) * R{i+1}", self.format_matrix(matrix)))

        determinant = (-1 if exchanges % 2 else 1) * self.product_of_diagonal(matrix)
        steps.append(("Determinante Calculado:", determinant))

        return {
            "result": determinant,
            "steps": steps
        }

    def product_of_diagonal(self, matrix):
        product = 1
        for i in range(len(matrix)):
            product *= matrix[i][i]
        return product

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]

    def format_value(self, value):
        return int(value) if isinstance(value, Fraction) and value.denominator == 1 else float(value)
