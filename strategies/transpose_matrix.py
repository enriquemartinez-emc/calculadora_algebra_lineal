from strategies.math_operation_strategy import MathOperationStrategy

class TransposeMatrix(MathOperationStrategy):
    def execute(self, matrix):
        transposed_matrix = list(map(list, zip(*matrix)))
        steps = [
            ("Matriz Original:", self.format_matrix(matrix)),
            ("Matriz Transpuesta:", self.format_matrix(transposed_matrix))
        ]
        return {
            "result": self.format_matrix(transposed_matrix),
            "steps": steps
        }

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]

    def format_value(self, value):
        return int(value) if isinstance(value, float) and value.is_integer() else value
