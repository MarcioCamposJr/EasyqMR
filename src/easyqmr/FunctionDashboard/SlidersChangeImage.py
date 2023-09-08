from qtpy.QtGui import QImage,QPixmap
from easyqmr.Preprocessing.FormattingMatrix import FormatMatrix

class SliderMRI():

    def __init__(self,image,valueH, valueV = None, contrast=65, brightess = 5):

        self.imageV = self.ParameterMRI(image, valueH, valueV, contrast, brightess)
        self.imageH = self.SliceMRI(image,valueH,contrast,valueV, brightess)

    def SliceMRI(self,image,value,cont,valueV, brightess):

        if valueV is not None:
            image = self.apply_contrast_brightness(image[value][0].pixel_array, cont, brightess)
        else:
            image = self.apply_contrast_brightness(image[value].pixel_array, cont, brightess)

        height, width = image.shape

        dataImg = QImage(image, width, height, QImage.Format_Grayscale16)

        return QPixmap.fromImage(dataImg)

    def ParameterMRI(self, image, valueH, valueV, cont, brightess):

        if valueV is not None:
            image = self.apply_contrast_brightness(image[valueH][valueV].pixel_array, cont, brightess)

            height, width = image.shape

            dataImg = QImage(image, width, height, QImage.Format_Grayscale16)

            return QPixmap.fromImage(dataImg)

        else:
            return None

    def apply_contrast_brightness(self,image, contrast_factor, brightness_factor):

        enhanced_image = image * (contrast_factor/100) + (brightness_factor*100)

        enhanced_image = FormatMatrix(enhanced_image)

        return enhanced_image