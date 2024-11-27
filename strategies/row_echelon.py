from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class RowEchelon(MathOperationStrategy):
    def execute(self, matrix):
        matrix = [[Fraction(cell) for cell in row] for row in matrix]
        rows, cols = len(matrix), len(matrix[0])
        original_matrix = [row[:] for row in matrix]
        steps = []
        descriptions = []

        for i in range(rows):
            # Find the pivot row with the maximum element in the current column
            max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            if i != max_row:
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                descriptions.append(f"Intercambié la fila R{i+1} con la fila R{max_row+1} para posicionar el mayor elemento pivote.")
            else:
                descriptions.append(f"Seleccioné la fila R{i+1} como pivote porque tiene el mayor valor absoluto en la columna {i+1}.")
            steps.append((descriptions[-1], self.format_matrix(matrix)))

            pivot = matrix[i][i]
            if pivot != 0:
                for j in range(i + 1, rows):
                    ratio = matrix[j][i] / pivot
                    for k in range(i, cols):
                        matrix[j][k] -= ratio * matrix[i][k]
                    descriptions.append(f"Realicé la operación R{j+1} = R{j+1} - ({self.format_value(ratio)}) * R{i+1} para hacer cero el elemento en la posición ({j+1},{i+1}).")
                    steps.append((descriptions[-1], self.format_matrix(matrix)))
            else:
                descriptions.append(f"Se saltó la eliminación para el pivote en la fila R{i+1} porque es cero.")
                steps.append((descriptions[-1], self.format_matrix(matrix)))

        result = self.format_matrix(matrix)

        return {
            "original": self.format_matrix(original_matrix),
            "steps": steps,
            "result": result
        }

    def format_value(self, value):
        if isinstance(value, Fraction):
            return value
        if value.is_integer():
            return int(value)
        return Fraction(value).limit_denominator()

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]
