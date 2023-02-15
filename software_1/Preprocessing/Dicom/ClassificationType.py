def classification(image): #MRI METHOD CLASSIFICATION

    if variation_detection(image) == False:

        #MRI CLASSIFICATION IN RELAXOMETRY WEIGHTED
        if image[0].EchoTime > 50:
            clss = 'Ponderada em T2'
        else:
            clss = 'Ponderada em T1'

    elif variation_detection(image) == True:

        if image[0].EchoTime != image[1].EchoTime or image[0].RepetitionTime != image[1].RepetitionTime:

            if np.mean(image[0].pixel_array) - np.mean(image[1].pixel_array) > 0 :
                clss = 'Imagem de T2'
            elif np.mean(image[0].pixel_array) - np.mean(image[1].pixel_array) < 0 :
                clss = 'Imagem de T1'

        else:
            clss = 'Imagem de IVIM'

    else:
        clss = 'Nao identificada'

    return clss