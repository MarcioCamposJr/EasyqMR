import matplotlib.animation as animation
import matplotlib.pyplot as plt

def create_gif(img_dicom, fp):      #CREATE DICOM IMAGE ANIMATION
    i=0
    figures = []
    fig = plt.figure()

    #ASSIGNING DICOM IMAGES TO OBJECT
    for i in range(len(img_dicom)):
        image=plt.imshow(img_dicom[i].pixel_array , animated=True ,cmap='gray',extent=[0, img_dicom[i].PixelSpacing[0]*len(img_dicom[i].pixel_array[0,:]), 0, img_dicom[i].PixelSpacing[1]*len(img_dicom[i].pixel_array[:,0])])
        #plt.title(str(img_dicom[i].SliceLocation))
        figures.append([image])

    #TRANSFORMING IMAGES INTO GIF
    ani = animation.ArtistAnimation(fig, figures, interval=50, blit=True, repeat_delay=1000)
    ani.save("G:\Meu Drive\Projeto InBrain 2022\EasyqMRI\software_1\Docs\Animation\preview.gif", fps = fp)