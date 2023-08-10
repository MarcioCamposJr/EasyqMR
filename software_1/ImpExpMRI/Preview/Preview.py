from qtpy.QtWidgets import QDialog, QApplication
from qtpy.uic import loadUi
from qtpy.QtGui import QMovie
from qtpy.QtCore import Qt

from software_1.ImpExpMRI.Preview.MRIPreviewSample import create_gif
from software_1.Alerts.Processing.Processing1 import Processing1

import os

class PreviewGUI(QDialog):

    def __init__(self, imageData, parent):

        super(PreviewGUI,self).__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.processingCreateGif = Processing1('Preparing preview screen', self)
        self.processingCreateGif.show()
        QApplication.processEvents()

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "qt.ui/preview.ui")
        loadUi(path, self)

        self.setFixedSize(self.size())
        self.setWindowTitle("Preview")

        self.imageData=imageData

        self.PatientName.setText(str(self.imageData[0][0].PatientName))
        self.BodyPartExamined.setText(str(self.imageData[0][0].BodyPartExamined))
        self.MRAcquisitionType.setText(str(self.imageData[0][0].MRAcquisitionType))
        self.SeriesDescription.setText(str(self.imageData[0][0].SeriesDescription))

        self.SamplingPreviewMRI()

        self.show()

        self.Discard.clicked.connect(self.close)

    def SamplingPreviewMRI(self):

        fewSlices = []

        for i in range(len(self.imageData)):
            fewSlices.append(self.imageData[i][0])

        create_gif(fewSlices, 13)

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "Docs\Animation\preview.gif")

        self.gif = QMovie(path)
        self.prev.setMovie(self.gif)
        self.gif.start()

        self.processingCreateGif.close()