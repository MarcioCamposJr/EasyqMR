from .MappingTypes.T2 import mappingT2

class InitGeneration():
    def __init__(self, MRI, modalityMRI):
        super(InitGeneration, self).__init__()

        self.infomap = []

        if modalityMRI == 'T2':

            for i in range(len(MRI)):
                self.infomap.append(mappingT2(MRI[i]))

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