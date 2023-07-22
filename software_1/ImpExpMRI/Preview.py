from qtpy.QtWidgets import QDialog
from qtpy.uic import loadUi
from qtpy.QtGui import QMovie,QPixmap

from software_1.ImpExpMRI.ProcessingFile.MRIPreviewSample import create_gif

import os
# from ProcessingFile.getinfo import getInfoDicom

class PreviewGUI(QDialog):

    def __init__(self, imageData):

        super(PreviewGUI,self).__init__()

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "qt.ui/preview.ui")
        loadUi(path,self)

        self.setWindowTitle("Preview")

        self.imageData=imageData

        # info = getInfoDicom(self.imageData[1])
        # self.PatientName.setText(str(info[0]))
        # self.BodyPartExamined.setText(str(info[1]))
        # self.MRAcquisitionType.setText(str(info[2]))
        # self.SeriesDescription.setText(str(info[3]))

        self.SamplingPreviewMRI()
        self.show()
        self.Discard.clicked.connect(self.close)

    def SamplingPreviewMRI(self):

        fewSlices = []

        for i in range(12):
            fewSlices.append(self.imageData[i][0])

        create_gif(fewSlices, 13)

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "Docs\Animation\preview.gif")

        gif = QMovie(path)
        self.prev.setMovie(gif)
        gif.start()