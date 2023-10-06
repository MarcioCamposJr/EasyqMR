from qtpy.QtWidgets import QFileDialog,QDialog
import nibabel as nib
from pathlib import Path

class OpenNII(QDialog):
    def __init__(self):
        super(OpenNII, self).__init__()
        self.path = self.brosewfiles()
        if self.path:
            self.imageMRI = self.importData(self.path)

    def brosewfiles(self):
        filedialog = QFileDialog()
        path = filedialog.getOpenFileName(self, 'Open file','C:/Users/marci/OneDrive/Desktop','NIfTi (*.nii)')
        filedialog.show()
        return path[0]

    def importData(self, path_to_MRI):
        path_to_MRI = Path(path_to_MRI)

        mri_data = nib.load(path_to_MRI)

        return mri_data