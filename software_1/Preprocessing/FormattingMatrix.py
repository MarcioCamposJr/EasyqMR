import numpy as np

def FormatParamMap(matrix):

    max = np.amax(matrix)

    matrix = np.clip(matrix, 0, max-1)

    matrix = (matrix - np.min(matrix)) / ((np.max(matrix) - np.min(matrix)))

    matrix = (matrix * ((2 ** 16)-1))

    matrix = np.round(matrix).astype(np.uint16)

    return matrix

    #Pegar maior intensidade de pixle, normalizar e ajustar para 16 bits

def FormatTo16bits(matrix):

    matrix = (matrix - np.min(matrix)) / ((np.max(matrix) - np.min(matrix)))

    matrix = (matrix * ((2 ** 16)-1))

    matrix = np.round(matrix).astype(np.uint16)

    return matrix

def FormatMatrix(matrix):

    # matrix = np.round(matrix)

    matrix = np.clip(matrix, 0, ((2 ** 16)-1))

    matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

    matrix = (matrix * ((2 ** 16)-1))

    matrix = np.round(matrix).astype(np.uint16)

    # print(np.max(matrix))
    #
    # matrix = matrix - 1
    #
    # matrix = np.clip(matrix, 1, 65000)

    return matrix