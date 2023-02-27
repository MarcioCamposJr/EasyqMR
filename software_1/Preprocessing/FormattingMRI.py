def FormattedMRI(MRI, image_type):

    FormatMRI = []

    if image_type == 'DICOM':
        for i in range(len(MRI)):
            FormatMRI.append(MRIImage(MRI[i], image_type))

    if image_type == 'NIfTI':
        dataPixel = MRI.get_fdata()
        for i in range(dataPixel.shape[0]):
            FormatMRI.append(MRIImage(MRI,image_type, count= i ))

    print(type(FormatMRI[0].pixel_array))
    print(FormatMRI[0].pixel_array)

    return FormatMRI

class MRIImage():

    def __init__(self, MRI, image_type, count = None):

        self.image_type = image_type

        self.count = count

        if self.image_type == 'DICOM':
            self.ImageFormated = self.FormatDicom(MRI)

        if self.image_type == 'NIfTI':
            self.ImageFormated = self.FormatNIfTI(MRI, self.count)

    def FormatDicom(self,MRI):

        self.pixel_array = MRI.pixel_array
        self.SliceLocation = MRI.SliceLocation
        self.EchoTime = MRI.EchoTime
        self.RepetitionTime = MRI.RepetitionTime
        self.PatientName = MRI.PatientName
        self.BodyPartExamined = MRI.BodyPartExamined
        self.MRAcquisitionType = MRI.MRAcquisitionType
        self.SeriesDescription = MRI.SeriesDescription
        self.PixelSpacing = MRI.PixelSpacing

    def FormatNIfTI(self, MRI, count):

        dataPixel = MRI.get_fdata()

        self.pixel_array = dataPixel[count]
        self.SliceLocation = None
        self.RepetitionTime = MRI.header.get('repetition_time')
        self.EchoTime= MRI.header.get('echo_time')
        self.PatientName = None
        self.BodyPartExamined = None
        self.MRAcquisitionType = None
        self.SeriesDescription = None
        self.PixelSpacing = None
