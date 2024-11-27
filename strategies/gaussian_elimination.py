from fractions import Fraction
from strategies.math_operation_strategy import MathOperationStrategy

class GaussianElimination(MathOperationStrategy):
    def execute(self, matrix):
        # Convert all elements to Fraction
        matrix = [[Fraction(cell) for cell in row] for row in matrix]
        rows, cols = len(matrix), len(matrix[0])  # Number of rows and columns
        original_matrix = [row[:] for row in matrix]
        steps = []
        descriptions = []

        for i in range(min(rows, cols - 1)):  # Adjust to account for augmented column
            # Find the pivot row and swap
            max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            if i != max_row:
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                descriptions.append(f"Swapped row R{i+1} with row R{max_row+1} to position the largest pivot element.")
            else:
                descriptions.append(f"Selected row R{i+1} as pivot because it has the largest absolute value in column {i+1}.")
            steps.append((descriptions[-1], self.format_matrix(matrix)))

            # Make the diagonal element 1 and eliminate below
            pivot = matrix[i][i]
            if pivot != 0:
                for j in range(i + 1, rows):
                    ratio = matrix[j][i] / pivot
                    for k in range(i, cols):
                        matrix[j][k] -= ratio * matrix[i][k]
                    descriptions.append(f"Performed row operation R{j+1} = R{j+1} - ({self.format_value(ratio)}) * R{i+1} to make the element at position ({j+1},{i+1}) zero.")
                    steps.append((descriptions[-1], self.format_matrix(matrix)))
            else:
                descriptions.append(f"Skipped elimination for pivot in row R{i+1} because it is zero.")
                steps.append((descriptions[-1], self.format_matrix(matrix)))

        result = self.format_matrix(matrix)
        variables = self.solve_variables(matrix, rows, cols)

        return {
            "original": self.format_matrix(original_matrix),
            "steps": steps,
            "result": result,
            "variables": variables
        }

    def format_value(self, value):
        if isinstance(value, Fraction):
            return value
        if value.is_integer():
            return int(value)
        return Fraction(value).limit_denominator()

    def format_matrix(self, matrix):
        return [[self.format_value(cell) for cell in row] for row in matrix]

    def solve_variables(self, matrix, rows, cols):
        variables = [Fraction(0)] * (rows)  # Ensure enough space for all variables

        for i in range(rows - 1, -1, -1):
            if matrix[i][i] == 0:
                continue
            variables[i] = matrix[i][cols - 1] / matrix[i][i]
            for k in range(i - 1, -1, -1):
                matrix[k][cols - 1] -= matrix[k][i] * variables[i]

        # Limit denominator to avoid long fractional forms
        return [self.format_value(v) for v in variables]
