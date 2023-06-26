from qtpy.QtWidgets import QDialog, QApplication
from qtpy.uic import loadUi
import os

class ProgressUI(QDialog):
    def __init__(self):
        super(ProgressUI, self).__init__()

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "qt.ui/ProcessingStepOpen.ui")
        loadUi(path, self)

        self.setWindowTitle("Processing Files")

    def updateProgress(self, percent, labelStep):
        print(labelStep)
        self.progressBar.setValue(percent)
        self.step.setText(str(labelStep))
        QApplication.processEvents()