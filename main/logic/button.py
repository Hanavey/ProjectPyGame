# Импорт библиотек
import pygame
from typing import Callable
# Импорт созданных классов и функций
from main.logic.text import Text
from main.logic.load_images import load_image


class Button:
    """Класс кнопок"""
    def __init__(self, screen: pygame.Surface, dot: tuple[int, int], size: tuple[int, int], text: str=None,
                 text_color: tuple[int, int, int]=(255, 255, 255), image: pygame.image=None,
                 surface: pygame.Surface=None):
        self.screen = screen
        self.image = image
        self.x = dot[0]
        self.y = dot[1]
        self.w = size[0]
        self.h = size[1]
        self.text = text
        self.text_color = text_color
        self.surface = surface

    # Метод для получения размера текста
    def text_(self, text_color: tuple[int, int, int], font_path: str=None) -> tuple[int, int, int, str]:
        start_size = 100

        while True:
            font = pygame.font.Font(font_path, start_size)
            text_surface = font.render(self.text, True, text_color)
            text_width, text_height = text_surface.get_size()
            if text_width <= self.w and text_height <= self.y:
                break
            start_size -= 1

        text_x = self.x + (self.w - text_width) // 2
        text_y = self.y + (self.h - text_height) // 2

        return text_x, text_y, start_size - 20, font_path

    def render(self):   # Метод для вывода кнопки на экран
        if self.image is None:
            pygame.draw.rect(self.screen, (pygame.Color('green')), (self.x, self.y, self.w, self.h), 4)
            if self.text is not None:
                text_ = self.text_(self.text_color)
                Text(font_name=text_[3], font_size=text_[2], color=self.text_color).render(self.screen, self.text,
                                                                                           (text_[0], text_[1]))
        else:
            texture = pygame.transform.scale(load_image(self.image), (self.w, self.h))
            self.surface.blit(texture, (self.x, self.y))
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()

    def get_click(self, event_pos: tuple[int, int]) -> bool:    # Получение нажатия на кнопку
        pos_x, pos_y = event_pos
        if self.x <= pos_x <= self.x + self.w and self.y <= pos_y <= self.y + self.h:
            return True
        return False

    # Добавление функции, которая будет вызвана после нажатия на кнопку
    def connect(self, function: Callable, event_pos: tuple[int, int], args: tuple=()) -> None:
        if self.get_click(event_pos):
            function(*args)
