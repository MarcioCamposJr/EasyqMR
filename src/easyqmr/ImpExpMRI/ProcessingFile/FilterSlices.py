class SlicesMRI():
    def __init__(self, imageMRI):
        self.NumberSlices = self.SlicerCounter(imageMRI)
        self.OnlySlices = self.SepareteSlices(imageMRI)
        self.FewSlices = self.SepareteFewSlices(imageMRI)
        self.Matrix = self.FormulantinMatrixMRI(imageMRI)

    #Gera vetor contendo numero de imagens de mesma fatia
    def SlicerCounter(self, imageMRI):
        i=0
        j=0
        cont = []
        cont.append(0)
        while i < (len(imageMRI)-1):
            if imageMRI[i].SliceLocation == imageMRI[i+1].SliceLocation:
                j = j + 1
            else:
                j = j + 1
                cont.append(j)

            i = i +1
        return cont

    def SepareteSlices(self, imageMRI):

        Slices = []
        counter = self.SlicerCounter(imageMRI)
        total = 0

        if counter[0] != 1:
            for i in range(len(counter)-1):
                # total = total + counter[i]
                Slices.append(imageMRI[counter[i]])

            return Slices
        else:
            return imageMRI

    def SepareteFewSlices(self, imageMRI):
        Slices = self.SepareteSlices(imageMRI)
        if len(Slices)> 15:
            Slices = Slices[0:15]

        return Slices

    #Defininco matrix bidimensional, contendo primeira dimensao a fatia e a segunda a variacao do paramentro
    def FormulantinMatrixMRI(self,imageMRI):

        counter = self.SlicerCounter(imageMRI)

        Slices = []
        SlicesInterm = []
        j=0
        for i in range(len(imageMRI)):
            if i == 0 and i == counter[j]:
                SlicesInterm.append(imageMRI[i])

                if j != len(counter)-1:
                    j = j + 1

            elif i == counter[j] and i != 0:
                Slices.append(SlicesInterm)

                SlicesInterm = []
                SlicesInterm.append(imageMRI[i])

                if j != len(counter)-1:
                    j = j + 1

            elif i == len(imageMRI)-1:
                SlicesInterm.append(imageMRI[i])
                Slices.append(SlicesInterm)

            else:
                SlicesInterm.append(imageMRI[i])

        return Slices
