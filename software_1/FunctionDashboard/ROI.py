from qtpy.QtGui import QImage, QPixmap, QPainter, QPen, QColor
from qtpy.QtCore import Qt
from software_1.Preprocessing.FormattingMatrix import FormatMatrix

class SliderMRI_ROI():

    def __init__(self,image,valueH, valueV, contrast=65, brightess = 5):

        self.image = self.SliceMRI(image, valueH, valueV, contrast, brightess)

    def SliceMRI(self, image, valueH, valueV, cont, brightess):

        image_pixel_array = self.apply_contrast_brightness(image[valueH][valueV].pixel_array, cont, brightess)

        height, width = image_pixel_array.shape

        dataImg = QImage(image_pixel_array, width, height, QImage.Format_Grayscale16)

        pixmap = QPixmap.fromImage(dataImg)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        if image[valueH][valueV].maskFull is not None:

            Rect_color = QColor(0, 255, 0, 100)
            pen_color = QColor(0, 128, 0)

            painter.setPen(QPen(pen_color, 2, Qt.SolidLine))
            painter.setBrush(Rect_color)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            painter.drawRect(40, 40, 80, 80)
            painter.end()

        else: painter.end()

        return pixmap

    def apply_contrast_brightness(self,image, contrast_factor, brightness_factor):

        enhanced_image = image * (contrast_factor/100) + (brightness_factor*100)

        enhanced_image = FormatMatrix(enhanced_image)

        return enhanced_image

