import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from .ImpExpMRI.Preview import Preview
from .ImpExpMRI import OpenMRI
from .ImpExpMRI.ExportMap import ExportMapForamt

from .Alerts.Error.ErrorWarning import ErrorWarning
from .Alerts.About import WindowAbout

from .Preprocessing.BrainExtraction import BET
from .Preprocessing.MRIcoregistration import register_slices

from .FunctionDashboard.SlidersChangeImage import SliderMRI
from .FunctionDashboard.ParameterGraphAnalysis import graphParameter
from .FunctionDashboard.MaskSelection import Mask
from .FunctionDashboard.ROI import SliderMRI_ROI

from qtpy.QtWidgets import QMainWindow, QApplication, QStackedWidget, QSizePolicy,QVBoxLayout, QWidget, QFileDialog
from qtpy.uic import loadUi
from qtpy.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QPixmapCache
from qtpy.QtCore import Qt, QPoint, QTimer, QRect

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import os
import sys
import numpy as np
import nibabel as nib

class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()

        self.MatrixMRI = None
        self.ImageMRI = [0, 1, 3]
        self.slider = None

        self.infoMapping = None

        self.modalityMRI = None

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "src/easyqmr/qt.ui/main.ui")
        loadUi(path, self)

        self.openMRI.triggered.connect(self.OpenMRI)
        self.spinBoxSlicer.valueChanged.connect(self.connectSpinBoxSlicer)
        self.SyncCheckBox.clicked.connect(self.syncSlider)
        self.horizontalSlider.valueChanged.connect(self.UpdatePixmap)
        self.verticalSlider.valueChanged.connect(self.UpdatePixmap)
        self.Brightness.valueChanged.connect(self.UpdatePixmap)
        self.Contrast.valueChanged.connect(self.UpdatePixmap)
        self.bet.clicked.connect(self.Bet)
        self.co_registration.clicked.connect(self.Co_registration)
        self.ParametricMap.clicked.connect(self.generateMap)
        self.errorMap.clicked.connect(self.setErrorMap)
        self.woROI.clicked.connect(self.UpdatePixmap)
        self.wROI.clicked.connect(self.UpdatePixmap)
        self.setMouseTracking(True)
        self.AnalyzeGraph.clicked.connect(lambda: self.CondExistMouPreEve('AG'))
        self.RectROI.clicked.connect(lambda: self.CondExistMouPreEve('RR'))
        self.ElliROI.clicked.connect(lambda: self.CondExistMouPreEve('ER'))
        self.FreeHandsROI.clicked.connect(lambda: self.CondExistMouPreEve('FHR'))
        self.FullROI.clicked.connect(lambda: self.CondExistMouPreEve('FR'))
        self.FullVolumeROI.clicked.connect(self.SelectFullVolumeROI)
        # self.rectROI.pressed.connect(lambda: self.withdrawnROI('RR'))
        # self.elliROI.pressed.connect(lambda: self.withdrawnROI('ER'))
        # self.FreeHandsROI.pressed.connect(lambda: self.withdrawnROI('FHR'))
        self.FullROI.released.connect(self.SelectFullROI)
        self.FullVolumeROI.released.connect(self.SelectFullVolumeROI)
        self.horizontalSliderMap.valueChanged.connect(self.UpdatePixmapMap)
        self.minMap.valueChanged.connect(self.UpdatePixmapMapBoundaries)
        self.maxMap.valueChanged.connect(self.UpdatePixmapMapBoundaries)
        self.savePNGFormat.triggered.connect(lambda: self.ExportMap('PNG'))
        self.saveNIfTIFormat.triggered.connect(lambda: self.ExportMap('NIfTI'))
        self.actionAbout.triggered.connect(self.AboutUS)
    def OpenMRI(self):
        self.OpenMri = OpenMRI.OpenMRI(self)
        self.OpenMri.open.clicked.connect(self.reviewMRIData)

    def reviewMRIData(self):

        self.MatrixMRI = self.OpenMri.MRIMatrixDone

        Slice = True
        i = 0

        while Slice:
            j = 0
            process = True

            while process:
                if np.array_equal(self.MatrixMRI[i][j].pixel_array, 0):
                    self.MatrixMRI[i].remove(self.MatrixMRI[i][j])

                else:
                    j = j + 1

                if j == len(self.MatrixMRI[i]):
                    process = False

                if len(self.MatrixMRI[i]) == 0:
                    self.MatrixMRI.remove(self.MatrixMRI[i])
                    i = i - 1

            i = i + 1

            if i == len(self.MatrixMRI):
                Slice = False


        self.modalityMRI = self.OpenMri.modality

        self.Preview()

    def Preview(self):

        self.OpenMri.close()
        self.preview = Preview.PreviewGUI(self.MatrixMRI, self)
        self.preview.Open.clicked.connect(self.InitImage)

    def InitImage(self):
        self.preview.close()

        self.horizontalSlider.setValue(0)
        self.verticalSlider.setValue(0)

        self.spinBoxSlicer.setValue(1)

        self.spinBoxSlicer.setMinimum(1)
        self.spinBoxSlicer.setMaximum(len(self.MatrixMRI[:]))
        self.horizontalSlider.setMaximum(len(self.MatrixMRI[:]) - 1)

        self.Contrast.setRange(-100, 300)

        self.Contrast.setValue(100)

        valueH = self.horizontalSlider.value()
        valueV = self.verticalSlider.value()

        self.spinBoxSlicer.setValue(valueH)

        self.verticalSlider.setMaximum(len(self.MatrixMRI[valueH][:]) - 1)

        bright = self.Brightness.value()
        contrast = self.Contrast.value()

        self.slider = SliderMRI(self.MatrixMRI,valueH, valueV, brightess=bright, contrast=contrast)

        self.scaledimage = self.slider.imageV.scaled(self.mainImage.size(), Qt.KeepAspectRatio)
        self.mainImage.setPixmap(self.scaledimage)

        self.FullVolumeROI.setChecked(True)
        self.SetROI()

        self.wROI.setChecked(True)

    def connectSpinBoxSlicer(self):
        if self.MatrixMRI is not None:
            value = self.spinBoxSlicer.value()
            self.horizontalSlider.setValue(value - 1)
        else:
            self.spinBoxSlicer.setValue(0)

    def UpdatePixmap(self):
        if self.MatrixMRI is not None:

            self.SyncCheckBox.setChecked(False)

            valueH = self.horizontalSlider.value()
            valueV = self.verticalSlider.value()

            self.spinBoxSlicer.setValue(valueH + 1)

            bright = self.Brightness.value()
            contrast = self.Contrast.value()

            self.slider = SliderMRI(self.MatrixMRI, valueH, valueV, brightess=bright, contrast=contrast)

            self.scaledimage = self.slider.imageV.scaled(self.mainImage.size(), Qt.KeepAspectRatio)

            self.mainImage.setPixmap(self.scaledimage)

            if self.MatrixMRI[valueH][valueV].fullMask is None and self.MatrixMRI[valueH][valueV].mask is None:

                self.RectROI.setChecked(False)
                self.ElliROI.setChecked(False)
                self.FreeHandsROI.setChecked(False)
                self.FullROI.setChecked(False)

            if self.wROI.isChecked():

                self.SetROI()

        else: self.woROI.setChecked(True)

    def CondExistMouPreEve(self, state):

        if self.infoMapping is None:

            self.AnalyzeGraph.setChecked(False)

        if self.MatrixMRI is None:

            self.RectROI.setChecked(False)
            self.ElliROI.setChecked(False)
            self.FreeHandsROI.setChecked(False)
            self.FullROI.setChecked(False)
            self.FullVolumeROI.setChecked(False)

        if self.AnalyzeGraph.isChecked() and state == 'AG':

            self.RectROI.setChecked(False)
            self.ElliROI.setChecked(False)
            self.FreeHandsROI.setChecked(False)
            self.FullROI.setChecked(False)
            self.FullVolumeROI.setChecked(False)

        elif self.RectROI.isChecked() and state == 'RR':

            self.AnalyzeGraph.setChecked(False)
            self.ElliROI.setChecked(False)
            self.FreeHandsROI.setChecked(False)
            self.FullROI.setChecked(False)
            self.FullVolumeROI.setChecked(False)

            self.wROI.setChecked(True)

        elif self.ElliROI.isChecked() and state == 'ER':

            self.RectROI.setChecked(False)
            self.AnalyzeGraph.setChecked(False)
            self.FreeHandsROI.setChecked(False)
            self.FullROI.setChecked(False)
            self.FullVolumeROI.setChecked(False)

            self.wROI.setChecked(True)
            self.position = []

        elif self.FreeHandsROI.isChecked() and state == 'FHR':

            self.RectROI.setChecked(False)
            self.ElliROI.setChecked(False)
            self.AnalyzeGraph.setChecked(False)
            self.FullROI.setChecked(False)
            self.FullVolumeROI.setChecked(False)

            self.wROI.setChecked(True)

        elif self.FullROI.isChecked() and state == 'FR':

            self.RectROI.setChecked(False)
            self.ElliROI.setChecked(False)
            self.FreeHandsROI.setChecked(False)
            self.AnalyzeGraph.setChecked(False)

            self.wROI.setChecked(True)

            self.SelectFullROI()

    def mouseMoveEvent(self, event):

        if self.MatrixMRI is not None:
            mousePos = self.mapFromGlobal(event.globalPos())

            pixmap_pos = mousePos - (self.mainImage.mapToGlobal(QPoint(0, 0)) + self.mainImage.pixmap().rect().topLeft() - self.mapToGlobal(QPoint(0, 0)))

            if pixmap_pos.x() > 0 and pixmap_pos.y() > 0 and pixmap_pos.x() < self.mainImage.size().width() and pixmap_pos.y() < self.mainImage.size().height():
                widthRescaling = int(pixmap_pos.x() * np.array(self.MatrixMRI[0][0].pixel_array).shape[0] / self.mainImage.size().width())
                heightRescaling = int(pixmap_pos.y() * np.array(self.MatrixMRI[0][0].pixel_array).shape[1] / self.mainImage.size().height())

                self.showxcoor.setText("x =" + str(widthRescaling))
                self.showycoor.setText("y =" + str(heightRescaling))

                valueHS = self.horizontalSlider.value()
                valueVS = self.verticalSlider.value()

                self.intensity.setText("Intensity =" + str(self.MatrixMRI[valueHS][valueVS].pixel_array[heightRescaling][widthRescaling]))

            if self.ElliROI.isChecked():

                self.position.append([pixmap_pos.x(),pixmap_pos.y() ])

                if len(self.position)>3:
                    pass
                    # self.SelectElliROI(self.position)


    # TODO problema com selecao de regiao com forma
    # def SelectElliROI(self, position):
    #
    #     if self.MatrixMRI is not None:
    #         painter = QPainter(self.mainImage.pixmap())
    #         painter.setRenderHint(QPainter.Antialiasing)
    #
    #         ellipse_color = QColor(255, 0, 0, 100)  # Vermelho com transparência de 100
    #         pen_color = QColor(0, 0, 0)  # Preto
    #
    #         painter.setPen(QPen(pen_color, 2, Qt.SolidLine))
    #         painter.setBrush(ellipse_color)
    #         painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
    #
    #         width = int(position[-1][0] - position[0][0])
    #         height = int(position[-1][1] - position[0][1])
    #
    #         x = int(position[0][0])
    #         y = int(position[0][1])
    #
    #         if len(position) > 5:
    #
    #             width_e = int(position[-2][0] - position[0][0])
    #             height_e = int(position[-2][1] - position[0][1])
    #
    #             painter.eraseRect(x, y, width_e, height_e)
    #
    #         painter.drawEllipse(x, y, width, height)
    #         painter.end()
    #
    #         self.mainImage.update()

    def SelectFullROI(self):

        if self.MatrixMRI is not None:

            valueH = self.horizontalSlider.value()

            if self.FullROI.isChecked():

                if self.MatrixMRI[valueH][0].fullMask is None:

                    n = len(self.MatrixMRI[valueH][0].pixel_array)

                    for i in range(len(self.MatrixMRI[valueH])):

                        self.MatrixMRI[valueH][i].fullMask = np.ones((n, n), dtype=bool)

                        self.MatrixMRI[valueH][i].fullROI = True

                if all(obj[0].fullROI for obj in self.MatrixMRI):

                    self.FullVolumeROI.setChecked(True)

            else:

                for i in range(len(self.MatrixMRI[valueH])):
                    self.MatrixMRI[valueH][i].fullMask = None

                    self.MatrixMRI[valueH][i].fullROI = False

                self.FullVolumeROI.setChecked(False)

            self.UpdatePixmap()

    def SelectFullVolumeROI(self):

        if self.MatrixMRI is not None:

            if self.FullVolumeROI.isChecked():

                n = len(self.MatrixMRI[0][0].pixel_array)

                for j in range(len(self.MatrixMRI)):
                    for i in range(len(self.MatrixMRI[j])):

                        self.MatrixMRI[j][i].fullMask = np.ones((n, n), dtype=bool)

                        self.MatrixMRI[j][i].fullROI = True

                self.wROI.setChecked(True)

                self.RectROI.setChecked(False)
                self.ElliROI.setChecked(False)
                self.FreeHandsROI.setChecked(False)

            else:

                for j in range(len(self.MatrixMRI)):
                    for i in range(len(self.MatrixMRI[j])):
                        self.MatrixMRI[j][i].fullMask = None

                        self.MatrixMRI[j][i].fullROI = False

            self.UpdatePixmap()

    def SetROI(self):

        valueH = self.horizontalSlider.value()
        valueV = self.verticalSlider.value()

        if self.MatrixMRI[valueH][valueV].fullROI:

            self.FullROI.setChecked(True)

            painter = QPainter(self.mainImage.pixmap())
            painter.setRenderHint(QPainter.Antialiasing)

            Rect_color = QColor(191, 76, 38, 50)
            pen_color = QColor(191, 76, 38)

            painter.setPen(QPen(pen_color, 4, Qt.DashLine))
            painter.setBrush(Rect_color)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            width = self.mainImage.pixmap().size().width()
            height = self.mainImage.pixmap().size().height()

            painter.drawRect(0, 0, width, height)
            painter.end()

            self.mainImage.update()

    def mousePressEvent(self, event):

        if self.MatrixMRI is not None:
            mousePos = self.mapFromGlobal(event.globalPos())

            pixmap_pos = mousePos - (self.mainImage.mapToGlobal(
                QPoint(0, 0)) + self.mainImage.pixmap().rect().topLeft() - self.mapToGlobal(QPoint(0, 0)))

            if pixmap_pos.x() > 0 and pixmap_pos.y() > 0 and pixmap_pos.x() < self.mainImage.size().width() and pixmap_pos.y() < self.mainImage.size().height():
                widthRescaling = int(pixmap_pos.x() * np.array(self.MatrixMRI[0][0].pixel_array).shape[0] / self.mainImage.size().width())
                heightRescaling = int(pixmap_pos.y() * np.array(self.MatrixMRI[0][0].pixel_array).shape[1] / self.mainImage.size().height())

                self.showxcoor.setText("x =" + str(widthRescaling))
                self.showycoor.setText("y =" + str(heightRescaling))

                valueHS = self.horizontalSlider.value()
                valueVS = self.verticalSlider.value()

                self.intensity.setText(
                    "Intensity =" + str(self.MatrixMRI[valueHS][valueVS].pixel_array[heightRescaling][widthRescaling]))

    def Bet(self):
        if self.MatrixMRI is not None:
            self.brain = BET(self.MatrixMRI)
            self.MatrixMRI = self.brain.MRI
            self.UpdatePixmap()

    def Co_registration(self):
        if self.ImageMRI is not None:
            if len(self.ImageMRI) != len(self.MatrixMRI[:]):
                self.MatrixMRI = register_slices(self.MatrixMRI)
                self.ChangeSlider()

    def generateMap(self):

        if self.MatrixMRI is not None:
            from PostProcessing.CheckMRItoMap import MRItoMap

            self.MRItoMap = MRItoMap(self.MatrixMRI)

            if len(self.MRItoMap) == 0:
                self.alertNoSlice = ErrorWarning('Add at least one slice with region of interest to generate a parametric map.')
            else:
                from PostProcessing.InitParMapGeneration import InitGeneration

                self.infoMapping = InitGeneration(self.MRItoMap, self.modalityMRI)

                if len(self.infoMapping.infomap) != 0:
                    self.setParameterMap()

    def setParameterMap(self):

        self.menuExportMap.setEnabled(True)

        self.popup_timer = QTimer(self)
        self.popup_timer.timeout.connect(self.close_popupGraph)

        self.horizontalSliderMap.setValue(0)
        self.horizontalSliderMap.setMaximum(len(self.infoMapping.infomap) - 1)

        image = self.infoMapping.infomap[0][0]

        self.figure, self.ax = plt.subplots(constrained_layout=True)
        self.figure.patch.set_facecolor('#252427')

        self.imMap = self.ax.imshow(image, cmap='hot', aspect='auto', clim=(self.infoMapping.Boundaries[0]))
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.axis('off')
        self.figure.set_frameon(False)

        self.cbar = self.figure.colorbar(self.imMap, ax=self.ax, pad = 0.02)
        self.cbar.ax.yaxis.set_tick_params(color='white')
        self.cbar.set_label('Relaxation Time (ms)', color='white')
        self.cbar.ax.tick_params(axis='y', which='both', length=0)
        self.cbar.ax.yaxis.set_major_locator(MultipleLocator(base=10))  # Definir passo dos marcadores como 10

        # Definir cor das etiquetas dos marcadores como branco
        for t in self.cbar.ax.get_yticklabels():
            t.set_color('white')

        self.canvas = FigureCanvas(self.figure)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(52)
        size_policy.setVerticalStretch(38)

        self.canvas.setSizePolicy(size_policy)

        self.widgetMap.layout().replaceWidget(self.mapping, self.canvas)
        self.canvas.draw()

        self.canvas.mpl_connect("button_press_event", self.on_canvas_click)

        self.maxMap.setValue(self.infoMapping.Boundaries[0][1])
        self.minMap.setValue(self.infoMapping.Boundaries[0][0])

    def UpdatePixmapMap(self, min = None, max = None):

        if self.infoMapping is not None and not self.errorMap.isChecked():

            if min is None or max is None:

                value = self.horizontalSliderMap.value()

                self.maxMap.setValue(self.infoMapping.Boundaries[value][1])
                self.minMap.setValue(self.infoMapping.Boundaries[value][0])

            else:
                self.maxMap.setValue(max)
                self.minMap.setValue(min)

                self.UpdatePixmapMapBoundaries()


        elif self.errorMap.isChecked():
            self.setErrorMap()

        if self.SyncCheckBox.isChecked():
            self.syncSlider()


    def UpdatePixmapMapBoundaries(self):
        if self.infoMapping is not None:

            self.errorMap.setChecked(False)

            minValue, maxValue = self.minMap.value(), self.maxMap.value()

            value = self.horizontalSliderMap.value()

            image = self.infoMapping.infomap[value][0]
            self.imMap.set_data(image)
            self.imMap.set_clim(minValue, maxValue)
            self.imMap.set_cmap('hot')
            self.cbar.set_label('Relaxation Time (ms)', color='white')
            self.canvas.draw()

    def syncSlider(self):
        if self.infoMapping is not None and self.SyncCheckBox.isChecked():

            value = self.horizontalSliderMap.value()

            SliceLocation = self.infoMapping.infomap[value][3]

            i=0
            loop = True
            while loop:
                if self.MatrixMRI[i][0].SliceLocation == SliceLocation:
                    loop = False
                else:
                    i = i + 1

            self.horizontalSlider.setValue(i)

            self.SyncCheckBox.setChecked(True)

        else:
            self.SyncCheckBox.setChecked(False)

    def setErrorMap(self):

        if self.infoMapping is not None:
            if self.errorMap.isChecked():
                self.SyncCheckBox.setChecked(True)

                value = self.horizontalSliderMap.value()

                errorMap = self.infoMapping.infomap[value][2]

                self.cbar.set_label('Fitting Error', color='white')

                self.imMap.set_data(errorMap)
                self.imMap.set_cmap('viridis')
                self.imMap.set_clim(0, 1)

                self.canvas.draw()

            else:
                min, max = self.minMap.value(), self.maxMap.value()
                self.UpdatePixmapMap(min, max)

        else:
            self.errorMap.setChecked(False)

    def on_canvas_click(self, event):
        if event.inaxes == self.ax:
            x_clicked = event.xdata
            y_clicked = event.ydata

            if x_clicked is not None and y_clicked is not None:
                self.showxcoorMap.setText("x =" + str(int(x_clicked)))
                self.showycoorMap.setText("y =" + str(int(y_clicked)))

                value = self.horizontalSliderMap.value()

                self.intensityMap.setText("Intensity = " + f"{self.infoMapping.infomap[value][0][int(y_clicked)][int(x_clicked)]:.2f}")

                if self.AnalyzeGraph.isChecked():

                    self.show_popupGraph(x_clicked,y_clicked , value)

    def show_popupGraph(self, x_clicked, y_clicked, value):
        popup_widget = QWidget(self, Qt.Popup | Qt.FramelessWindowHint)

        layout = QVBoxLayout()

        layout.setContentsMargins(2, 2, 2, 2)

        graph = graphParameter(self.infoMapping.infomap[value], x_clicked, y_clicked).graph

        layout.addWidget(graph)

        popup_widget.setStyleSheet("background-color: #252427; border: 2px solid rgba(128, 128, 128, 0.5);")

        popup_widget.setLayout(layout)
        popup_widget.move(self.canvas.mapToGlobal(QPoint(int(x_clicked - popup_widget.size().width()*3.2), int(y_clicked + popup_widget.size().height()*1.8))))
        popup_widget.show()

        self.popup_timer.start(2000)  # Tempo em milissegundos para exibir o popup
        self.current_popup = popup_widget


    def close_popupGraph(self):
        if self.current_popup:
            self.current_popup.close()
            self.popup_timer.stop()

    def ExportMap(self, typeFormat):
        filedialog = QFileDialog()
        path_ = os.path.dirname(os.path.abspath('None'))
        path = filedialog.getExistingDirectory(self, 'Select Folder', path_)

        PatientName = self.MatrixMRI[0][0].PatientName.family_name

        if typeFormat == 'PNG':
            for i in range(len(self.infoMapping.infomap)):

                image = self.infoMapping.infomap[i][0]
                self.imMap.set_data(image)
                self.imMap.set_clim(self.infoMapping.Boundaries[i])
                self.imMap.set_cmap('hot')
                self.cbar.set_label('Relaxation Time (ms)', color='white')

                self.figure.savefig(path + '/' + PatientName + "_" + self.modalityMRI + "_" + str(self.infoMapping.infomap[i][3])[:5] + '.png',bbox_inches='tight', transparent=True)


        if typeFormat == "NIfTI":
            mapImage = []
            for i in range(len(self.infoMapping.infomap)):

                mapImage.append(self.infoMapping.infomap[i][0])

            nifti_header = nib.Nifti1Header()
            nifti_header.set_xyzt_units('mm', 'msec')  # Unidades espaciais e temporais

            custom_info = f"Patient Name: {PatientName}, Modality: {self.modalityMRI}"
            nifti_header['descrip'] = custom_info.encode('utf-8')

            nifti_image = nib.Nifti1Image(np.array(mapImage), affine=np.eye(4), header=nifti_header)

            output_filename = f"{PatientName}_{self.modalityMRI}.nii.gz"
            nib.save(nifti_image, path +"/"+output_filename)

    def AboutUS(self):
        WindowAbout(self)

    def closeEvent(self, event):
        # Este slot será chamado quando a janela for fechada
        # Encerra o programa
        app.quit()

def main():
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    sizeScreen = screen.availableGeometry()

    mainwindow = MainWindow()
    widget = QStackedWidget()
    widget.addWidget(mainwindow)

    widget.setWindowTitle("EasyqMR")

    policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    policy.setHeightForWidth(True)
    widget.setSizePolicy(policy)

    widget.setMinimumWidth(int(sizeScreen.width()*(2/3)))
    widget.setMinimumHeight(int(sizeScreen.height()*(2/3)))

    widget.showMaximized()

    widget.show()

    app.exec_()
    sys.exit(app.exec_())
