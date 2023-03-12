import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap

class graphParameter():

    def __init__(self, MRIData, map, pixelWidht, pixelHeight, TypeImage = None):

        self.graph = self.mapT2(MRIData, map, pixelWidht, pixelHeight)

    def mapT2(self,MRIData, map, pixelWidht, pixelHeight):

        echoTime = [float(dcm.EchoTime) for dcm in MRIData]
        IntenPixel = [dcm.pixel_array[pixelWidht][pixelHeight] for dcm in MRIData]

        T2 = map[0][pixelWidht, pixelHeight]
        ConsMag = map[1][pixelWidht, pixelHeight]

        b = -1/T2

        x_line = np.linspace(echoTime[0], echoTime[len(echoTime)-1], int(echoTime[len(echoTime)-1])*50)
        y_line = ConsMag * np.exp(b * x_line)

        fig, ax = plt.subplots()
        ax.scatter(echoTime, IntenPixel)
        ax.plot(x_line, y_line)

        canvas = FigureCanvas(fig)

        pixmap = QPixmap(canvas.size())
        canvas.render(pixmap)

        return pixmap

