from qtpy.QtWidgets import QDialog
import os
from qtpy.QtCore import Qt
from qtpy.uic import loadUi
class WindowAbout(QDialog):

    def __init__(self, parent):

        super(WindowAbout,self).__init__(parent)

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "qt.ui/AboutUs.ui")
        loadUi(path, self)

        self.setWindowTitle("About Us")
        self.setFixedSize(self.size())
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.show()