from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class VectorAddition(MathOperationStrategy):
    def execute(self, vectors, scalars):
        if not self.validate_vectors(vectors):
            return "Todos los vectores deben tener las mismas dimensiones."

        try:
            scalars = [Fraction(scalar) for scalar in scalars]
        except ValueError:
            return "Los escalares deben ser enteros, números con decimales o fracciones; no deben contener letras ni caracteres especiales."

        result_vector = [Fraction(0)] * len(vectors[0])
        steps = []

        for vector_index, (vector, scalar) in enumerate(zip(vectors, scalars)):
            description = f"Multiplicando vector {vector_index + 1} por escalar {scalar}."
            scaled_vector = [scalar * component for component in vector]
            steps.append((description, self.format_vector(scaled_vector)))
            for i in range(len(vector)):
                result_vector[i] += scaled_vector[i]

        steps.append(("Resultado Final", self.format_vector(result_vector)))

        return {
            "result": self.format_vector(result_vector),
            "steps": steps
        }

    def validate_vectors(self, vectors):
        length = len(vectors[0])
        for vector in vectors:
            if len(vector) != length:
                return False
        return True

    def format_vector(self, vector):
        return [self.format_value(component) for component in vector]

    def format_value(self, value):
        if isinstance(value, Fraction):
            return value
        if value.is_integer():
            return int(value)
        return Fraction(value).limit_denominator()
