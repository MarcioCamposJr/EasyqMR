import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class graphParameter():

    def __init__(self, infoMap, x_clicked, y_clicked, size = None, TypeImage = None):

        self.graph = self.mapT2(infoMap, x_clicked, y_clicked, size)

    def mapT2(self, infoMap, x_clicked, y_clicked, size = None):

        echoTime = infoMap[5]
        IntenPixel = infoMap[4][:, int(y_clicked), int(x_clicked)]

        T2 = infoMap[0][int(y_clicked), int(x_clicked)]
        ConsMag = infoMap[1][int(y_clicked), int(x_clicked)]

        b = -1/T2
        x_line = np.linspace(echoTime[0], echoTime[-1], int(echoTime[-1])*50)
        y_line = ConsMag * np.exp(b * x_line)

        fig, ax = plt.subplots(constrained_layout=True, figsize=(4, 2))
        fig.patch.set_facecolor('#252427')
        ax.set_facecolor('#252427')
        ax.scatter(echoTime, IntenPixel, label='Original Data', color=(0.8, 0.6, 0.4) )
        ax.plot(x_line, y_line, label='Curve Fit', color=(0.4, 0.6, 0.8))

        ax.set_xlabel('Echo Time')
        ax.set_ylabel('Intensity')
        ax.legend()

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_tick_params(which='both', size=0)
        ax.yaxis.set_tick_params(which='both', size=0)

        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        canvas = FigureCanvas(fig)

        return canvas

