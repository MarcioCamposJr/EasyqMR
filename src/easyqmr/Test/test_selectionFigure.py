import random, sys
from qtpy.QtCore import QPoint, QRect, QSize, Qt
from qtpy.QtGui import *
from PyQt5.QtWidgets import QLabel,QApplication,QRubberBand

class Window(QLabel):
    def __init__(self, parent = None):
        QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Line, self)
        self.origin = QPoint()

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):

        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()

def create_pixmap():

    def color():
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        return QColor(r, g, b)

    def point():
        return QPoint(random.randrange(0, 400), random.randrange(0, 300))

    pixmap = QPixmap(400, 300)
    pixmap.fill(color())
    painter = QPainter()
    painter.begin(pixmap)
    i = 0
    while i < 1000:
        painter.setBrush(color())
        painter.drawPolygon(QPolygon([point(), point(), point()]))
        i += 1

    painter.end()
    return pixmap


if __name__ == "__main__":

    app = QApplication(sys.argv)
    random.seed()

    window = Window()
    window.setPixmap(create_pixmap())
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec_())