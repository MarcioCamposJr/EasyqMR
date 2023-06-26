from qtpy.QtWidgets import QDialog
from qtpy.uic import loadUi
import os

class ErrorWarning(QDialog):

    def __init__(self, labelError='oi'):
        super(ErrorWarning, self).__init__()

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "qt.ui/ErrorAlert.ui")
        loadUi(path, self)

        self.oi = 123

        self.setWindowTitle("Error Warning")

        self.error.setText(str(labelError))

        self.errorOk.clicked.connect(self.close)

        self.show()