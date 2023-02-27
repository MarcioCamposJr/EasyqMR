def sort_slices(info):  #SORT DICOM SLICES
    if info[0].SliceLocation is not None:
        i = 0
        k = 0
        sequence = []
        order = []
        cont = range(len(info))

        #ASSIGNING SLICE POSITION VALUES
        for i in range(len(info)):
            sequence.append(info[i].SliceLocation)

        #ARRANGE SLICE SEQUENCE VALUES
        sequence.sort()
        j=0

        #ARRANGE DICOM SLICE SEQUENCE
        while k != len(info)-1:

            if sequence[k] == info[j].SliceLocation:
                order.append(info[j])
                k=k+1
            if j == len(info)-1:
                j=0
            j=j+1

        return order
    else:
        return info
