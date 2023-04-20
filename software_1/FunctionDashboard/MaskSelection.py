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

        # plt.figure(MatrixMRI[self.ValueSlice][0].pixel_array, cmap='gray')

        # dataImg = QImage(img.tobytes("raw", "I;16"), img.size[0], img.size[1], QImage.Format_Grayscale16)

        image = QImage(FormatMatrix(MatrixMRI[self.ValueSlice][0].pixel_array), MatrixMRI[self.ValueSlice][0].pixel_array.shape[0],MatrixMRI[self.ValueSlice][0].pixel_array.shape[1], QImage.Format_Grayscale16)

        self.image.setPixmap(QPixmap(image))

        # self.image.setPixmap(QPixmap(plt.imshow(MatrixMRI[self.ValueSlice][0].pixel_array, cmap='gray')))

        # self.selection.clicked.connect(self.RectangularSelec)
        # self.hands.clicked.connect(self.HandsFree)

        self.show()

    def FullImage(self):
        from PostProcessing.MappingTypes.T2 import mappingT2
        mapT2, consMag = mappingT2(self.MatrixMRI[self.ValueSlice][:])
        self.map = mapT2
        Image.fromarray(mapT2)
        return mapT2,consMag

    # def RectangularSelec(self):
    #
    # def HandsFree(self):


