from qtpy.QtWidgets import QDialog, QFileDialog, QHeaderView, QCheckBox, QTableWidgetItem, QAbstractItemView
from qtpy.uic import loadUi
from qtpy.QtCore import Qt

from pathlib import Path
import time

from software_1.ImpExpMRI.ProcessingFile.FormattingMRI import FormattedMRI
from software_1.ImpExpMRI.ProcessingFile.ClassificationType import classification
from software_1.ImpExpMRI.ProcessingFile import OrderSlices

from software_1.Alerts.Error import ErrorWarning

from software_1.ImpExpMRI.UIProgressStepOpen import ProgressUI

import nibabel as nib
import pydicom as dicom

import os
class OpenMRI(QDialog):

    def __init__(self):

        super(OpenMRI,self).__init__()

        path = os.path.dirname(os.path.abspath('None'))
        path = os.path.join(path, "qt.ui/OpenMRI.ui")
        loadUi(path,self)

        self.setWindowTitle("OpenMRI")

        # Estrutura inicial da tabela
        self.tableFile.setColumnCount(8)
        self.tableFile.setHorizontalHeaderLabels([''," Classification", "Slice", "Echo Time", "Repetion Time", "Flip Angle", "Inversion Time", "b-value" ])
        self.tableFile.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        #Define tamanho das colunas
        self.tableFile.setColumnWidth(0, 1)
        self.tableFile.setColumnWidth(1, 90)
        self.tableFile.setColumnWidth(2, 70)
        self.tableFile.setColumnWidth(3, 75)
        self.tableFile.setColumnWidth(4, 100)
        self.tableFile.setColumnWidth(5, 75)
        self.tableFile.setColumnWidth(6, 100)
        self.tableFile.setColumnWidth(7, 65)

        # Obtenha os cabeçalhos horizontal e vertical da tabela
        header_horizontal = self.tableFile.horizontalHeader()
        header_vertical = self.tableFile.verticalHeader()

        #Define tamanho das linhas
        self.tableFile.resizeRowsToContents()

        #Tamanho de cabecalho
        header_vertical.setDefaultSectionSize(15)
        header_vertical.setVisible(False)

        #Fixa tamanho de linhas e colunas
        header_vertical.setSectionResizeMode(QHeaderView.Fixed)
        header_horizontal.setSectionResizeMode(QHeaderView.Fixed)

        #Alinha texto de cabecalho para esquerda
        header_horizontal.setDefaultAlignment(Qt.AlignLeft)

        # Desative a seleção nos cabeçalhos
        header_horizontal.setSectionsClickable(False)
        header_vertical.setSectionsClickable(False)
        self.tableFile.setCornerButtonEnabled(False)
        self.tableFile.setSelectionMode(QAbstractItemView.NoSelection)

        # Criar uma QCheckBox para o cabeçalho horizontal
        self.checkbox_horizontal = QCheckBox(header_horizontal)
        self.checkbox_horizontal.setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }""QCheckBox { padding: 0px; margin: 3px;  margin-left:6px }")
        self.tableFile.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.tableFile.setCellWidget(0, 0, self.checkbox_horizontal)

        # Test de stylesheet
        # pathStyleSheet = "C:/Users/marci/OneDrive/Desktop/EasyqMRI/software_1/QSS/StyleSheetTableOpenMRI.qss"
        # with open(pathStyleSheet, "r") as file:
        #     qss_style = file.read()
        # self.tableFile.setStyleSheet(qss_style)

        # Defina uma folha de estilo para os cabeçalhos
        header_style_horizonatal = "::section { background-color: #848484; color: black; font-weight: bold;font-size: 12px;text-align: center;}"
        header_style_vertical = "::section { background-color: rgb(95, 95, 95); text-align: center;}"
        header_style_table = "::section { background-color: rgb(95, 95, 95); font-size: 12px;}"

        # Defina a folha de estilo para os cabeçalhos horizontal e vertical
        header_horizontal.setStyleSheet(header_style_horizonatal)
        header_vertical.setStyleSheet(header_style_vertical)
        self.tableFile.setStyleSheet(header_style_table)

        self.show()

        self.openFolder.clicked.connect(self.OpenFolder)
        self.openFile.clicked.connect(self.OpenFile)

        self.checkbox_horizontal.stateChanged.connect(self.selectAll)

        self.Progress = ProgressUI()

        self.Path = None
        self.MRI = None
        self.MRIMatrix = []
        self.checkbox = []
        self.checkbox_item = []

        self.Close.clicked.connect(self.close)

    def OpenFolder(self):
        filedialog = QFileDialog()
        path = filedialog.getExistingDirectory(self, 'Open Folder','C:/Users/marci/OneDrive/Desktop')

        if path:
            self.Path = Path(path)
            self.ImpAndFormat()

    def OpenFile(self):
        filedialog = QFileDialog()
        self.pathFiles = filedialog.getOpenFileName(self, 'Open File','C:/Users/marci/OneDrive/Desktop')

        if self.pathFiles:
            self.Path = Path(self.pathFiles[0])
            print(self.pathFiles[0])
            self.ImpAndFormat()

    def ImpAndFormat(self):
        self.Progress = ProgressUI()
        self.Progress.show()
        self.test = ErrorWarning()

        self.Progress.updateProgress(10, 'Importing and formatting MRI files...')
        all_files = list(self.Path.glob("*"))

        listItems = []

        if all_files:
            for pathFile in all_files:
                if str(pathFile)[-4:] == ".nii":
                    file_nifti = nib.load(pathFile)
                    listItems = FormattedMRI(file_nifti,'NIfTI')
                    self.MRI = listItems

                if str(pathFile)[-4:] == ".dcm":
                    file_dicom = dicom.read_file(pathFile)
                    listItems.append(FormattedMRI(file_dicom, 'DICOM'))
                    self.MRI = listItems
        else:
            if str(self.Path)[-4:] == ".nii":
                file_nifti = nib.load(self.Path)
                listItems = FormattedMRI(file_nifti, 'NIfTI')
                self.MRI = listItems

            if str(self.Path)[-4:] == ".dcm":
                file_dicom = dicom.read_file(self.Path)
                listItems.append(FormattedMRI(file_dicom, 'DICOM'))
                self.MRI.append(listItems)
        self.CheckItems()

    def CheckItems(self): # todo rever a questao de adicionar mais itens, isto pois aqui esta usando sempre self.MRI
        self.Progress.updateProgress(20, 'Checking similarity of MRI files...')
        ReferName = self.MRI[0].PatientName
        ReferResol = (len(self.MRI[0].pixel_array), len(self.MRI[0].pixel_array[0]))

        i=1
        while i < len(self.MRI):
            if self.MRI[i].PatientName != ReferName:
                i = len(self.MRI) + 1
                self.Progress.close()
                self.Erro = ErrorWarning('The slices do not refer to the same patient.')

            elif (len(self.MRI[i].pixel_array),len(self.MRI[i].pixel_array[0])) != ReferResol:
                i = len(self.MRI) + 1
                self.Progress.close()
                self.Erro = ErrorWarning('The slices do not have the same spatial resolution.')
            else:
                i = i + 1
            if i == len(self.MRI):
                self.SortItens()

    def SortItens(self):
        self.Progress.updateProgress(30, 'Arranging MRI slices...')
        #Organizar fatias em matrix com conjunto de imagens correpondeste a seu parametro e verificacao se nao ha fatias repetidas por comparação de matriz
        SortMatrixMRI, check, index = OrderSlices.CheckSlicesMRI(self.MRI)
        print(check)
        if check:
            errorLabel = 'Selected images have duplicate slice position' + str(SortMatrixMRI[index[0]][index[1]].SliceLocation)
            self.Erro = ErrorWarning(errorLabel)
            self.Progress.close()
        else:
            self.Progress.updateProgress(60, 'Classifying MRI modality...')
            #Classifica a modalidade de imagem de ressonancia
            SortMatrixMRI = classification(SortMatrixMRI)
            #Organiza as fatias de acordo com a ordem correta do parametro associado
            SortMatrixMRI = OrderSlices.sortMRIParameters(SortMatrixMRI)
            self.Progress.updateProgress(80, 'Checking symmetry of MRI slices...')
            #Verifica simetria das fatias em relacao aos parametros
            if OrderSlices.CheckSymmetryParameter(SortMatrixMRI):
                self.MRIMatrix = SortMatrixMRI #todo Preciso rever aqui porque vou add mais de uma vez imagens nesse objeto
                self.listItems(SortMatrixMRI)
            else:
                self.error = ErrorWarning('The selected files do not have symmetry between slices and respective images.')
                self.Progress.close()

    def listItems(self, items):
        self.Progress.updateProgress(95, 'Adding the MRI Slices...')
        List = []

        Classification = []
        Slice = []
        EchoTime = []
        RepetionTime = []
        FlipAngle = []
        InversionTime = []
        bValue = []

        for i in range(len(items)):
            for j in range(len(items[0])):
                Classification.append(str(items[i][j].TypeMRI))
                Slice.append(str(items[i][j].SliceLocation))
                EchoTime.append(str(items[i][j].EchoTime))
                RepetionTime.append(str(items[i][j].RepetitionTime))
                FlipAngle.append(str(items[i][j].FlipAngle))
                InversionTime.append(str(items[i][j].InversionTime))
                bValue.append(str(items[i][j].DiffusionBValue))

        List.append(Classification)
        List.append(Slice)
        List.append(EchoTime)
        List.append(RepetionTime)
        List.append(FlipAngle)
        List.append(InversionTime)
        List.append(bValue)

        self.addItem(List)

    def addItem(self, item):
        #Add texto de diretorio para referenciar ultimo arquivo add
        self.path.setText('   ' + str(self.Path))

        PatientName = self.MRIMatrix[0][0].PatientName
        Resolution = str(len(self.MRIMatrix[0][0].pixel_array[:]) )+ ',' +str( len(self.MRIMatrix[0][0].pixel_array[0][:]))
        LenItens = (len(self.MRIMatrix)*len(self.MRIMatrix[0]))

        self.tableFile.setRowCount(len(item[0]))

        for i in range(len(item[0])):
            self.checkbox.append(QCheckBox())
            self.checkbox[i].setStyleSheet("QCheckBox::indicator { width: 15px; height: 15px; }""QCheckBox { padding: 0px; margin: 1px;  margin-left:6px }")
            self.checkbox_item.append(QTableWidgetItem())
            self.checkbox_item[i].setFlags(self.checkbox_item[i].flags() | 0x0020)  # Definindo a flag como um item selecionável

            self.tableFile.setItem(i, 0, self.checkbox_item[i])
            self.tableFile.setCellWidget(i, 0, self.checkbox[i])
            self.tableFile.setItem(i, 1, QTableWidgetItem(item[0][i]))
            self.tableFile.setItem(i, 2, QTableWidgetItem(item[1][i]))
            self.tableFile.setItem(i, 3, QTableWidgetItem(item[2][i]))
            self.tableFile.setItem(i, 4, QTableWidgetItem(item[3][i]))
            self.tableFile.setItem(i, 5, QTableWidgetItem(item[4][i]))
            self.tableFile.setItem(i, 6, QTableWidgetItem(item[5][i]))
            self.tableFile.setItem(i, 7, QTableWidgetItem(item[6][i]))

        self.Progress.updateProgress(100, 'Done!')
        self.Progress.close()
    def selectAll(self, state):
        if state == 2:  # 2 corresponde ao estado "marcado"
            for i in range(len(self.MRI)):
                self.checkbox[i].setChecked(True)
        else:
            for i in range(len(self.MRI)):
                self.checkbox[i].setChecked(False)



