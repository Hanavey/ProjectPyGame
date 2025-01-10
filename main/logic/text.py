# Импорт библиотек
import pygame


class Text:
    """Класс для текста"""
    def __init__(self, font_name: str=None, font_size: int=30, color: tuple[int, int, int]=(255, 255, 255)) -> None:
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(font_name, font_size)

    def render(self, screen, text: str, position: tuple[int, int], center: bool=False) -> None: # Вывод текста на экран
        text_surface = self.font.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position
        screen.blit(text_surface, text_rect)

    def set_color(self, color: tuple[int, int, int]) -> None:   # Изменение цвета
        self.color = color

    def set_font(self, font_name: str, font_size: int) -> None: # Изменение стилей
        self.font_name = font_name
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, font_size)
