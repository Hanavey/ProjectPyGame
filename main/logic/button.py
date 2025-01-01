import pygame


class Button:
    def __init__(self, screen: pygame.Surface, x: int, y: int, w: int, h: int, image: pygame.image=None):
        self.screen = screen
        self.image = image
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def render(self):
        pygame.draw.rect(self.screen, (pygame.Color('green')), (self.x, self.y, self.w, self.h), 4)

    def get_click(self, event_pos: tuple[int, int]) -> bool:
        pos_x, pos_y = event_pos
        if self.x <= pos_x <= self.x + self.w and self.y <= pos_y <= self.y + self.h:
            return True
        return False
