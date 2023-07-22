import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os

def create_gif(img_dicom, fp):      #CREATE DICOM IMAGE ANIMATION

    figures = []
    fig = plt.figure()

    #ASSIGNING DICOM IMAGES TO OBJECT
    for i in range(len(img_dicom)):
        image=plt.imshow(img_dicom[i].pixel_array , animated=True ,cmap='gray')
        figures.append([image])

    #TRANSFORMING IMAGES INTO GIF
    ani = animation.ArtistAnimation(fig, figures, interval=50, blit=True, repeat_delay=1000)
    path = os.path.dirname(os.path.abspath('None'))
    path = os.path.join(path, "Docs\Animation\preview.gif")
    ani.save(path, fps = fp)
