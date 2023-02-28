import numpy as np


def mappingT2(image):
    # i = 0
    # echoTime = []
    #
    # while i < len(image) - 1:
    #     echoTime.append(float(image[i].EchoTime))
    #     i = i + 1

    echo_times = [float(dcm.EchoTime) for dcm in image]
    image_data = [dcm.pixel_array for dcm in image]
    image_data = np.array(image_data)

    t2_map = np.zeros(image_data.shape[1:])
    # array = []
    #
    # i = 0
    # j = 0
    # k = 0
    # for j in range(image[0].pixel_array.shape[0]):
    #     for k in range(image[0].pixel_array.shape[1]):
    #         pixel = []
    #         while i < len(image) - 1:
    #             pixel.append(image[i].pixel_array[j][k] + 1)
    #             i = i + 1
    #         i = 0
    #         T2 = calc_t2(echoTime, pixel)
    #
    #         mapT2[j][k] = T2
    #
    # return mapT2

    for i in range(image_data.shape[1]):
        for j in range(image_data.shape[2]):
            y = np.log(image_data[:, i, j])
            x = np.array(echo_times)
            fit = np.polyfit(x, y, 1)
            if fit[0] < 0:
                t2_map[i, j] = -1 / fit[0]
            else:
                t2_map[i, j] = 0
    return FormatMatrix(t2_map)*2


def calc_t2(te, signal):
    signal = np.asarray(signal)
    log_signal = np.log(signal)
    slope, intercept = np.polyfit(te, log_signal, 1)
    if slope != 0:
        return -1 / slope
    else:
        return 0

def FormatMatrix(matrix):

    matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))
    matrix = (matrix * (2**16)).astype(np.uint16)

    return matrix