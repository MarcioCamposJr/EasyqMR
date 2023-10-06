import numpy as np
import cv2
from dipy.segment.mask import median_otsu

from easyqmr.Alerts.Processing.UIProgressStepOpen import ProgressUI

class BET():

    def __init__(self, mri):

        super(BET, self).__init__()

        self.Progress = ProgressUI(Title='Brain Extraction Tool')
        self.Progress.show()

        self.firstBet = self.betMO(mri)
        self.Progress.updateProgress(100, 'Finishing Extracting brain... 100%')
        self.betDone = self.betGTO(self.firstBet)

        self.Progress.close()

        self.MRI = self.betDone

    def betGTO(self,mri):
        for i in range(len(mri)):

            image = mri[i][-1].pixel_array
            thresh_val, img_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            img_bin = cv2.convertScaleAbs(img_bin)

            # Encontrar os contornos dos objetos na imagem binarizada
            contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Encontrar o contorno do maior objeto (o cérebro)
            brain_contour = max(contours, key=cv2.contourArea)

            # Criar uma máscara para o cérebro
            brain_mask = np.zeros_like(img_bin)
            cv2.drawContours(brain_mask, [brain_contour], 0, 255, -1)

            for j in range(len(mri[0][:])):

                # Aplicar a máscara à imagem original para extrair apenas o cérebro
                mri[i][j].pixel_array = cv2.bitwise_and(mri[i][j].pixel_array, mri[i][j].pixel_array, mask=brain_mask)

                mri[i][j].maskFull = brain_mask

        return mri

    def betMO(self, mri):


        step = int(100/len(mri))

        for i in range(len(mri)):
            self.Progress.updateProgress(step * i, 'Extracting brain... ' + str(step*i) + '%')
            for j in range(len(mri[i])):
                b0_mask = median_otsu(mri[i][j].pixel_array,numpass=3, median_radius=3)[0]

                mri[i][j].pixel_array = b0_mask

        return mri