# Импорт библиотек
import pygame
import os


def load_image(name, color_key=None):   # Функция для загрузки изображения
    """Загрузка изображения"""
    fullname = os.path.abspath(os.path.join('main', 'images', name))
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image
