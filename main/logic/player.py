# Импорт библиотек
import pygame
# Импорт созданных классов и функций
from main.logic.load_images import load_image


class Player(pygame.sprite.Sprite):
    """Класс игрока"""
    def __init__(self, pos: tuple[int, int], cell_size: int, img: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        # Создание изображения
        self.image = load_image(f'player{img}.png')
        self.image = pygame.transform.scale(self.image, (cell_size // 1.5, cell_size))
        # Создание rect объекта
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.speed = 4  # Переменная для скорости игрока
        # Создание маски объекта
        self.mask = pygame.mask.from_surface(self.image)
        # Переменные для разворота игрока
        self.left, self.right = False, True

    def check_collision(self, walls: pygame.sprite.Group, exit_maze: pygame.sprite.Group,
                        enemies: pygame.sprite.Group) -> int:
        for wall in walls:
            if pygame.sprite.collide_mask(self, wall):  # Проверка столкновения по маске со стенами
                return 1
        for exit_maze in exit_maze:
            if pygame.sprite.collide_mask(self, exit_maze): # Проверка столкновения по маске с выходом
                return 2
        for enemy in enemies:
            if pygame.sprite.collide_mask(self, enemy):
                return 3
        return 0

    def move(self, keys, walls: pygame.sprite.Group, exit_maze: pygame.sprite.Group,
             enemies: pygame.sprite.Group) -> int:
        dx, dy = 0, 0
        if keys[pygame.K_UP]:  # Движение вверх
            dy = -self.speed
        if keys[pygame.K_DOWN]:  # Движение вниз
            dy = self.speed
        if keys[pygame.K_LEFT]:  # Движение влево
            dx = -self.speed
            if self.left:
                self.image = pygame.transform.flip(self.image, True, False)
                self.right = True
                self.left = False
        if keys[pygame.K_RIGHT]:  # Движение вправо
            dx = self.speed
            if self.right:
                self.image = pygame.transform.flip(self.image, True, False)
                self.left = True
                self.right = False

        self.rect.x += dx
        if self.check_collision(walls, exit_maze, enemies) == 1: # Если сталкивается со стенами дальше не идет по оси X
            self.rect.x -= dx

        self.rect.y += dy
        if self.check_collision(walls, exit_maze, enemies) == 1: # Если сталкивается со стенами дальше не идет по оси X
            self.rect.y -= dy

        if self.check_collision(walls, exit_maze, enemies) == 2: # Если сталкивается с выходом, возвращается True
            return 1

        if self.check_collision(walls, exit_maze, enemies) == 3:
            return 2