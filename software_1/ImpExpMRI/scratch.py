from qtpy.QtWidgets import QDialog, QApplication, QListWidget, QListWidgetItem
from qtpy.uic import loadUi
from qtpy.QtGui import QMovie, QPixmap
from qtpy.QtCore import Qt
from Preprocessing.getinfo import getInfoDicom

import sys

class OpenMRI(QDialog):

    def __init__(self, imageData):

        super(OpenMRI,self).__init__()
        loadUi("C:\Meu Drive\Projeto InBrain 2022\EasyqMRI\software_1\qt.ui\OpenMRI.ui",self)

        self.setWindowTitle("OpenMRI")

        app = QApplication(sys.argv)
        screen = app.primaryScreen()
        sizeScreen = screen.availableGeometry()
        self.resize(sizeScreen.width()*1.78, sizeScreen.height()*1.5)