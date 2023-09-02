import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QScrollArea, QApplication
from qtpy.QtGui import QImage, QPainter

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Create the canvas
        self.canvas = QCanvas()

        # Draw a circle on the canvas
        painter = QPainter(self.canvas)
        painter.drawEllipse(0, 0, 100, 100)

        # Convert the canvas to an image
        self.image = QImage.fromData(self.canvas.saveAsData())

        # Create the label
        self.label1 = QLabel()
        self.label1.setText("Label 1")

        # Create the checkbox
        self.checkbox1 = QCheckBox()

        # Add the items to the layout
        self.layout.addWidget(QLabel(self.image))
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.checkbox1)

        # Create the scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self)

        # Add the scroll area to the layout
        self.layout.addWidget(self.scrollArea)

    def show(self):
        super().show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())