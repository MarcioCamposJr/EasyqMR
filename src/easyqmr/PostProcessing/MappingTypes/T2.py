import numpy as np
from scipy.optimize import curve_fit
import time
import copy

def mappingT2(image):
    """
    Calculate T2 map, constant magnitude map, offset map, and error map from input images.

    Parameters:
        image (list): List of DICOM images.

    Returns:
        list: [t2_map, consMag, offset, errorMap]
    """
    start_time = time.time()

    echo_times = np.array([float(dcm.EchoTime) for dcm in image])
    data = np.array([dcm.pixel_array for dcm in image])

    t2_map = np.zeros(data.shape[1:])
    consMag = np.zeros(data.shape[1:])
    errorMap = np.zeros(data.shape[1:])
    mean = meanThreshold(data, 5000)

    for i in range(data.shape[1]):
        print(i)
        for j in range(data.shape[2]):
            if image[0].fullMask[i][j] and data[0, i, j] > 5000:
                try:
                    y = np.log(data[:, i, j] + 1)
                    fit = np.polyfit(echo_times, y, 1)
                    initial_guess = [np.exp(fit[1]), (-1/fit[0])]

                except RuntimeError as e:
                    initial_guess = [mean, 0]

                try:
                    params, _ = curve_fit(exponential_func, echo_times, data[:, i, j], p0=initial_guess)

                    a, b = copy.copy(params)
                    a, b = (0, 0) if b > 1000 or b < 0 else (a, b)

                except RuntimeError as e:
                    a, b = 0, 0

            else:
                a, b = 0, 0


            consMag[i, j] = a
            t2_map[i, j] = b

            if np.isnan(data[:, i, j]).any() or data[0, i, j] < 5000:
                errorMap[i, j] = 0
            else:
                y_pred = exponential_func(echo_times, a, b)
                residuals = y_pred - data[:, i, j]
                ss_residuals = np.sum(residuals ** 2)
                ss_total = np.sum((data[:, i, j] - np.mean(data[:, i, j])) ** 2)
                errorMap[i, j] = max(0, 1 - (ss_total / ss_residuals))

    end_time = time.time()

    # Calcula a duração da execução
    duration = end_time - start_time
    print(f'Duração da execução: {duration:.6f} segundos')

    return [t2_map, consMag, errorMap, image[0].SliceLocation, data, echo_times]

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
