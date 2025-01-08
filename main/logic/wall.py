import pygame
from main.logic.load_images import load_image


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], cell_size: int, wall_stage: int, *groups):
        super().__init__(*groups)
        stages = {
            0: load_image(f'wall0.png'),
            1: load_image(f'wall1.png'),
            11: pygame.transform.rotate(load_image(f'wall1.png'), 90),
            2: load_image(f'wall2.png'),
            21: pygame.transform.rotate(load_image(f'wall2.png'), 90),
            22: pygame.transform.rotate(load_image(f'wall2.png'), 180),
            23: pygame.transform.rotate(load_image(f'wall2.png'), 270),
            3: load_image(f'wall3.png'),
            31: pygame.transform.rotate(load_image(f'wall3.png'), 90),
            32: pygame.transform.rotate(load_image(f'wall3.png'), 180),
            33: pygame.transform.rotate(load_image(f'wall3.png'), 270),
            4: load_image(f'wall4.png'),
            5: load_image(f'wall5.png'),
            51: pygame.transform.rotate(load_image(f'wall5.png'), 90),
            52: pygame.transform.rotate(load_image(f'wall5.png'), 180),
            53: pygame.transform.rotate(load_image(f'wall5.png'), 270),
        }
        self.image = stages[wall_stage]
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * cell_size, pos[1] * cell_size)
        self.mask = pygame.mask.from_surface(self.image)
