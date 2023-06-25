def FormattedMRI(MRI, image_type):


    if image_type == 'DICOM':
        # for i in range(len(MRI)): #Modelo antigo
        FormatMRI = MRIImage(MRI, image_type)
        return FormatMRI

    if image_type == 'NIfTI':
        FormatMRI = []
        dataPixel = MRI.get_fdata()

        if dataPixel.shape[1] == dataPixel.shape[0]:
            lenMRI = dataPixel.shape[2]
            dataPixel = dataPixel[:1]

        if dataPixel.shape[1] == dataPixel.shape[2]:
            lenMRI = dataPixel.shape[0]
            dataPixel = dataPixel[1:]

        for i in range(int(lenMRI)):
            FormatMRI.append(MRIImage(MRI,image_type, data = dataPixel))

        return FormatMRI

class MRIImage():

    def __init__(self, MRI, image_type,data =  None ):

        if image_type == 'DICOM':
            self.ImageFormated = self.FormatDicom(MRI)

        if image_type == 'NIfTI':
            self.ImageFormated = self.FormatNIfTI(MRI, data)

    def FormatDicom(self,MRI):
        # if hasattr(MRI, 'InversionTime'): ##Todo condicao para verificar se variavel existe
        self.pixel_array = MRI.pixel_array
        self.SliceLocation = MRI.SliceLocation

        self.EchoTime = MRI.EchoTime
        self.RepetitionTime = MRI.RepetitionTime
        self.InversionTime = None
        self.FlipAngle = MRI.FlipAngle
        self.DiffusionBValue = MRI.DiffusionBValue

        self.PatientName = MRI.PatientName
        self.BodyPartExamined = MRI.BodyPartExamined
        self.MRAcquisitionType = MRI.MRAcquisitionType
        self.SeriesDescription = MRI.SeriesDescription
        self.PixelSpacing = MRI.PixelSpacing

        self.TypeMRI = None

    def FormatNIfTI(self, MRI, data):

        self.pixel_array = data
        self.SliceLocation = None

        self.RepetitionTime = MRI.header.get('repetition_time')
        self.EchoTime= MRI.header.get('echo_time')
        self.InversionTime = None
        self.FlipAngle = None
        self.DiffusionBValue = None

        self.PatientName = None
        self.BodyPartExamined = None
        self.MRAcquisitionType = None
        self.SeriesDescription = None
        self.PixelSpacing = None

        self.TypeMRI = None
