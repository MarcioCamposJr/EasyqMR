import imageio
import numpy as np
import io
from PIL import Image, ImageDraw
from PyQt5.QtGui import QMovie, QImage
from PyQt5.QtCore import QBuffer, QByteArray, QSize
from PIL import Image
from PyQt5.QtGui import QPixmap

def create_gif(mri):

# Cria as imagens e adiciona aos frames do GIF
    ims = []
    for i in range(len(mri)):
        im = np.array(mri[i].pixel_array)
        ims.append(im.astype(np.uint8))
    # Cria um buffer de memória para armazenar as imagens
    frames = []
    for matrix in ims:
        # Criar uma imagem a partir da matriz
        image = Image.fromarray(matrix)

        # Adicionar a imagem à lista de quadros
        frames.append(image)

    buffer = io.BytesIO()
    imageio.mimsave(buffer, frames, format='GIF', loop =1, duration =0.9)
    imageio.mimsave("G:\Meu Drive\Projeto InBrain 2022\EasyqMRI\software_1\Docs\Animation\preview.gif", frames, format='GIF', loop =15, duration =0.4)

    movie = QMovie(buffer.getbuffer())

    return movie

