from ui.gaussian_elimination_ui import GaussianEliminationUI
from ui.row_echelon_ui import RowEchelonUI
from ui.matrix_addition_ui import MatrixAdditionUI

class OperationUIFactory:
    _factories = {
        "Gaussian Elimination": GaussianEliminationUI,
        "Row Echelon": RowEchelonUI,
        "Matrix Addition": MatrixAdditionUI
    }

    @staticmethod
    def get_operation_ui(operation):
        ui_class = OperationUIFactory._factories.get(operation)
        if ui_class:
            return ui_class()
        return None
