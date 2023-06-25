def classification(image): #MRI METHOD CLASSIFICATION

    # if variation_detection(image) == False:
    #
    #     #MRI CLASSIFICATION IN RELAXOMETRY WEIGHTED
    #     if image[0][0].EchoTime > 50:
    #         clss = 'Ponderada em T2'
    #     else:
    #         clss = 'Ponderada em T1'
    #
    # else:
    #TODO ver se essas consideracoes fazem sentido e se nao seria melhor classificar pela variacao do parametro
    if image[0][0].RepetitionTime<=3000 and image[0][0].EchoTime >= 60:
        clss = 'T2'

    elif image[0][0].RepetitionTime<=3000 and image[0][0].EchoTime <= 30:
        clss = 'T2*'

    elif image[0][0].RepetitionTime>=500 and image[0][0].FlipAngle >= 5:
        clss = 'T1'

    elif image[0][0].InversionTime>=100 and image[0][0].FlipAngle >= 10:
        clss = 'T1p'

    elif image[0][0].DiffusionBValue > 0:
        clss = "IVIM"

    else:
        clss = 'Nao identificada'

    for i in range(len(image)):
        for j in range(len(image[0])):
            image[i][j].TypeMRI = clss

    return image