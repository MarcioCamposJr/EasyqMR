import numpy as np

def FormattedMRI(MRI, image_type):

    FormatMRI = []

    if image_type == 'DICOM':
        for i in range(len(MRI)): #Modelo antigo
            FormatMRI.append(MRIImage(MRI[i], image_type))
    return FormatMRI


    if image_type == 'NIfTI':
        dataPixel = MRI.get_fdata()

        if dataPixel.shape[0] == dataPixel.shape[1]:
            lenMRI = dataPixel.shape[2]
            dataPixel = dataPixel[:1]

        if dataPixel.shape[1] == dataPixel.shape[2]:
            lenMRI = dataPixel.shape[0]
            dataPixel = dataPixel[1:]

        for i in range(int(lenMRI)):
            FormatMRI.append(MRIImage(MRI,image_type, count= i , data = dataPixel))

        return FormatMRI

class MRIImage():

    def __init__(self, MRI, image_type,data =  None , count = None):

        self.image_type = image_type

        self.count = count

        self.data = data

        if self.image_type == 'DICOM':
            self.ImageFormated = self.FormatDicom(MRI)

        if self.image_type == 'NIfTI':
            self.ImageFormated = self.FormatNIfTI(MRI, self.count, self.data)

    def FormatDicom(self,MRI):
        self.pixel_array = FormatTo16bits(MRI.pixel_array)
        self.SliceLocation = MRI.SliceLocation
        self.EchoTime = MRI.EchoTime
        self.RepetitionTime = MRI.RepetitionTime
        self.PatientName = MRI.PatientName
        self.BodyPartExamined = MRI.BodyPartExamined
        self.MRAcquisitionType = MRI.MRAcquisitionType
        self.SeriesDescription = MRI.SeriesDescription
        self.PixelSpacing = MRI.PixelSpacing
        MRI.

        self.Type = 'DICOM'

    def FormatNIfTI(self, MRI, count, data):

        self.pixel_array = FormatTo16bits(data)
        self.SliceLocation = None
        self.RepetitionTime = MRI.header.get('repetition_time')
        self.EchoTime= MRI.header.get('echo_time')
        self.PatientName = None
        self.BodyPartExamined = None
        self.MRAcquisitionType = None
        self.SeriesDescription = None
        self.PixelSpacing = None

        self.Type = 'NIfTI'

    # def FormatMatrix(self, matrix):
    #
    #     matrix = (matrix - np.min(matrix)) /((np.max(matrix) - np.min(matrix)))
    #
    #     matrix = (matrix*(2**16)).astype(np.uint16)
    #     return matrix
