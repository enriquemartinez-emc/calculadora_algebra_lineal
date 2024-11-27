from strategies.bisection_method import BisectionMethod
from strategies.gaussian_elimination import GaussianElimination
from strategies.row_echelon import RowEchelon
from strategies.matrix_addition import MatrixAddition
from strategies.transpose_matrix import TransposeMatrix
from strategies.vector_addition import VectorAddition
from strategies.vector_multiplication import VectorMultiplication

class OperationFactory:
    _operations = {
        "Gaussian Elimination": GaussianElimination,
        "Row Echelon": RowEchelon,
        "Matrix Addition": MatrixAddition,
        "Bisection Method": BisectionMethod,
        "Vector Addition": VectorAddition,
        "Vector Multiplication": VectorMultiplication,
        "Transpose Matrix": TransposeMatrix
    }

    @staticmethod
    def get_operation(operation):
        operation_class = OperationFactory._operations.get(operation)
        if operation_class:
            return operation_class()
        return None
