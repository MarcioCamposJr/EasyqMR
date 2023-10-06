from qtpy.QtWidgets import QDialog, QApplication
from qtpy.uic import loadUi
from qtpy.QtGui import QMovie
from qtpy.QtCore import Qt
import os

class Processing1(QDialog):

    def __init__(self, labelStep, parent):
        super(Processing1, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        path = os.path.dirname(os.path.abspath('None'))
        path_ui = os.path.join(path, "qt.ui/Processing1.ui")
        loadUi(path_ui, self)

        self.setWindowTitle("Processing")

        gif_path = os.path.join(path, "Docs/icon/loadingGif2.gif")
        self.fileGif = QMovie(gif_path)
        self.gif.setMovie(self.fileGif)

        self.fileGif.start()
        QApplication.processEvents()
        self.step.setText(str(labelStep))

        self.show()
