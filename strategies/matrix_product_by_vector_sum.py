from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class MatrixProductByVectorSum(MathOperationStrategy):
    def execute(self, matrix, vectors):
        if any(len(vector) != len(vectors[0]) for vector in vectors):
            return "All vectors must have the same dimensions."

        if len(matrix[0]) != len(vectors[0]):
            return "The number of columns in the matrix must equal the number of rows in the vector."

        try:
            vectors = [[Fraction(val) for val in vector] for vector in vectors]
        except ValueError:
            return "Vector values must be integers, numbers with decimals, or fractions."

        vector_sum = [sum(vector[i] for vector in vectors) for i in range(len(vectors[0]))]
        result = [sum(matrix[i][j] * vector_sum[j] for j in range(len(vector_sum))) for i in range(len(matrix))]

        steps = [
            ("Matriz Original:", self.format_matrix(matrix)),
            ("Vectores Originales:", [self.format_vector(vector) for vector in vectors]),
            ("Suma de Vectores:", self.format_vector(vector_sum)),
            ("Resultado:", self.format_vector(result))
        ]

        for i in range(len(matrix)):
            description = f"Calculando elemento en la fila {i+1} de la matriz resultante:"
            computations = [f"{self.format_value(matrix[i][j])} * {self.format_value(vector_sum[j])}" for j in range(len(vector_sum))]
            steps.append((description, computations))

        return {
            "result": self.format_vector(result),
            "steps": steps
        }

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]

    def format_vector(self, vector):
        return [self.format_value(cell) for cell in vector]

    def format_value(self, value):
        if isinstance(value, Fraction):
            return int(value) if value.denominator == 1 else float(value)
        return int(value) if isinstance(value, float) and value.is_integer() else value
