"""Основной файл, запускающий игру."""
import os.path

# Импорт библиотек
import pygame
import os
# Импорт созданных классов и функций
from main.logic.board import Board
from main.logic.home_screen import HomeScreen
from main.logic.load_images import load_image


def Main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Разрушитель лабиринтов')

    clock = pygame.time.Clock()

    start_menu = HomeScreen(screen, 'home_screen.png', True)
    el = start_menu.render(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if el == 1:
            screen.fill((0, 0, 0))
        elif el == 2:
            screen.fill((255, 255, 255))
        else:
            el = start_menu.render(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    Main()
