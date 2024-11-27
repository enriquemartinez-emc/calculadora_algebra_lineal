from ui.bisection_method_ui import BisectionMethodUI
from ui.gaussian_elimination_ui import GaussianEliminationUI
from ui.row_echelon_ui import RowEchelonUI
from ui.matrix_addition_ui import MatrixAdditionUI
from ui.vector_addition_ui import VectorAdditionUI

class OperationUIFactory:
    _factories = {
        "Gaussian Elimination": GaussianEliminationUI,
        "Row Echelon": RowEchelonUI,
        "Matrix Addition": MatrixAdditionUI,
        "Bisection Method": BisectionMethodUI,
        "Vector Addition": VectorAdditionUI
    }

    @staticmethod
    def get_operation_ui(operation):
        ui_class = OperationUIFactory._factories.get(operation)
        if ui_class:
            return ui_class()
        return None
