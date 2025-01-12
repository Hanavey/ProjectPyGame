"""Основной файл, запускающий игру."""
# Импорт библиотек
from random import choice
import sqlite3
import bcrypt
import pygame
import sys
import os
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
from main.logic.enemy import Enemy
from main.logic.line_edit import LineEdit
from main.logic.bomb import Bomb


# Запуск экрана
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
# Константа
CELL_SIZE = 60


def option() -> None:   # Экран опций
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


def get_wall_stage(layout, x, y):   # Функция обработки стен (Состояние стены)
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

    return 1


def get_exit_stage(layout, x, y):   # Состояние выхода (направление)
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


def lost_screen():  # Экран проигрыша
    screen.fill((0, 0, 0))
    lost_image = pygame.transform.scale(load_image('lost_screen.png'), (1920, 1080))
    new_game_btn = Button(screen, (150, 660), (630, 180), image='new_game.jpg', surface=lost_image)
    exit_btn = Button(screen, (1135, 660), (630, 180), image='exit.jpg', surface=lost_image)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_game_btn.connect(play, event.pos)
                    exit_btn.connect(main_menu, event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        new_game_btn.render()
        exit_btn.render()
        screen.blit(lost_image, (0, 0))


def win_screen():   # Экран выигрыша
    screen.fill((0, 0, 0))
    lost_image = pygame.transform.scale(load_image('win_screen.png'), (1920, 1080))
    new_game_btn = Button(screen, (150, 660), (630, 180), image='new_game.jpg', surface=lost_image)
    exit_btn = Button(screen, (1135, 660), (630, 180), image='exit.jpg', surface=lost_image)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_game_btn.connect(play, event.pos)
                    exit_btn.connect(main_menu, event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        new_game_btn.render()
        exit_btn.render()
        screen.blit(lost_image, (0, 0))


def play() -> None: # Основная функция игры
    def create_walls(layout, updated_cells1=None):  # Функция для создания стен
        walls1 = pygame.sprite.Group()
        if updated_cells1:
            for cell1 in updated_cells1:
                x1, y1 = cell1
                if layout[y1][x1] == 0:  # Если ячейка пустая
                    for wall in walls:  # Удаляем соответствующий спрайт
                        if wall.rect.topleft == (x1 * CELL_SIZE, y1 * CELL_SIZE):
                            wall.kill()
                else:  # Перерисовываем стену, если она есть
                    wall_stage = get_wall_stage(layout, x1, y1)
                    Wall((x1, y1), CELL_SIZE, wall_stage, walls, all_sprites_group)
            return walls1
        grass = pygame.sprite.Group()   # Группа травы
        exit_maze1 = pygame.sprite.Group()  # Группа для выхода
        for y1, row1 in enumerate(layout):
            for x1, cell1 in enumerate(row1):
                Grass((x1, y1), CELL_SIZE, grass, all_sprites_group)
                if cell1 == 1:  # Если клетка - стена
                    wall_stage = get_wall_stage(layout, x1, y1)
                    Wall((x1, y1), CELL_SIZE, wall_stage, walls1, all_sprites_group)
                if cell1 == 3:  # Если клетка - выход
                    exit_stage = get_exit_stage(layout, x1, y1)
                    ExitMaze((x1, y1), CELL_SIZE, exit_stage, exit_maze1, all_sprites_group)
        return walls1, grass, exit_maze1

    board = Board(60, 60)  # 60x60 клеток
    board.set_view(0, 0, CELL_SIZE)
    empty_cells = []
    for y, row in enumerate(board.board):
        for x, cell in enumerate(row):
            if cell == 0:
                if not 25 < x < 35 and not 25 < y < 35:
                    empty_cells.append((x, y))
    screen.fill((0, 0, 0))
    clock1 = pygame.time.Clock()
    walls_data = create_walls(board.board)
    # Группы спрайтов
    all_sprites_group = pygame.sprite.Group()
    walls = walls_data[0]
    exit_maze = walls_data[2]
    enemies = pygame.sprite.Group()
    camera = Camera(board.width * CELL_SIZE, board.height * CELL_SIZE, 1920, 1080)

    for _ in range(20): # Создание врагов
        x, y = choice(empty_cells)
        Enemy(x, y, board.board, 60, 7, all_sprites_group, enemies)
        empty_cells.remove((x, y))

    # Центр мира в пикселях
    world_center_x = (board.width * CELL_SIZE) // 2
    world_center_y = (board.height * CELL_SIZE) // 2

    # Создаём игрока в центре мира
    player = Player((world_center_x, world_center_y), CELL_SIZE, all_sprites_group)

    menu_screen = pygame.transform.scale(load_image('menu.png'), (50, 50))
    menu_btn = Button(screen, (10, 10), (50, 50), image='empty.png', surface=menu_screen)

    # Кол-во заданных бомб
    bombs = 5

    # Основной цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_btn.connect(main_menu, event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bombs > 0:
                        Bomb(player.rect.center[0] // CELL_SIZE, player.rect.center[1] // CELL_SIZE, CELL_SIZE,
                                    all_sprites_group)
                        bombs -= 1
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        keys = pygame.key.get_pressed()
        check = player.move(keys, walls, exit_maze, enemies)
        # Условие выигрыша
        if check == 1:
            win_screen()
        # Условие проигрыша
        if check == 2:
            lost_screen()

        enemies.update(player.rect.center)

        # Обновление экрана
        camera.update(player)
        enemies.update(player.rect.center)

        screen.fill((0, 0, 0))  # Заливка фона

        for sprite in all_sprites_group:
            if isinstance(sprite, Bomb):
                board.board, enemies, updated_cells = sprite.explosion(board.board, enemies, walls)
                if updated_cells:
                    create_walls(board.board, updated_cells)
            screen.blit(sprite.image, camera.apply(sprite))
        menu_btn.render()
        Text(font_size=50, color=(255, 0, 0)).render(screen, f'Bombs: {bombs}', (60, 10))
        pygame.display.flip()
        clock1.tick(75)


def quit_screen(screen_start) -> None:  # Экран выхода из игры
    scr = fade_in_out(screen, screen_start, fade_in=False, max_alpha=122, speed=3)
    screen.blit(scr, (0, 0))
    no_btn = Button(screen, (526, 540), (384, 100), image='no.jpg', surface=screen)
    yes_btn = Button(screen, (1010, 540), (384, 100), image='yes.jpg', surface=screen)
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


def main_menu():    # Функция главного меню
    pygame.display.set_caption('Разрушитель лабиринтов')
    clock1 = pygame.time.Clock()
    screen.fill((0, 0, 0))
    screen_start = load_image('home_screen.png')
    screen.blit(screen_start, (0, 0))
    button_start = Button(screen, (720, 530), (480, 120), image='new_game.jpg', surface=screen_start)
    button_help = Button(screen, (720, 730), (480, 100), image='options.jpg', surface=screen_start)
    button_exit = Button(screen, (720, 930), (480, 100), image='exit.jpg', surface=screen_start)
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
        clock1.tick(120)
    pygame.quit()


def hash_password(password: str) -> str:    # Хэширование паролей
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(stored_password: str, provided_password: str) -> bool:  # Проверка валидности пароля
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


def registration(): # Окно входа или регистрации
    def enter(login: str, password: str, sign_in: bool):    # Функция для работы с базой данных
        enter_to_play = False
        comments = pygame.Surface((1920, 1080))
        try:
            db = sqlite3.connect(os.path.abspath('main/date base/users'))
            cur = db.cursor()
            if len(login) != 0 and len(password) != 0:
                if sign_in:
                    answer = cur.execute("SELECT * FROM users WHERE user=?", (login,)).fetchall()
                    if len(answer) == 0:
                        Text(font_size=50).render(comments, 'Неверный логин', (500, 700))

                    stored_password = answer[0][1]

                    if verify_password(stored_password, password):
                        enter_to_play = True
                    else:
                        Text(font_size=50).render(comments, 'Неверный пароль', (500, 700))
                else:
                    cur.execute("INSERT INTO users(user, password) VALUES (?, ?)", (login, hash_password(password)))
                    db.commit()
                    Text(font_size=50).render(comments, 'Логин и пароль приняты)', (500, 700))
            elif len(login) != 0:
                Text(font_size=50).render(comments, 'Вы не ввели пароль(', (500, 700))
            elif len(password) != 0:
                Text(font_size=50).render(comments, 'Вы не ввели логин(', (500, 700))
        except Exception as e:
            print(e)
        finally:
            if enter_to_play:
                print(1)
                main_menu()
            enter_screen.blit(comments, (0, 0))
    pygame.display.set_caption('Регистрация')
    clock1 = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    enter_screen = pygame.Surface((1920, 1080))

    login_edit = LineEdit(760, 300, 400, 50, font)

    password_edit = LineEdit(760, 400, 400, 50, font)

    signin_btn = Button(enter_screen, (535, 100), (400, 100), image='sign_in.png', surface=enter_screen)
    new_akk_btn = Button(enter_screen, (985, 100), (400, 100), image='registration.jpg', surface=enter_screen)
    enter_btn = Button(enter_screen, (760, 600), (400, 100), image='enter.png', surface=enter_screen)

    check_mark = pygame.transform.scale(load_image('check_mark.png'), (50, 50))

    signin_flag = True

    running = True
    while running:
        dt = clock1.tick(75)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if signin_btn.get_click(event.pos):
                    signin_flag = True
                if new_akk_btn.get_click(event.pos):
                    signin_flag = False
                enter_btn.connect(enter, event.pos, (login_edit.return_text(), password_edit.return_text(), signin_flag))
            login_edit.handle_event(event)
            password_edit.handle_event(event)

        login_edit.update(dt)
        login_edit.draw(enter_screen)
        password_edit.update(dt)
        password_edit.draw(enter_screen)
        signin_btn.render()
        new_akk_btn.render()
        enter_btn.render()

        Text(font_size=40).render(enter_screen, 'Пароль', (650, 410))
        Text(font_size=40).render(enter_screen, 'Логин', (670, 310))
        screen.blit(enter_screen, (0, 0))

        if not signin_flag:
            screen.blit(check_mark, (1385, 125))
        else:
            screen.blit(check_mark, (485, 125))

        pygame.display.flip()


if __name__ == '__main__':
    registration()
