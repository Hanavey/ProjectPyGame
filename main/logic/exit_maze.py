import pygame
from main.logic.load_images import load_image


class ExitMaze(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], cell_size: int, exit_maze_stage: int, *groups):
        super().__init__(*groups)
        stages = {
            1: load_image('exit_maze.png'),
            2: pygame.transform.rotate(load_image('exit_maze.png'), 90)
        }
        self.image = stages[exit_maze_stage]
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0] * cell_size, pos[1] * cell_size)
        self.mask = pygame.mask.from_surface(self.image)
