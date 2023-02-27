class SlicesMRI():
    def __init__(self, imageMRI):
        self.NumberSlices = self.SlicerCounter(imageMRI)
        self.OnlySlices = self.SepareteSlices(imageMRI)
        self.FewSlices = self.SepareteFewSlices(imageMRI)
        self.Matrix = self.FormulantinMatrixMRI(imageMRI)

    def SlicerCounter(self, imageMRI):
        if imageMRI[0].SliceLocation is not None: # Coloquei esta condicao ainda porque nao entendi muito bem a estrutura do nifti
            i=0
            cont = 0
            if len(imageMRI) !=0:
                while imageMRI[i].SliceLocation == imageMRI[i+1].SliceLocation:
                    i = i+1
                    cont = cont + 1
        else:
            cont = 0
        return cont

    def SepareteSlices(self, imageMRI):

        Slices = []
        j = 0
        i = 0
        counter = self.SlicerCounter(imageMRI)

        if counter != 0:
            Slices.append(imageMRI[0])
            while i < len(imageMRI)-1:
                if imageMRI[i].SliceLocation != imageMRI[i+1].SliceLocation:
                    Slices.append(imageMRI[i+1])
                i = i + 1
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
        if counter != 0:

            Slices = []
            SlicesInterm = []
            i = 0

            while i < len(imageMRI)-1:
                if imageMRI[i].SliceLocation == imageMRI[i+1].SliceLocation:
                    SlicesInterm.append(imageMRI[i])
                    i = i + 1
                else:
                    SlicesInterm.append(imageMRI[i])
                    Slices.append(SlicesInterm)
                    SlicesInterm = []
                    i = i + 1

            return Slices

        else:
            return imageMRI