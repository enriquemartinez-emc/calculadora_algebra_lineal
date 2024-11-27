from ui.bisection_method_ui import BisectionMethodUI
from ui.cramers_rule_ui import CramersRuleUI
from ui.determinant_of_matrix_ui import DeterminantOfMatrixUI
from ui.gaussian_elimination_ui import GaussianEliminationUI
from ui.inverse_of_matrix_ui import InverseOfMatrixUI
from ui.matrix_equation_ui import MatrixEquationUI
from ui.matrix_product_by_vector_sum_ui import MatrixProductByVectorSumUI
from ui.matrix_product_ui import MatrixProductUI
from ui.row_echelon_ui import RowEchelonUI
from ui.matrix_addition_ui import MatrixAdditionUI
from ui.scalar_product_ui import ScalarProductUI
from ui.transpose_matrix_ui import TransposeMatrixUI
from ui.vector_addition_ui import VectorAdditionUI
from ui.vector_multiplication_ui import VectorMultiplicationUI

class OperationUIFactory:
    _factories = {
        "Gaussian Elimination": GaussianEliminationUI,
        "Row Echelon": RowEchelonUI,
        "Matrix Addition": MatrixAdditionUI,
        "Bisection Method": BisectionMethodUI,
        "Vector Addition": VectorAdditionUI,
        "Vector Multiplication": VectorMultiplicationUI,
        "Transpose Matrix": TransposeMatrixUI,
        "Scalar Product": ScalarProductUI,
        "Matrix Product": MatrixProductUI,
        "Matrix Equation": MatrixEquationUI,
        "Matrix Product by Vector Sum": MatrixProductByVectorSumUI,
        "Determinant of a Matrix": DeterminantOfMatrixUI,
        "Cramer's Rule": CramersRuleUI,
        "Inverse of a Matrix": InverseOfMatrixUI,
    }

    @staticmethod
    def get_operation_ui(operation):
        ui_class = OperationUIFactory._factories.get(operation)
        if ui_class:
            return ui_class()
        return None
