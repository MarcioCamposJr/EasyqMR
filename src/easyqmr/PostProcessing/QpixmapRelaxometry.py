from qtpy.QtGui import QPixmap, QImage, QColor, QPainter

def create_pixmap_from_matrix(matrix):
    # Crie uma imagem QImage a partir da matriz
    image = QImage(matrix.data, matrix.shape[1], matrix.shape[0], QImage.Format_Grayscale8)

    # Crie um QPainter para desenhar a colorbar na imagem
    colorbar_pixmap = create_colorbar_pixmap(matrix.shape[0])
    image_with_colorbar = combine_image_and_colorbar(image, colorbar_pixmap)

    # Crie um QPixmap a partir da imagem com a colorbar
    pixmap = QPixmap.fromImage(image_with_colorbar)
    return pixmap

def create_colorbar_pixmap(height):
    colorbar_width = 20
    colorbar_image = QImage(colorbar_width, height, QImage.Format_RGB32)

    for y in range(height):
        normalized_value = y / (height - 1)
        color = get_color_value(normalized_value)
        colorbar_image.setPixelColor(colorbar_width - 1, y, color)

    colorbar_pixmap = QPixmap.fromImage(colorbar_image)
    return colorbar_pixmap

def combine_image_and_colorbar(image, colorbar):
    combined_image = image.copy()
    painter = QPainter(combined_image)
    painter.drawPixmap(image.width(), 0, colorbar)
    painter.end()
    return combined_image

def get_color_value(value):

    color = QColor(255, int(255 * value), 0)  # Exemplo: Vermelho a Amarelo
    return color
