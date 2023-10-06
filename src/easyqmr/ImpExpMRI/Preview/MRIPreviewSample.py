from PIL import Image
from easyqmr.Preprocessing.FormattingMatrix import FormatTo8bits
import os

def create_gif(img_dicom, fp):      #CREATE DICOM IMAGE ANIMATION
#todo arrumar isto, pois o contraste ta zuado, tb ver de colocar as informacoes nos labels em baixo
    figures = []

    for i in range(len(img_dicom)):
        obj = FormatTo8bits(img_dicom[i].pixel_array)
        image = Image.fromarray(obj)
        figures.append(image)


    path = os.path.dirname(os.path.abspath('None'))
    path = os.path.join(path, "Docs\Animation\preview.gif")

    figures[0].save(path, save_all=True, append_images=figures[1:], duration=len(figures)*2, loop=0)
