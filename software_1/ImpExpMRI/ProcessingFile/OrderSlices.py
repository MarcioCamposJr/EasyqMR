# Identificacao de todas as imagens que contem a mesma posicao de fatia
# Classificacao para descobrir parametro de interesse para passos seguintes
# Verificar se possuim uma mesma matrix a partir do parametro relacionado
# Verificao se todas possuim a mesma quantidade de fatias de mesma posicao, (pegar a que tem mais fatia  e definir como padrao?)
#TODO preciso fazer a verificacao por parametro para que nao haja fatia repetida(fazendo isso pq comparar a matrix inteira parece ser algo mais custoso, ou sera q nao?)
from software_1.ImpExpMRI.ProcessingFile.FilterSlices import SlicesMRI
import numpy as np

def CheckSlicesMRI(MRI):

    #Organizcao inicial de fatias
    MRI = sort_slices(MRI)

    Slices = SlicesMRI(MRI)
    MRIMatrix = Slices.Matrix

    #Verificao de fatias repetidas #TODO ver se isso esta funcioanndo
    for i in range(len(MRIMatrix)):
        for j in range(len(MRIMatrix[i])):
            for k in range(len(MRIMatrix[i])):
                if np.array_equal(np.array(MRIMatrix[i][j].pixel_array), np.array(MRIMatrix[i][k].pixel_array)) and j != k:
                #Retirando fatia repetida, importante para adicao de novos diretorios nos itens
                    #MRIMatrix[i].remove(MRIMatrix[i][j])
                    #todo fazer aviso pq coloquei pra remover e parece que nao havia uma imagem a mais, mas sim havia uma imagem duplicada para manter a simetria(tenho que verificar se foi isso mesmo)
                    break

    return MRIMatrix

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
def sortMRIParameters(MRISlices):
    #TODO Verificar se a proxima entrada de arquivos eh do mesmo tipo

    ParameterInter = []
    MRISlicesSort = []

    typeMRI = MRISlices[0][0].TypeMRI

    for i in range(len(MRISlices)):
        for j in range(len(MRISlices[i])):
            if typeMRI == 'T1':
                ParameterInter.append(MRISlices[i][j].RepetitionTime)

            if typeMRI == 'T2':
                ParameterInter.append(MRISlices[i][j].EchoTime)

            if typeMRI == 'T1p':
                ParameterInter.append(MRISlices[i][j].InversionTime)

            if typeMRI == 'T2*':
                ParameterInter.append(MRISlices[i][j].EchoTime)

            if typeMRI == 'IVIM':
                ParameterInter.append(MRISlices[i][j].DiffusionBValue)

        ParameterInter.sort()

        j = 0
        count = 0

        while(len(MRISlices[i]) != count):
        #TODO orhganizar as fatias na ordem
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

    return MRISlicesSort

def CheckSymmetryParameter(MRI):

    LenSlices = []

    for i in range(len(MRI)-1):
        if len(MRI[i]) != len(MRI[i+1]):
            #TODO Funcao aviso
            break
    else:
        return True













