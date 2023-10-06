# import nibabel as nib
# from brainextractor import BrainExtractor
# import matplotlib.pyplot as plt
#
# input_nib = nib.load("C:/Users/marci/OneDrive/Desktop/MRI/NIFTI/3/sub-s118_ses-wk6_func_sub-s118_ses-wk6_task-placement_bold.nii")
# input_nib2 = nib.load("C:/Users/marci/OneDrive/Desktop/MRI/NIFTI/5/sub-s127_ses-wk1_T1w_defaced.nii")
# input_nib3 = nib.load("C:/Users/marci/OneDrive/Desktop/MRI/NIFTI/testConvert/901_relax_5xte20_sense.nii.gz")
# input_nib4 = nib.load("C:/Users/marci/OneDrive/Desktop/MRI/NIFTI/testConvert/701_axial_t1.nii.gz")
#
# bet2 = BrainExtractor(img = input_nib3)
# bet2.run()
#
# plt.imshow(bet2.data[5])
# plt.show()
# plt.imshow(bet2.compute_mask()[5])
# plt.show()
# plt.imshow(bet2.data[5]*bet2.compute_mask()[5])

