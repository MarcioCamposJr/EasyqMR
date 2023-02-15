from qtpy.QtWidgets import QDialog
from qtpy.uic import loadUi
from qtpy.QtGui import QMovie
from Preprocessing.Dicom.getinfo import getInfoDicom

class PreviewGUI(QDialog):

    def __init__(self, imageData):

        super(PreviewGUI,self).__init__()
        loadUi("G:\Meu Drive\Projeto InBrain 2022\EasyqMRI\software_1\qt.ui\preview.ui",self)

        self.setWindowTitle("Preview")

        self.imageData=imageData

        info = getInfoDicom(self.imageData[0])
        self.PatientName.setText(str(info[0]))
        self.BodyPartExamined.setText(str(info[1]))
        self.MRAcquisitionType.setText(str(info[2]))
        self.SeriesDescription.setText(str(info[3]))

        self.SamplingPreviewMRI()
        self.show()
        self.Discard.clicked.connect(self.close)

    def SamplingPreviewMRI(self):

        from Preprocessing.Dicom.OrderSlicesDicom import sort_slices

        self.OrderImageMRI = sort_slices(self.imageData)

        from Preprocessing.Dicom.FilterSlices import SlicesMRI

        slices = SlicesMRI(self.OrderImageMRI)
        self.separeMRI = slices.FewSlices

        from Preprocessing.Dicom.MRIPreviewSample import create_gif

        create_gif(self.separeMRI, 10)
        gif = QMovie("G:\Meu Drive\Projeto InBrain 2022\EasyqMRI\software_1\Docs\Animation\preview.gif")
        self.prev.setMovie(gif)
        gif.start()