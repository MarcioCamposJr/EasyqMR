import matplotlib.pyplot as plt

from ImpExpMRI.Dicom import OpenDicom
from ImpExpMRI.NIfTI import OpenNII
from ImpExpMRI import Preview
from ImpExpMRI import OpenMRI

from Preprocessing.FilterSlices import SlicesMRI
from Preprocessing.getinfo import getInfoDicom
from Preprocessing import FormattingMRI
from Preprocessing.BrainExtraction import bet
from Preprocessing.MRIcoregistration import register_slices

from FunctionDashboard.SlidersChangeImage import SliderMRI
from FunctionDashboard.ParameterGraphAnalysis import graphParameter
from FunctionDashboard.MaskSelection import Mask

from qtpy.QtWidgets import QMainWindow, QApplication, QStackedWidget, QSizePolicy
from qtpy.uic import loadUi
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtCore import Qt, QPoint, QPropertyAnimation

import sys
import numpy as np

class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()

        self.MatrixMRI = None
        self.ImageMRI = None
        self.slider = None

        self.infoMapping = None

        loadUi('G:\Meu Drive\Projeto InBrain 2022\EasyqMRI\software_1\qt.ui\main.ui', self)

        self.setMouseTracking(True)

        self.OpenDicom.triggered.connect(self.OpenFolderDicom)
        self.OpenNIFTI.triggered.connect(self.OpenFolderNii)
        self.test.triggered.connect(self.OpenMRI)

        self.horizontalSlider.valueChanged.connect(self.ChangeSlider)
        self.verticalSlider.valueChanged.connect(self.ChangeSlider)

        self.Brightness.valueChanged.connect(self.ChangeSlider)
        self.Contrast.valueChanged.connect(self.ChangeSlider)

        self.bet.clicked.connect(self.Bet)

        self.co_registration.clicked.connect(self.Co_registration)

        self.Maskselection.clicked.connect(self.MaskSelection)

        self.AnalyzeGraph.clicked.connect(self.buttAnalyzeGraph)
        self.AnalyzeGraph.released.connect(self.realeaseSetMap)

    def OpenMRI(self):
        self.Open = OpenMRI.OpenMRI()
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
        self.SlicesMRI = SlicesMRI(self.ImageMRI)
        self.MatrixMRI = self.SlicesMRI.Matrix
        self.OnlySlices = self.SlicesMRI.OnlySlices

        # import nibabel as nib
        #
        # slices = []
        #
        # for i in range(len(self.OnlySlices)):
        #
        #     slices.append(np.array(self.OnlySlices[i].pixel_array))
        #
        #
        # imagem_nifti = nib.Nifti1Image(np.array(slices), np.eye(4))
        # nib.save(imagem_nifti, 'C:/Users/marci/OneDrive/Desktop/MRI/NIFTI/testConvert/test2')

        # if self.SlicesMRI.NumberSlices != 0:
        #     self.condParam = True
        # else:
        #     self.condParam = False

        self.preview.close()

        self.setinfo()

        self.horizontalSlider.setValue(0)
        self.verticalSlider.setValue(0)

        self.horizontalSlider.setMaximum(len(self.MatrixMRI[:]) - 1)

        # sizeConstrast = DefSizeConstrast(self.MatrixMRI, self.condParam)

        self.Contrast.setRange(100,300)

        self.Contrast.setValue(100)

        self.ChangeSlider()

    def ChangeSlider(self):

        if self.ImageMRI is not None:

            if len(self.ImageMRI) != len(self.MatrixMRI[:]):

                valueH = self.horizontalSlider.value()
                valueV = self.verticalSlider.value()

                self.verticalSlider.setMaximum(len(self.MatrixMRI[valueH][:]) - 1)

                bright = self.Brightness.value()
                contrast = self.Contrast.value()

                self.slider = SliderMRI(self.MatrixMRI,valueH, valueV, brightess=bright, contrast=contrast)

                scaledimage = self.slider.imageV.scaled(self.mainImage.size(), Qt.KeepAspectRatio)
                self.mainImage.setPixmap(scaledimage)

            else:
                self.verticalSlider.setMaximum(0)

                valueH = self.horizontalSlider.value()

                bright = self.Brightness.value()
                contrast = (self.Contrast.value())

                self.slider = SliderMRI(self.MatrixMRI ,valueH, brightess=bright, contrast=contrast)

                scaledimage = self.slider.imageH.scaled(self.mainImage.size(), Qt.KeepAspectRatio)
                self.mainImage.setPixmap(scaledimage)

    def MaskSelection(self):

        if self.ImageMRI is not None:
            if len(self.ImageMRI) != len(self.MatrixMRI[:]):
                self.mask = Mask(self.MatrixMRI, self.horizontalSlider.value())
                self.mask.full.clicked.connect(self.setMapping)

    def setMapping(self):

        MapImage = self.mask.FullImage()
        self.mask.close()

        self.infoMapping = MapImage

        mapping = self.infoMapping[0]

        import matplotlib.pyplot as plt
        plt.imshow(np.array(mapping), cmap='rainbow', clim=(0,4000))
        plt.show()

        print(np.amax(np.array(mapping)))

        image = QImage(mapping.tobytes(), mapping.shape[0],mapping.shape[1] , QImage.Format_Grayscale16)
        scaledimage = QPixmap(image).scaled(self.mapping.size(), Qt.KeepAspectRatio)
        self.mapping.setPixmap(scaledimage)

    def buttAnalyzeGraph(self):
        if self.infoMapping is not None:
            if self.AnalyzeGraph.isChecked():
                self.setMouseTracking(True)
            else:
                self.setMouseTracking(False)
        else:
            self.AnalyzeGraph.setChecked(False)

    def realeaseSetMap(self):

        if self.infoMapping is not None:
            mapping = self.infoMapping[0]

            image = QImage(mapping.tobytes(), mapping.shape[0],mapping.shape[1] , QImage.Format_Grayscale16)
            scaledimage = QPixmap(image).scaled(self.mapping.size(), Qt.KeepAspectRatio)
            self.mapping.setPixmap(scaledimage)
            plt.close()

    def mousePressEvent(self, event):
        if self.AnalyzeGraph.isChecked():
            mousePos = self.mapFromGlobal(event.globalPos())

            pixmap_pos = mousePos - (self.mainImage.mapToGlobal(QPoint(0,0))-self.mapToGlobal(QPoint(0,0)))

            if pixmap_pos.x() > 0 and pixmap_pos.y() >0 and pixmap_pos.x() < self.mainImage.size().width() and pixmap_pos.y() < self.mainImage.size().height():

                widthRescaling = int(pixmap_pos.x() * np.array(self.MatrixMRI[0][0].pixel_array).shape[0] / self.mainImage.size().width())
                heightRescaling = int(pixmap_pos.y() * np.array(self.MatrixMRI[0][0].pixel_array).shape[1] / self.mainImage.size().height())
                print(str(self.main))
                indexMRI = self.horizontalSlider.value()

                size = self.mapping.size()
                graph = graphParameter(self.MatrixMRI[indexMRI], self.infoMapping, heightRescaling, widthRescaling, size)

                self.mapping.setPixmap(graph.graph)

        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.ImageMRI is not None:
            mousePos = self.mapFromGlobal(event.globalPos())

            pixmap_pos = mousePos - (self.mainImage.mapToGlobal(QPoint(0, 0)) - self.mapToGlobal(QPoint(0, 0)))

            if pixmap_pos.x() > 0 and pixmap_pos.y() > 0 and pixmap_pos.x() < self.mainImage.size().width() and pixmap_pos.y() < self.mainImage.size().height():
                widthRescaling = int(pixmap_pos.x() * np.array(self.MatrixMRI[0][0].pixel_array).shape[0] / self.mainImage.size().width())
                heightRescaling = int(pixmap_pos.y() * np.array(self.MatrixMRI[0][0].pixel_array).shape[1] / self.mainImage.size().height())

                self.showxcoor.setText("x =" + str(widthRescaling))
                self.showycoor.setText("y =" + str(heightRescaling))

            else:
                anim = QPropertyAnimation(self.showycoor, b"opacity")
                anim.setDuration(1000)
                anim.setStartValue(1.0)
                anim.setEndValue(0.0)
                anim.finished.connect(self.showycoor.hide)
                anim.start()

                anim2 = QPropertyAnimation(self.showxcoor, b"opacity")
                anim2.setDuration(1000)
                anim2.setStartValue(1.0)
                anim2.setEndValue(0.0)
                anim2.finished.connect(self.showxcoor.hide)
                anim2.start()

    def Bet(self):
        if self.ImageMRI is not None:
            if len(self.ImageMRI) != len(self.MatrixMRI[:]):
                self.MatrixMRI = bet(self.MatrixMRI)
                self.ChangeSlider()

    def Co_registration(self):
        if self.ImageMRI is not None:
            if len(self.ImageMRI) != len(self.MatrixMRI[:]):
                self.MatrixMRI = register_slices(self.MatrixMRI)
                self.ChangeSlider()

    def setinfo(self):

        info = getInfoDicom(self.ImageMRI[0])
        # self.pacient.setText(str(info[0]))
        # self.body.setText(str(info[1]))
        # self.type.setText(str(info[2]))
        # self.desc.setText(str(info[3]))
        # self.variation.setText(str(variation_detection(image_mri)))
        # self.clss.setText(str(classification(image_mri)))
    def closeEvent(self, event):
        # Este slot será chamado quando a janela for fechada
        # Encerra o programa
        app.quit()

if __name__ == "__main__":
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
