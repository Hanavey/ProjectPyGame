import pygame
from main.logic.load_images import load_image


class Grass(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], cell_size: int, *groups):
        super().__init__(*groups)
        self.image = load_image('grass.png')
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * cell_size, pos[1] * cell_size)
        self.mask = pygame.mask.from_surface(self.image)
