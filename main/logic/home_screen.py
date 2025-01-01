"""Начальный экран"""
# Импорт библиотек
import pygame
import sys
import os
# Импорт созданных классов и функций
from main.logic.load_images import load_image


class HomeScreen:
    def __init__(self):
        self.rect = (1920, 1080)

    @staticmethod
    def img() -> str:
        return os.path.join('main', 'images', 'home_screen.png')

    def start(self, screen):
        start_menu = pygame.image.load(self.img())
        screen.blit(start_menu, (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
