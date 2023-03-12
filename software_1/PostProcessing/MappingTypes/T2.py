import numpy as np
import cv2

def mappingT2(image):

    echo_times = [float(dcm.EchoTime) for dcm in image]
    data = [dcm.pixel_array for dcm in image]
    data = np.array(data)

    # data = cv2.normalize(data, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    image_data = []

    # for i in range(len(data)):
    #     image_data.append(cv2.bilateralFilter(data[i], d=5, sigmaColor=10, sigmaSpace=10))
    #
    # image_data = cv2.normalize(np.array(image_data), None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    t2_map = np.zeros(data.shape[1:])
    consMag = np.zeros(data.shape[1:])

    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            # if np.any(image_data[:, i, j] > 20):
                y = np.log(data[:, i, j] + 1)
                x = np.array(echo_times)
                fit = np.polyfit(x, y, 1)
                if fit[0] < 0:
                    t2_map[i, j] = -1 / fit[0]

                else:
                    t2_map[i, j] = 0
                consMag[i, j] = np.exp(fit[1])
            # else:
            #     t2_map[i, j] = 0

    return t2_map,consMag

def FormatMatrix(matrix):
    matrix = (matrix - np.amin(matrix)) / (np.amax(matrix) - np.amin(matrix))
    matrix = (matrix * (2**16)).astype(np.uint16)

    matrix = ((2 ** 16) / np.amax(matrix)) * matrix

    return matrix