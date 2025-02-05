from PIL import Image, ImageOps
import numpy as np

# Функция добавления рамки
def add_border(image_path, border_size):
    img = Image.open(image_path)
    bordered_img = ImageOps.expand(img, border=border_size, fill='black')
    return bordered_img

# Функция создания распределения цветов
def create_color_distribution(image):
    colors = np.array(image).reshape(-1, 3).mean(axis=0)
    return colors.tolist()
