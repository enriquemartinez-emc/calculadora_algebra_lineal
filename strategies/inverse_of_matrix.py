from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class InverseOfMatrix(MathOperationStrategy):
    def execute(self, matrix):
        n = len(matrix)
        identity_matrix = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
        augmented_matrix = [row + identity_matrix[i] for i, row in enumerate(matrix)]
        steps = [("Matriz Augmentada Inicial", self.format_matrix(augmented_matrix))]

        # Perform Gaussian Elimination
        for i in range(n):
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                for k in range(i + 1, n):
                    if augmented_matrix[k][i] != 0:
                        augmented_matrix[i], augmented_matrix[k] = augmented_matrix[k], augmented_matrix[i]
                        break
                pivot = augmented_matrix[i][i]

            augmented_matrix[i] = [x / pivot for x in augmented_matrix[i]]
            steps.append((f"Dividiendo Fila {i + 1} por {pivot}", self.format_matrix(augmented_matrix)))

            for j in range(n):
                if i != j:
                    ratio = augmented_matrix[j][i]
                    augmented_matrix[j] = [augmented_matrix[j][x] - ratio * augmented_matrix[i][x] for x in range(len(augmented_matrix[j]))]
                    steps.append((f"Restando {ratio} * Fila {i + 1} de Fila {j + 1}", self.format_matrix(augmented_matrix)))

        inverse_matrix = [row[n:] for row in augmented_matrix]
        steps.append(("Matriz Inversa", self.format_matrix(inverse_matrix)))
        
        return {
            "result": self.format_matrix(inverse_matrix),
            "steps": steps
        }

    def format_matrix(self, matrix):
        formatted_matrix = ['[' + ' '.join(f"{self.format_value(cell):>8}" for cell in row) + ']' for row in matrix]
        return '\n'.join(formatted_matrix)

    def format_value(self, value):
        return int(value) if value.denominator == 1 else value
