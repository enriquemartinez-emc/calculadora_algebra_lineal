from strategies.gaussian_elimination import GaussianElimination
from strategies.row_echelon import RowEchelon
from strategies.matrix_addition import MatrixAddition

class OperationFactory:
    _operations = {
        "Gaussian Elimination": GaussianElimination,
        "Row Echelon": RowEchelon,
        "Matrix Addition": MatrixAddition
    }

    @staticmethod
    def get_operation(operation):
        operation_class = OperationFactory._operations.get(operation)
        if operation_class:
            return operation_class()
        return None
