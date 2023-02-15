from PIL import Image
from qtpy.QtGui import QImage,QPixmap
import numpy as np

class SliderMRI():

    def __init__(self, image, valueH, valueV = None, contrast=65, brightess = 5):

        self.imageV = self.ParameterMRI(image, valueH, valueV, contrast, brightess)
        self.imageH = self.SliceMRI(image,valueH,contrast,valueV, brightess)

    def SliceMRI(self,image,value,cont,valueV, brightess):

        if valueV is not None:
            img = Image.fromarray( self.to_8bit((image[value][0].pixel_array*cont) + brightess ))
        else:
            img = Image.fromarray(self.to_8bit((image[value].pixel_array*cont) + brightess ))

        dataImg = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_Grayscale8)

        return QPixmap.fromImage(dataImg)

    def ParameterMRI(self, image, valueH, valueV, cont, brightess):

        if valueV is not None:
            img = Image.fromarray(self.to_8bit((image[valueH][valueV].pixel_array*cont) + brightess ))
            dataImg = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_Grayscale8)

            return QPixmap.fromImage(dataImg)

        else:
            return None

    def to_8bit(self, matrix):
        # Normalize the matrix to the range [0, 1]
        matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

        # Convert the matrix to 16-bit unsigned integers
        matrix = (matrix * 256).astype(np.uint8)

        return matrix