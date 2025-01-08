import pygame
from main.logic.load_images import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], cell_size, *groups):
        super().__init__(*groups)
        self.image = load_image('player1.png')
        self.image = pygame.transform.scale(self.image, (cell_size // 1.5, cell_size))
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.left, self.right = False, True

    def check_collision(self, walls):
        for wall in walls:
            if pygame.sprite.collide_mask(self, wall):  # Проверка столкновения по маске
                return True
        return False

    def move(self, keys, walls):
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
        if self.check_collision(walls):
            self.rect.x -= dx

        self.rect.y += dy
        if self.check_collision(walls):
            self.rect.y -= dy
