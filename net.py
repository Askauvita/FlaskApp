from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO


# Функция добавления рамки
def add_border(image_path, border_size):
    img = Image.open(image_path)
    bordered_img = ImageOps.expand(img, border=border_size, fill='black')
    return bordered_img


# Функция создания графика распределения цветов
def create_color_distribution(image_path):
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)

    # Создаем гистограмму для каждого канала RGB
    r_channel = img_array[:, :, 0].flatten()
    g_channel = img_array[:, :, 1].flatten()
    b_channel = img_array[:, :, 2].flatten()

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("Распределение цветов", fontsize=16)

    # Общий график RGB
    axes[0, 0].hist(r_channel, bins=256, color='red', alpha=0.5, label='Red')
    axes[0, 0].hist(g_channel, bins=256, color='green', alpha=0.7, label='Green')
    axes[0, 0].hist(b_channel, bins=256, color='blue', alpha=0.9, label='Blue')
    axes[0, 0].set_title("Общее распределение")
    axes[0, 0].legend()

    # Графики для каждого канала
    axes[0, 1].hist(r_channel, bins=256, color='red')
    axes[0, 1].set_title("Красный канал")

    axes[1, 0].hist(g_channel, bins=256, color='green')
    axes[1, 0].set_title("Зеленый канал")

    axes[1, 1].hist(b_channel, bins=256, color='blue')
    axes[1, 1].set_title("Синий канал")

    # Сохраняем график в формате base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return image_base64