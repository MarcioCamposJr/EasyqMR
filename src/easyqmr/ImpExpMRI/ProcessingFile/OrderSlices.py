#TODO preciso fazer a verificacao por parametro para que nao haja fatia repetida(fazendo isso pq comparar a matrix inteira parece ser algo mais custoso, ou sera q nao?)
from easyqmr.ImpExpMRI.ProcessingFile.FilterSlices import SlicesMRI

import numpy as np

def CheckSlicesMRI(MRI):

    #Organizcao inicial de fatias
    MRI = sort_slices(MRI)

    for i in range(len(MRI)):
        for j in range(len(MRI)):
            #todo rever a questao destas fatias problematicas
            if np.array_equal(MRI[i].pixel_array, MRI[j].pixel_array) and i != j and j!=124 and j != 120:
                return MRI, True, (i,j)
                break

    return MRI, False, None

def sort_slices(info):  #SORT DICOM SLICES
    if info[0].SliceLocation is not None:
        k = 0
        sequence = []
        order = []
        #ASSIGNING SLICE POSITION VALUES
        for i in range(len(info)):
            sequence.append(info[i].SliceLocation)

        #ARRANGE SLICE SEQUENCE VALUES
        sequence.sort()
        j=0

        #ARRANGE DICOM SLICE SEQUENCE
        while k != len(info):

            if sequence[k] == info[j].SliceLocation:
                order.append(info[j])
                k=k+1
            if j == len(info)-1:
                j=0
            j=j+1
        return order
    else:
        return info
def sortMRIParameters(MRISlices, typeMRI):
    #TODO Verificar se a proxima entrada de arquivos eh do mesmo tipo

    MRISlicesSort = []

    for i in range(len(MRISlices)):
        ParameterInter = []
        for j in range(len(MRISlices[i])):
            if typeMRI == 'T1':
                ParameterInter.append(MRISlices[i][j].RepetitionTime)

            elif typeMRI == 'T2':
                ParameterInter.append(MRISlices[i][j].EchoTime)

            elif typeMRI == 'T1p':
                ParameterInter.append(MRISlices[i][j].InversionTime)

            elif typeMRI == 'T2*':
                ParameterInter.append(MRISlices[i][j].EchoTime)

            elif typeMRI == 'IVIM':
                ParameterInter.append(MRISlices[i][j].DiffusionBValue)

        ParameterInter.sort()

        j = 0
        count = 0
        while(len(MRISlices[i]) != count):

            if typeMRI == 'T1' and MRISlices[i][j].RepetitionTime == ParameterInter[count]:
                MRISlicesSort.append(MRISlices[i][j])
                count = count + 1

            elif typeMRI == 'T2' and MRISlices[i][j].EchoTime == ParameterInter[count]:
                MRISlicesSort.append(MRISlices[i][j])
                count = count + 1

            elif typeMRI == 'T1p' and MRISlices[i][j].InversionTime == ParameterInter[count]:
                MRISlicesSort.append(MRISlices[i][j])
                count = count + 1

            elif typeMRI == 'T2*' and MRISlices[i][j].EchoTime == ParameterInter[count]:
                MRISlicesSort.append(MRISlices[i][j])
                count = count + 1

            elif typeMRI == 'IVIM' and MRISlices[i][j].DiffusionBValue == ParameterInter[count]:
                MRISlicesSort.append(MRISlices[i][j])
                count = count + 1

            if j < count:
                j = j + 1
            else:
                j = 0

    MRISlicesSort = SlicesMRI(MRISlicesSort)
    MRISlicesSort = MRISlicesSort.Matrix
    return MRISlicesSort

def CheckSymmetryParameter(MRI):

    for i in range((len(MRI)-1)):
        if len(MRI[i]) != len(MRI[i+1]):
            return False
    else:
        return True













