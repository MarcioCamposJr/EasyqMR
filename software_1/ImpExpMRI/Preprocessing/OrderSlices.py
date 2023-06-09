# Identificacao de todas as imagens que contem a mesma posicao de fatia
# Classificacao para descobrir parametro de interesse para passos seguintes
# Verificar se possuim uma mesma matrix a partir do parametro relacionado
# Verificao se todas possuim a mesma quantidade de fatias de mesma posicao, (pegar a que tem mais fatia  e definir como padrao?)
#TODO preciso fazer a verificacao por parametro para que nao haja fatia repetida( fazendo isso pq comparar a matrix inteira parece ser algo mais custoso, ou sera q nao?)
from FilterSlices import SlicesMRI
def OrderMRI(MRI):

    #Organizcao inicial de fatias
    MRI, arrayLenParameterSlice = sort_slices(MRI)

    #Criar a matrix com fatias de mesma posicao
    Slices = SlicesMRI(MRI)
    MRIMatrix = Slices.Matrix

    #Verificao de fatias repetidas #TODO ver se isso esta funcioanndo
    for i in range(len(arrayLenParameterSlice)):
        for j in range(len(arrayLenParameterSlice[i])):
            for k in range(len(arrayLenParameterSlice[i])):
                if MRIMatrix[i][j].pixel_array == MRIMatrix[i][k].pixel_array and j != k:
                #Retirando fatia repetida, importante para adicao de novos diretorios nos itens
                    MRIMatrix[i].remove(MRIMatrix[i][j])

    #TODO verificar se todos possuim o mesmo tamanhao de variacao de parametros

def sort_slices(info):  #SORT SLICES
    if info[0].SliceLocation is not None:

        sequence = []
        order = []
        listInterm = []
        lenParameterList = []

        #ASSIGNING SLICE POSITION VALUES
        for i in range(len(info)):
            sequence.append(info[i].SliceLocation)

        #ARRANGE SLICE SEQUENCE VALUES
        sequence.sort()

        #Matrix com numeros de fatias de mesmo parametro
        for i in range(len(info)):
            if sequence[i + 1] == sequence[i]:
                listInterm.append(sequence[i])
            else:
                listInterm.append(sequence[i])
                lenParameterList.append(listInterm)

        j=0
        k=0
        #ARRANGE DICOM SLICE SEQUENCE
        while k != len(info)-1:

            if sequence[k] == info[j].SliceLocation:
                order.append(info[j])
                k=k+1
            if j == len(info)-1:
                j=0
            j=j+1

        return order, lenParameterListn
    else:
        return info

