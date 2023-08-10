def MRItoMap(MRI):

    MRItoMap = []

    for i in range(len(MRI)):
        inter = []
        for j in range(len(MRI[i])):
            if MRI[i][j].fullROI or MRI[i][j].elliROI or MRI[i][j].rectROI or MRI[i][j].freeHandsROI:
                inter.append(MRI[i][j])
        if MRI[i][j].fullROI or MRI[i][j].elliROI or MRI[i][j].rectROI or MRI[i][j].freeHandsROI:
            MRItoMap.append(inter)

    return MRItoMap