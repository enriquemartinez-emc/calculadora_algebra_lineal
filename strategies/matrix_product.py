from strategies.math_operation_strategy import MathOperationStrategy

class MatrixProduct(MathOperationStrategy):
    def execute(self, matrix1, matrix2):
        if len(matrix1[0]) != len(matrix2):
            return "El número de columnas en la primera matriz y el número de filas en la segunda matriz deben ser iguales."

        result = [[0] * len(matrix2[0]) for _ in range(len(matrix1))]
        steps = [
            ("Matriz 1:", self.format_matrix(matrix1)),
            ("Matriz 2:", self.format_matrix(matrix2))
        ]

        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                result[i][j] = sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix2)))
                calculations = [f"{self.format_value(matrix1[i][k])} * {self.format_value(matrix2[k][j])}" for k in range(len(matrix2))]
                steps.append((f"Calculando elemento ({i+1},{j+1})", calculations))

        steps.append(("Resultado:", self.format_matrix(result)))

        return {
            "result": self.format_matrix(result),
            "steps": steps
        }

    def format_matrix(self, matrix):
        return ['[' + ' '.join(f"{self.format_value(cell):>8}" for cell in row) + ']' for row in matrix]

    def format_value(self, value):
        return int(value) if isinstance(value, float) and value.is_integer() else value
