from .MappingTypes.T2 import mappingT2
import numpy as np
import cv2

class InitGeneration():
    def __init__(self, MRI, modalityMRI):
        super(InitGeneration, self).__init__()

        self.infomap = []
        self.Boundaries = []
        self.MRI = MRI

        if modalityMRI == 'T2':

            for i in range(len(MRI)):

                self.infomap.append(mappingT2(MRI[i]))

                self.Boundaries.append(self.MapBoundaries(self.infomap[i][0]))

        elif modalityMRI == 'T2*':
            pass

        elif modalityMRI == 'T1':
            pass

        elif modalityMRI == 'T1p':
            pass

        elif modalityMRI == 'IVIM':
            pass
    #
    #
    # def T2(self):
    #     pass
    #
    # def T2e(self):
    #     pass
    #
    # def T1(self):
    #     pass
    #
    # def T1p(self):
    #     pass
    #
    # def IVIM(self):
    #     pass

    def MapBoundaries(self, image):

        matrix = image[image > 0]

        normalized_matrix = ((matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))) * 255
        normalized_matrix = normalized_matrix.astype(np.uint8)

        factor = (np.max(matrix) / np.max(normalized_matrix))

        thresh_val, img_bin = cv2.threshold(normalized_matrix, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        threshold_value = thresh_val * factor

        return 0, int(threshold_value)


