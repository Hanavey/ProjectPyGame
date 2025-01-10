"""Основной файл, запускающий игру."""
# Импорт библиотек
import pygame
import sys
import numpy as np
from random import choice
# Импорт созданных классов и функций
from main.logic.button import Button
from main.logic.load_images import load_image
from main.logic.text import Text
from time import sleep
from main.logic.fade_in_out import fade_in_out
from main.logic.wall import Wall
from main.logic.board import Board
from main.logic.player import Player
from main.logic.grass import Grass
from main.logic.exit_maze import ExitMaze
from main.logic.camera import Camera


screen = pygame.display.set_mode((1920, 1080))
cell_size = 60
all_sprites_group = pygame.sprite.Group()


def option() -> None:
    screen.fill((255, 255, 255))
    Text(font_size=100, color=(0, 0, 0)).render(screen, 'Пока идет разработка(((', (960, 100), True)
    btn_return = Button(screen, (720, 300), (480, 50), text='Назад', text_color=(0, 0, 0))
    btn_return.render()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and btn_return.get_click(event.pos):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.flip()


def get_wall_stage(layout, x, y):
    neighbors = {
        "top": layout[y - 1][x] if y > 0 else 0,  # Сверху
        "bottom": layout[y + 1][x] if y < len(layout) - 1 else 0,  # Снизу
        "left": layout[y][x - 1] if x > 0 else 0,  # Слева
        "right": layout[y][x + 1] if x < len(layout[0]) - 1 else 0,  # Справа
    }

    # Определяем тип стены
    if all(v == 0 for v in neighbors.values()):
        return 0  # Wall0: одиночная стена

    # Wall4: перекресток с четырьмя соединениями
    if all(neighbors.values()):
        return 4  # Все 4 стороны соединены

    # Wall3: три соединения
    if sum(neighbors.values()) == 3:
        if not neighbors["top"]:
            return 31  # Вниз-влево-вправо
        if not neighbors["bottom"]:
            return 33  # Вверх-влево-вправо
        if not neighbors["left"]:
            return 32  # Вверх-вправо-вниз
        if not neighbors["right"]:
            return 3  # Вверх-влево-вниз

    # Wall2: углы
    if neighbors["top"] and neighbors["left"] and not (neighbors["bottom"] or neighbors["right"]):
        return 2  # Угол вверх-влево
    if neighbors["top"] and neighbors["right"] and not (neighbors["bottom"] or neighbors["left"]):
        return 23  # Угол вверх-вправо
    if neighbors["bottom"] and neighbors["right"] and not (neighbors["top"] or neighbors["left"]):
        return 22  # Угол вниз-вправо
    if neighbors["bottom"] and neighbors["left"] and not (neighbors["top"] or neighbors["right"]):
        return 21  # Угол вниз-влево

    # Wall1: обычная стена
    if neighbors["top"] and neighbors["bottom"] and not (neighbors["left"] or neighbors["right"]):
        return 1  # Вертикальная стена
    if neighbors["left"] and neighbors["right"] and not (neighbors["top"] or neighbors["bottom"]):
        return 11  # Горизонтальная стена (поворачиваем на 90 градусов)

    # Wall5: начало стены
    if neighbors["top"] and not any(v for k, v in neighbors.items() if k != "top"):
        return 5  # Смотрит вверх
    if neighbors["left"] and not any(v for k, v in neighbors.items() if k != "left"):
        return 51  # Смотрит влево
    if neighbors["right"] and not any(v for k, v in neighbors.items() if k != "right"):
        return 53  # Смотрит вправо
    if neighbors["bottom"] and not any(v for k, v in neighbors.items() if k != "bottom"):
        return 52  # Смотрит вниз

    # На случай ошибки: по умолчанию вертикальная стена
    return 1


