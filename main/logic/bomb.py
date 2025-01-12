import pygame
from main.logic.load_images import load_image


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.world_x = self.x * cell_size
        self.world_y = self.y * cell_size
        self.cell_size = cell_size
        self.image = pygame.transform.scale(load_image('bomb.png'), (self.cell_size, self.cell_size))
        self.rect = self.image.get_rect(topleft=(self.world_x, self.world_y))
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = pygame.time.get_ticks()
        self.explode_time = 200

    def explosion(self, maze, enemy_group, wall_group):
        current_time = pygame.time.get_ticks()
        updated_cells = []  # Список измененных клеток

        if current_time - self.timer >= self.explode_time:
            explosion_area = self.get_explosion_area()

            # Удаляем врагов в зоне взрыва
            for enemy in enemy_group:
                if enemy.rect.colliderect(explosion_area):
                    enemy.kill()

            # Удаляем стены в зоне взрыва
            for wall in wall_group:
                if wall.rect.colliderect(explosion_area):
                    cell_x, cell_y = wall.rect.topleft[0] // self.cell_size, wall.rect.topleft[1] // self.cell_size
                    if 0 < cell_x < len(maze[0]) - 1 and 0 < cell_y < len(maze) - 1:
                        if maze[cell_y][cell_x] == 1:  # Если это стена
                            maze[cell_y][cell_x] = 0  # Удаляем из уровня
                            updated_cells.append((cell_x, cell_y))
                        wall.kill()  # Удаляем спрайт стены

            self.kill()  # Удаляем саму бомбу

        return maze, enemy_group, updated_cells

    def get_explosion_area(self):
        return pygame.Rect(
            (self.x - 1) * self.cell_size,
            (self.y - 1) * self.cell_size,
            3 * self.cell_size,
            3 * self.cell_size
        )
