from qtpy.QtWidgets import QDialog
from qtpy.uic import loadUi
from qtpy.QtCore import Qt
import os

class ErrorWarning(QDialog):

    def __init__(self, labelError):
        super(ErrorWarning, self).__init__()

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "qt.ui/ErrorAlert.ui")
        loadUi(path, self)

        self.setWindowTitle("Error Warning")

        self.error.setText(str(labelError))

        self.errorOk.clicked.connect(self.close)

        self.show()