import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QColor
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui


class TransparentEllipseItem(pg.GraphicsObject):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen(None))
        p.setBrush(pg.mkColor(255, 0, 0, 100))  # Transparent red color (255, 0, 0) with 100 alpha (opacity)
        p.drawEllipse(self.rect)
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class CustomCircleROI(pg.CircleROI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contextMenuEvent(self, event):
        # Override the contextMenuEvent to disable the default context menu
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transparent Red Circular ROI with PyQtGraph")
        self.setGeometry(100, 100, 800, 600)

        # Create a QLabel and set the pixmap
        self.label = QLabel(self)
        pixmap = QPixmap("C:/Users/marci/OneDrive/Desktop/EasyqMRI/software_1/Docs/Animation/preview.gif")  # Replace with the path to your image
        self.label.setPixmap(pixmap)
        self.label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        # Create a QGraphicsView and add the pixmap to it
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        self.graphics_pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.graphics_pixmap_item)

        # Create the custom circular ROI with CustomCircleROI
        self.roi = CustomCircleROI([100, 100], [100, 100], pen=(255, 0, 0), scaleSnap=True)
        self.roi.setParentItem(self.graphics_pixmap_item)

        # Add the transparent red ellipse to the scene
        ellipse_item = TransparentEllipseItem(self.roi.boundingRect())
        self.scene.addItem(ellipse_item)

        self.show()

    def print_roi_values(self):
        print("Position: ", self.roi.pos())  # ROI position (x, y)
        print("Size: ", self.roi.size())  # ROI size (width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
