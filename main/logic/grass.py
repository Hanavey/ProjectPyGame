# Импорт библиотек
import pygame
# Импорт созданных классов и функций
from main.logic.load_images import load_image


class Grass(pygame.sprite.Sprite):
    """Класс травы"""
    def __init__(self, pos: tuple[int, int], cell_size: int, *groups):
        super().__init__(*groups)
        # Создание изображения
        self.image = load_image('grass.png')
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        # Создание rect объекта
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * cell_size, pos[1] * cell_size)
        # Создание маски объекта
        self.mask = pygame.mask.from_surface(self.image)
