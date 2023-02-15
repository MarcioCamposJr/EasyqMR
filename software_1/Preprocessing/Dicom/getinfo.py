def getInfoDicom(MRIDicom):
    info = []
    info.append(MRIDicom.PatientName)
    info.append(MRIDicom.BodyPartExamined)
    info.append(MRIDicom.MRAcquisitionType)
    info.append(MRIDicom.SeriesDescription)
    return info