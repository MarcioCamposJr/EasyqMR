def FormattedMRI(MRI, image_type):

    FormatMRI = []

    for i in range(len(MRI)):
        FormatMRI.append(MRIImage(MRI[i], image_type))

    return FormatMRI

class MRIImage:
    def __init__(self, MRI, image_type):

        self.image_type = image_type

        if self.image_type == 'DICOM':

            self.pixel_array = MRI.pixel_array
            self.SliceLocation = MRI.SliceLocation
            self.EchoTime = MRI.EchoTime
            self.RepetitionTime = MRI.RepetitionTime
            self.PatientName = MRI.PatientName
            self.BodyPartExamined = MRI.BodyPartExamined
            self.MRAcquisitionType = MRI.MRAcquisitionType
            self.SeriesDescription = MRI.SeriesDescription
            self.PixelSpacing = MRI.PixelSpacing

        if self.image_type == 'NIfTI':

            self.pixel_array = MRI.pixel_array
            self.SliceLocation = MRI.SliceLocation
            self.EchoTime = MRI.EchoTime
            self.RepetitionTime = MRI.RepetitionTime
            self.PatientName = MRI.PatientName
            self.BodyPartExamined = MRI.BodyPartExamined
            self.MRAcquisitionType = MRI.MRAcquisitionType
            self.SeriesDescription = MRI.SeriesDescription
            self.PixelSpacing = MRI.PixelSpacing