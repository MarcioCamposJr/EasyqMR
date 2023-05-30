from pathlib import Path
import pydicom as dicom
from qtpy.QtWidgets import QFileDialog,QDialog

class OpenMRI(QDialog):
    def __init__(self):
        super(OpenMRI, self).__init__()
        self.path = self.brosewfiles()
        if self.path:
            self.imageMRI = self.importData(self.path)

    def brosewfiles(self):
        filedialog = QFileDialog()
        # filedialog.setFixedHeight(720)
        # filedialog.setFixedWidth(480)
        path = filedialog.getExistingDirectory(self, 'Open file','C:/Users/marci/OneDrive/Desktop')
        filedialog.show()
        return path

    def importData(self, path_to_MRI):
        path_to_MRI = Path(path_to_MRI)
        all_files = list(path_to_MRI.glob("*"))

        mri_data = []

        for path in all_files:
            data = dicom.read_file(path)
            mri_data.append(data)

        return mri_data