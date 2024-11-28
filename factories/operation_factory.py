from strategies.bisection_method import BisectionMethod
from strategies.cramers_rule import CramersRule
from strategies.determinant_of_matrix import DeterminantOfMatrix
from strategies.false_position_method import FalsePositionMethod
from strategies.gaussian_elimination import GaussianElimination
from strategies.inverse_of_matrix import InverseOfMatrix
from strategies.matrix_equation import MatrixEquation
from strategies.matrix_product import MatrixProduct
from strategies.matrix_product_by_vector_sum import MatrixProductByVectorSum
from strategies.newton_raphson_method import NewtonRaphsonMethod
from strategies.row_echelon import RowEchelonForm
from strategies.matrix_addition import MatrixAddition
from strategies.scalar_product import ScalarProduct
from strategies.secant_method import SecantMethod
from strategies.transpose_matrix import TransposeMatrix
from strategies.vector_addition import VectorAddition
from strategies.vector_multiplication import VectorMultiplication

class OperationFactory:
    _operations = {
        "Gaussian Elimination": GaussianElimination,
        "Row Echelon Form": RowEchelonForm,
        "Matrix Addition": MatrixAddition,
        "Bisection Method": BisectionMethod,
        "Vector Addition": VectorAddition,
        "Vector Multiplication": VectorMultiplication,
        "Transpose Matrix": TransposeMatrix,
        "Scalar Product": ScalarProduct,
        "Matrix Product": MatrixProduct,
        "Matrix Equation": MatrixEquation,
        "Matrix Product by Vector Sum": MatrixProductByVectorSum,
        "Determinant of a Matrix": DeterminantOfMatrix,
        "Cramer's Rule": CramersRule,
        "Inverse of a Matrix": InverseOfMatrix,
        "False Position Method": FalsePositionMethod,
        "Newton Raphson Method": NewtonRaphsonMethod,
        "Secant Method": SecantMethod,
    }

    @staticmethod
    def get_operation(operation):
        operation_class = OperationFactory._operations.get(operation)
        if operation_class:
            return operation_class()
        return None
