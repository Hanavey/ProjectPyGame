# Импорт библиотек
import pygame
# Импорт созданных классов и функций
from main.logic.load_images import load_image


class Player(pygame.sprite.Sprite):
    """Класс игрока"""
    def __init__(self, pos: tuple[int, int], cell_size: int, img: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        # Загрузка изображений для анимации
        self.images = [
            pygame.transform.scale(load_image(f'player{img}.png'), (cell_size // 1.5, cell_size)),
            pygame.transform.scale(load_image(f'player{img}_1.png'), (cell_size // 1.5, cell_size)),
            pygame.transform.scale(load_image(f'player{img}_2.png'), (cell_size // 1.5, cell_size)),
        ]
        self.image = self.images[0]  # Устанавливаем начальное изображение
        # Создание rect объекта
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.speed = 4  # Переменная для скорости игрока
        # Создание маски объекта
        self.mask = pygame.mask.from_surface(self.image)
        # Переменные для разворота игрока
        self.left, self.right = False, True
        # Счётчик для анимации
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 10  # Скорость анимации

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]

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
        is_moving = False  # Флаг для проверки движения
        if keys[pygame.K_UP]:  # Движение вверх
            dy = -self.speed
            is_moving = True
        if keys[pygame.K_DOWN]:  # Движение вниз
            dy = self.speed
            is_moving = True
        if keys[pygame.K_LEFT]:  # Движение влево
            dx = -self.speed
            is_moving = True
            if self.left:
                self.images = [pygame.transform.flip(image, True, False) for image in self.images]
                self.right = True
                self.left = False
        if keys[pygame.K_RIGHT]:  # Движение вправо
            dx = self.speed
            is_moving = True
            if self.right:
                self.images = [pygame.transform.flip(image, True, False) for image in self.images]
                self.left = True
                self.right = False

        self.rect.x += dx
        if self.check_collision(walls, exit_maze, enemies) == 1:  # Если сталкивается со стенами дальше не идет по оси X
            self.rect.x -= dx

        self.rect.y += dy
        if self.check_collision(walls, exit_maze, enemies) == 1:  # Если сталкивается со стенами дальше не идет по оси Y
            self.rect.y -= dy

        if is_moving:
            self.update_animation()  # Обновляем анимацию, если игрок движется
        else:
            self.image = self.images[0]  # Возвращаемся к первому кадру, если игрок остановился

        if self.check_collision(walls, exit_maze, enemies) == 2:  # Если сталкивается с выходом
            return 1

        if self.check_collision(walls, exit_maze, enemies) == 3:  # Если сталкивается с врагами
            return 2