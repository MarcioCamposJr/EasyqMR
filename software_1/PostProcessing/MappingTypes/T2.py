import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import time

def mappingT2(image):
    """
    Calculate T2 map, constant magnitude map, offset map, and error map from input images.

    Parameters:
        image (list): List of DICOM images.

    Returns:
        list: [t2_map, consMag, offset, errorMap]
    """
    start_time = time.time()

    echo_times = [float(dcm.EchoTime) for dcm in image]
    data = [dcm.pixel_array for dcm in image]
    data = np.array(data)

    x = np.array(echo_times)

    t2_map = np.zeros(data.shape[1:])
    consMag = np.zeros(data.shape[1:])
    offset = np.zeros(data.shape[1:])
    errorMap = np.zeros(data.shape[1:])

    mean = meanThreshold(data, 5000)

    initial_guess = [mean, 0]
    fit = []

    for j in range(data.shape[1]):
        for i in range(data.shape[2]):
            print(i, j)
            if image[0].fullMask[i][j]:
                if data[0, i, j] > 5000:
                #     try:
                #         params, _ = curve_fit(exponential_func, x, data[:, i, j], p0=initial_guess)
                #
                #         a, b = params
                #         initial_guess = [a, b]
                #
                #     except RuntimeError as e:
                #
                #         try:
                #
                #             initial_guess = [mean, 0]
                #
                #             params, _ = curve_fit(exponential_func, x, data[:, i, j], p0=initial_guess)
                #
                #             a, b = params
                #             initial_guess = [a, b]
                #
                #         except RuntimeError as e:
                #
                #             a, b = 0, 0
                #
                #             initial_guess = [mean, 0]
                #
                #     if initial_guess == [0, 0]:
                #
                #         initial_guess = [mean, 0]
                #
                #         params, _ = curve_fit(exponential_func, x, data[:, i, j], p0=initial_guess)
                #
                #         a, b = params
                #         initial_guess = [a, b]
                #
                #
                # else:
                #     a, b = 0, 0
                #
                # if b > 0:
                #     t2_map[i][j] = 1 / b
                # else:
                #     t2_map[i][j] = 0
                #
                # consMag[i][j] = a
                # offset[i][j] = c

                    try:
                        y = np.log(data[:, i, j] + 1)
                        x = np.array(echo_times)
                        fit = np.polyfit(x, y, 1)

                    except RuntimeError as e:

                        t2_map[i, j] = 0
                        consMag[i, j] = 0

                else:

                    fit = [0, 0]
                    consMag[i, j] = 0

                if fit[0] < 0:
                    t2_map[i, j] = -1 / fit[0]

                else:
                    t2_map[i, j] = 0

                consMag[i, j] = np.exp(fit[1])

            # y_pred = exponential_func(x, a, b, c)
            # errorMap[i][j] = r2_score(data[:, i, j], y_pred)
    end_time = time.time()

    # Calcula a duração da execução
    duration = end_time - start_time
    print(f'Duração da execução: {duration:.6f} segundos')

    return [t2_map, consMag ]
# return [t2_map, consMag]

def exponential_func(x, a, b):
    """
    Exponential function.

    Parameters:
        x (numpy.ndarray): Input data.
        a (float): Coefficient.
        b (float): Coefficient.
        c (float): Coefficient.

    Returns:
        numpy.ndarray: Output of the exponential function.
    """
    return a * np.exp(-(b * x))

def meanThreshold(matrix, limiar):
    """
    Calculate the mean of elements in the matrix that are above the threshold.

    Parameters:
        matrix (numpy.ndarray): Input matrix.
        limiar (float): Threshold value.

    Returns:
        float: Mean of elements above the threshold.
    """
    matrix_np = np.array(matrix)
    array_above_threshold = matrix_np[matrix_np > limiar]
    mean = np.mean(array_above_threshold)
    return mean
