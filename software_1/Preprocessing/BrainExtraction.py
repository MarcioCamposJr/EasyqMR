import numpy as np
import cv2

def bet(mri):

    for i in range(len(mri[:])):
        for j in range(len(mri[0][:])):

            image = mri[i][j].pixel_array
            thresh_val, img_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            img_bin = cv2.convertScaleAbs(img_bin)

            # Encontrar os contornos dos objetos na imagem binarizada
            contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Encontrar o contorno do maior objeto (o cérebro)
            brain_contour = max(contours, key=cv2.contourArea)

            # Criar uma máscara para o cérebro
            brain_mask = np.zeros_like(img_bin)
            cv2.drawContours(brain_mask, [brain_contour], 0, 255, -1)

            # Aplicar a máscara à imagem original para extrair apenas o cérebro
            brain_img = cv2.bitwise_and(image, image, mask=brain_mask)

            mri[i][j].pixel_array = brain_img

    return mri