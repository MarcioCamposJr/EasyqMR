import numpy as np

def DefSizeConstrast(image, cond):

    slices = []

    if cond:

        for i in range(len(image[:])):
            slices.append(image[i][0].pixel_array)

        min = ((2 ** 16) / np.amax(slices)) * 2 / 3
        max = ((2 ** 16) / np.amax(slices))

    else:

        for i in range(len(image[:])):
            slices.append(image[i].pixel_array)

        min = ((2 ** 16) / np.amax(slices)) * 2 / 3
        max = ((2 ** 16) / np.amax(slices))

    size = [min, max]

    return size