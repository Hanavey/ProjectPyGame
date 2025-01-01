"""Начальный экран"""
# Импорт библиотек
import pygame
import sys
import os
# Импорт созданных классов и функций
from main.logic.load_images import load_image
from main.logic.button import Button
from main.logic.Text import Text


class HomeScreen:
    def __init__(self, screen, img, hit_box=False):
        self.rect = (1920, 1080)
        self.img1 = img
        self.screen = screen
        self.hit_box = hit_box
        self.button_start = Button(self.screen, 721, 424, 478, 50)
        self.button_help = Button(self.screen, 721, 550, 478, 50)

    def img(self) -> str:
        return os.path.join('main', 'images', self.img1)

    def render(self, screen):
        start_menu = pygame.image.load(self.img())
        screen.blit(start_menu, (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.button_start.get_click(event.pos):
                        return 1
                    if event.button == 1 and self.button_help.get_click(event.pos):
                        return 2
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 1
            if self.hit_box:
                self.button_start.render()
                self.button_help.render()
            return 0
