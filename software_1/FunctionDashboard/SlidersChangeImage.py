from PIL import Image
from qtpy.QtGui import QImage,QPixmap
import numpy as np
import cv2
from software_1.Preprocessing.FormattingMatrix import FormatMatrix

class SliderMRI():

    def __init__(self,image,valueH, valueV = None, contrast=65, brightess = 5):

        self.imageV = self.ParameterMRI(image, valueH, valueV, contrast, brightess)
        self.imageH = self.SliceMRI(image,valueH,contrast,valueV, brightess)

    def SliceMRI(self,image,value,cont,valueV, brightess):

        if valueV is not None:
            image = self.apply_contrast_brightness(image[value][0].pixel_array,cont,brightess)
            img = Image.fromarray(image)
        else:
            image = self.apply_contrast_brightness(image[value].pixel_array, cont, brightess)
            img = Image.fromarray(image)

        dataImg = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_Grayscale16)

        return QPixmap.fromImage(dataImg)

    def ParameterMRI(self, image, valueH, valueV, cont, brightess):

        if valueV is not None:
            image = self.apply_contrast_brightness(image[valueH][valueV].pixel_array, cont, brightess)

            img = Image.fromarray(image)
            dataImg = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_Grayscale16)

            return QPixmap.fromImage(dataImg)

        else:
            return None

    # def adjust_contrast_brightness(self, matrix, contrast, brightness):
    #     new_matrix = np.clip((matrix - 32768) * contrast + 32768 + brightness * 65535, 0, 65535).astype(np.uint16)
    #     return new_matrix

    def apply_contrast_brightness(self,image , alpha, beta):

        image = ((alpha/100) * image) + beta

        image = FormatMatrix(image)

        return image