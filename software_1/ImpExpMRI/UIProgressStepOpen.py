from qtpy.QtWidgets import QDialog, QApplication
from qtpy.uic import loadUi
from PyQt5.QtCore import QThread, pyqtSignal

class ProgressUI(QDialog):
    def __init__(self):
        super(ProgressUI, self).__init__()
        loadUi("C:/Users/marci/OneDrive/Desktop/EasyqMRI/software_1/qt.ui/ProcessingStepOpen.ui", self)

        self.setWindowTitle("Processing Files")

    def updateProgress(self, percent, labelStep):
        print(labelStep)
        self.progressBar.setValue(percent)
        self.step.setText(str(labelStep))
        QApplication.processEvents()