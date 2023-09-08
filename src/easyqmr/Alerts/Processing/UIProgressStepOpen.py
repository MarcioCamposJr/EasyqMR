from qtpy.QtWidgets import QDialog, QApplication
from qtpy.uic import loadUi
from qtpy.QtCore import Qt
import os

class ProgressUI(QDialog):
    def __init__(self, Title = None):
        super(ProgressUI, self).__init__()

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "qt.ui/ProcessingStepOpen.ui")
        loadUi(path, self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(Title)

    def updateProgress(self, percent, labelStep):
        print(labelStep)
        self.progressBar.setValue(percent)
        self.step.setText(str(labelStep))
        QApplication.processEvents()