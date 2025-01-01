"""Основной файл, запускающий игру."""
# Импорт библиотек
import pygame
# Импорт созданных классов и функций
from main.logic.board import Board
from main.logic.home_screen import HomeScreen
from main.logic.load_images import load_image


def Main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Разрушитель лабиринтов')

    clock = pygame.time.Clock()

    start_menu = HomeScreen()
    el = start_menu.start(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    Main()
