from ImpExpMRI.Dicom import OpenDicom
from ImpExpMRI.NIfTI import OpenNII
from ImpExpMRI import Preview

from Preprocessing.FilterSlices import SlicesMRI
from Preprocessing.getinfo import getInfoDicom
from Preprocessing import FormattingMRI

from FunctionDashboard.SlidersChangeImage import SliderMRI

from FunctionDashboard.MaskSelection import Mask

from qtpy.QtWidgets import QMainWindow, QApplication, QStackedWidget, QSizePolicy
from qtpy.uic import loadUi
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtCore import Qt

import sys

class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()

        self.MatrixMRI = None
        self.ImageMRI = None
        self.slider = None

        loadUi('G:\Meu Drive\Projeto InBrain 2022\EasyqMRI\software_1\qt.ui\main.ui', self)

        self.OpenDicom.triggered.connect(self.OpenFolderDicom)
        self.OpenNIFTI.triggered.connect(self.OpenFolderNii)

        self.horizontalSlider.valueChanged.connect(self.ChangeSlider)
        self.verticalSlider.valueChanged.connect(self.ChangeSlider)

        self.Brightness.valueChanged.connect(self.ChangeSlider)
        self.Contrast.valueChanged.connect(self.ChangeSlider)

        self.Maskselection.clicked.connect(self.MaskSelection)

    def OpenFolderDicom(self):

        importData = OpenDicom.OpenMRI()

        if importData.path:
            image_type = 'DICOM'
            imageData = importData.imageMRI
            self.Preview(imageData, image_type)

    def OpenFolderNii(self):

        importData = OpenNII.OpenNII()

        if importData.path:
            image_type = 'NIfTI'
            imageData = importData.imageMRI
            self.Preview(imageData, image_type)

    def Preview(self, imageData, image_type):
        MRI = FormattingMRI.FormattedMRI(imageData, image_type)
        self.preview = Preview.PreviewGUI(MRI)
        self.preview.Open.clicked.connect(self.CheckImage)

    def CheckImage(self):

        self.ImageMRI = self.preview.OrderImageMRI
        self.MatrixMRI = SlicesMRI(self.preview.OrderImageMRI).Matrix

        self.preview.close()

        self.setinfo()

        self.horizontalSlider.setValue(0)
        self.verticalSlider.setValue(0)

        self.horizontalSlider.setMaximum(len(self.MatrixMRI[:]) - 1)

        self.ChangeSlider()

    def ChangeSlider(self):

        if self.ImageMRI is not None:

            if len(self.ImageMRI) != len(self.MatrixMRI[:]):

                valueH = self.horizontalSlider.value()
                valueV = self.verticalSlider.value()

                self.verticalSlider.setMaximum(len(self.MatrixMRI[valueH][:]) - 1)

                bright = self.Brightness.value()
                contrast = self.Contrast.value()

                self.slider = SliderMRI(self.MatrixMRI, valueH, valueV, brightess=bright, contrast=contrast)

                scaledimage = self.slider.imageV.scaled(self.mainImage.size(), Qt.KeepAspectRatio)
                self.mainImage.setPixmap(scaledimage)

            else:
                self.verticalSlider.setMaximum(0)

                valueH = self.horizontalSlider.value()

                bright = self.Brightness.value()
                contrast = self.Contrast.value()

                self.slider = SliderMRI(self.MatrixMRI, valueH, brightess=bright, contrast=contrast)

                scaledimage = self.slider.imageH.scaled(self.mainImage.size(), Qt.KeepAspectRatio)
                self.mainImage.setPixmap(scaledimage)

    def MaskSelection(self):

        if self.ImageMRI is not None:
            if len(self.ImageMRI) != len(self.MatrixMRI[:]):
                self.mask = Mask(self.MatrixMRI, self.horizontalSlider.value(), self.Contrast.value())
                self.mask.full.clicked.connect(self.setMapping)

    def setMapping(self):

        MapImage = self.mask.FullImage()
        self.mask.close()

        import matplotlib.pyplot as plt
        plt.imshow(MapImage, cmap='gray', clim=(0, 256))
        plt.show()

        # def filtro(x):
        #     return x<256
        #
        # MapImage = list(filter(filtro,MapImage))

        image = QImage(MapImage, len(MapImage[:][0]), len(MapImage[:]), QImage.Format_Grayscale16)
        scaledimage = QPixmap(image).scaled(self.mapping.size(), Qt.KeepAspectRatio)
        self.mapping.setPixmap(scaledimage)

    def setinfo(self):

        info = getInfoDicom(self.ImageMRI[0])
        # self.pacient.setText(str(info[0]))
        # self.body.setText(str(info[1]))
        # self.type.setText(str(info[2]))
        # self.desc.setText(str(info[3]))
        # self.variation.setText(str(variation_detection(image_mri)))
        # self.clss.setText(str(classification(image_mri)))


app = QApplication(sys.argv)

screen = app.primaryScreen()
sizeScreen = screen.availableGeometry()

mainwindow = MainWindow()
widget = QStackedWidget()
widget.addWidget(mainwindow)

widget.setWindowTitle("EasyqMR")

policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
policy.setHeightForWidth(True)
widget.setSizePolicy(policy)

widget.setMinimumWidth(sizeScreen.width()*(2/3))
widget.setMinimumHeight(sizeScreen.height()*(2/3))

widget.showMaximized()

widget.show()

app.exec_()
sys.exit(app.exec_())
