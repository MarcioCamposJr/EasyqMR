from qtpy.QtWidgets import QDialog
from qtpy.QtGui import QPixmap,QImage
from qtpy.uic import loadUi
from PIL import Image
from Preprocessing.FormattingMRI import FormatMatrix

class Mask(QDialog):
    def __init__(self,MatrixMRI, value):

        super(Mask, self).__init__()
        loadUi("G:\Meu Drive\Projeto InBrain 2022\EasyqMRI\software_1\qt.ui\MaskSelection.ui", self)

        self.setWindowTitle("Mask Selection")

        self.MatrixMRI = MatrixMRI
        self.ValueSlice = value

        self.map = None

        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(len(self.MatrixMRI[:])-1)

        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(len(self.MatrixMRI[:])-1)

        self.horizontalScrollBar.valueChanged.connect(self.ChangeImage)
        self.spinBox.valueChanged.connect(self.ChangeImageSP)

        self.horizontalScrollBar.setValue(self.ValueSlice)
        self.spinBox.setValue(self.ValueSlice)

        self.ChangeImage()

        self.full.clicked.connect(self.FullImage)
        # self.selection.clicked.connect(self.RectangularSelec)
        # self.hands.clicked.connect(self.HandsFree)

        self.show()

    def ChangeImage(self, value=None):

        if value is None:
            value = self.horizontalScrollBar.value()
            self.spinBox.setValue(value)

        image = QImage(FormatMatrix(self.MatrixMRI[value][0].pixel_array), self.MatrixMRI[value][0].pixel_array.shape[0], self.MatrixMRI[value][0].pixel_array.shape[1], QImage.Format_Grayscale16)

        self.image.setPixmap(QPixmap(image))

    def ChangeImageSP(self):
        value = self.spinBox.value()

        self.horizontalScrollBar.setValue(value)

        self.ChangeImage(value=value)

    def FullImage(self):
        from PostProcessing.MappingTypes.T2 import mappingT2
        value = self.horizontalScrollBar.value()
        mapT2, consMag = mappingT2(self.MatrixMRI[value][:])
        self.map = mapT2
        Image.fromarray(mapT2)
        return mapT2,consMag

    # def RectangularSelec(self):
    #
    # def HandsFree(self):