def get_exit_stage(layout, x, y):
    neighbors = {
        "top": layout[y - 1][x] if y > 0 else 0,  # Сверху
        "bottom": layout[y + 1][x] if y < len(layout) - 1 else 0,  # Снизу
        "left": layout[y][x - 1] if x > 0 else 0,  # Слева
        "right": layout[y][x + 1] if x < len(layout[0]) - 1 else 0,  # Справа
    }

    if neighbors["left"] and neighbors["right"]:
        return 1
    if neighbors["top"] and neighbors["bottom"]:
        return 2


def create_walls(layout):
    walls = pygame.sprite.Group()
    grass = pygame.sprite.Group()
    exit_maze = pygame.sprite.Group()
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            Grass((x, y), cell_size, grass, all_sprites_group)
            if cell == 1:  # Если клетка - стена
                wall_stage = get_wall_stage(layout, x, y)
                Wall((x, y), cell_size, wall_stage, walls, all_sprites_group)
            if cell == 3:
                exit_stage = get_exit_stage(layout, x, y)
                ExitMaze((x, y), cell_size, exit_stage, exit_maze, all_sprites_group)
    return walls, grass, exit_maze


def play() -> None:
    board = Board(60, 60)  # 60x60 клеток
    board.set_view(0, 0, cell_size)
    screen.fill((0, 0, 0))
    clock1 = pygame.time.Clock()
    walls_data = create_walls(board.board)
    walls = walls_data[0]
    exit_maze = walls_data[2]
    camera = Camera(board.width * cell_size, board.height * cell_size, 1920, 1080)

    # Центр мира в пикселях
    world_center_x = (board.width * cell_size) // 2
    world_center_y = (board.height * cell_size) // 2

    # Создаём игрока в центре мира
    player = Player((world_center_x, world_center_y), cell_size, all_sprites_group)

    menu_btn = Button(screen, (10, 10), (30, 30), surface=screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_btn.connect(menu, event.pos)

        keys = pygame.key.get_pressed()
        check = player.move(keys, walls, exit_maze)
        if check:
            break

        # Обновление экрана
        camera.update(player)

        screen.fill((0, 0, 0))  # Заливка фона

        for sprite in all_sprites_group:
            screen.blit(sprite.image, camera.apply(sprite))


        pygame.display.flip()
        clock1.tick(75)


def quit_screen(screen_start) -> None:
    scr = fade_in_out(screen, screen_start, fade_in=False, max_alpha=122, speed=3)
    screen.blit(scr, (0, 0))
    no_btn = Button(screen, (460, 540), (400, 50), text='NO', image='main/images/Drawing (1).png', surface=screen)
    yes_btn = Button(screen, (1000, 540), (400, 50), text='YES', image='main/images/Drawing (1).png', surface=screen)
    Text(color=(255, 0, 0), font_size=100).render(screen, 'Выйти из игры?', (500, 360))
    no_btn.render()
    yes_btn.render()
    pygame.display.flip()
    while True:
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                break
            if event_.type == pygame.MOUSEBUTTONDOWN:
                if yes_btn.get_click(event_.pos):
                    sleep(0.1)
                    pygame.quit()
                    sys.exit()
                elif no_btn.get_click(event_.pos):
                    fade_in_out(screen, screen_start, speed=3, min_alpha=122)
                    return


def menu():
    pygame.init()
    pygame.display.set_caption('Разрушитель лабиринтов')
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    screen_start = pygame.image.load('main/images/home_screen.png')
    screen.blit(screen_start, (0, 0))
    button_start = Button(screen, (720, 425), (480, 50), image='main/images/Drawing (1).png', surface=screen_start)
    button_help = Button(screen, (720, 550), (480, 50), image='main/images/Drawing (1).png', surface=screen_start)
    button_exit = Button(screen, (720, 825), (480, 50), image='main/images/Drawing (1).png', surface=screen_start)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_start.connect(play, event.pos)
                button_help.connect(option, event.pos)
                button_exit.connect(quit_screen, event.pos, (screen_start,))
        button_start.render()
        button_help.render()
        button_exit.render()
        clock.tick(120)
    pygame.quit()


if __name__ == '__main__':
    menu()
