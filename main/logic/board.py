# Импорт библиотек
import pygame
import numpy as np
import random


class Board:    # клетчатое поле
    """Класс для клетчатого поля."""
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # self.board = np.random.randint(0, 2, (height, width), dtype=np.uint8)
        self.board = self.generate_maze()
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen: pygame.display) -> None:   # Метод отрисовки
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def set_view(self, left: int, top: int, cell_size: int) -> None:    # Метод изменения размеров и размещения поля
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos: tuple[int, int]) -> tuple[int, int] or None:  # Метод считающий координаты нажатой клетки
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos: tuple[int, int]) -> tuple[int, int] or None: # Метод возвращающий координаты нажатой клетки
        cell = self.get_cell(mouse_pos)
        self.board[cell[1]][cell[0]] = 1 if self.board[cell[1]][cell[0]] == 0 else 0
        return cell

    def generate_maze(self) -> list:
        # Убедимся, что размеры нечётные
        if self.width % 2 == 0:
            self.width -= 1
        if self.height % 2 == 0:
            self.height -= 1

        # Инициализация: всё поле — стены
        maze = np.ones((self.height, self.width), dtype=int)

        # Размер центральной комнаты
        room_size = 3  # Нечётное число для корректной интеграции
        room_x1 = (self.width - room_size) // 2
        room_y1 = (self.height - room_size) // 2
        room_x2 = room_x1 + room_size
        room_y2 = room_y1 + room_size

        # Очищаем область центральной комнаты
        maze[room_y1:room_y2, room_x1:room_x2] = 0

        # Рекурсивная генерация лабиринта
        def carve(x: int, y: int):
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]  # Сдвиги: вверх, вправо, вниз, влево
            random.shuffle(directions)  # Случайный порядок направлений

            for dx, dy in directions:
                nx, ny = x + dx, y + dy  # Новая клетка
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:  # Проверка на границы
                    if maze[ny, nx] == 1:  # Если клетка — стена
                        # Проверяем, не пересекаем ли центральную комнату
                        if not (room_x1 <= nx < room_x2 and room_y1 <= ny < room_y2):
                            maze[ny, nx] = 0  # Создаём проход
                            maze[ny - dy // 2, nx - dx // 2] = 0  # Убираем стену между клетками
                            carve(nx, ny)  # Рекурсивно идём дальше

        # Начальная точка (гарантированно нечётная)
        start_x, start_y = 1, 1
        maze[start_y, start_x] = 0  # Создаём первый проход

        # Запускаем генерацию
        carve(start_x, start_y)

        # Создаём путь из центральной комнаты в лабиринт
        room_exit_x = random.choice(range(room_x1, room_x2, 2))
        room_exit_y = random.choice(range(room_y1, room_y2, 2))
        maze[room_exit_y, room_exit_x] = 0

        # Соединяем комнату с лабиринтом
        if room_exit_x == room_x1:
            maze[room_exit_y, room_exit_x - 1] = 0
        elif room_exit_x == room_x2 - 1:
            maze[room_exit_y, room_exit_x + 1] = 0
        elif room_exit_y == room_y1:
            maze[room_exit_y - 1, room_exit_x] = 0
        elif room_exit_y == room_y2 - 1:
            maze[room_exit_y + 1, room_exit_x] = 0

        # Добавляем выход из лабиринта
        exit_x, exit_y = random.choice(
            [(0, random.randint(1, self.height - 2)), (self.width - 1, random.randint(1, self.height - 2)),
             (random.randint(1, self.width - 2), 0), (random.randint(1, self.width - 2), self.height - 1)])
        maze[exit_y, exit_x] = 3

        # Гарантируем соединение выхода с лабиринтом
        if maze[exit_y, exit_x] == 3 and maze[exit_y - 1:exit_y + 2, exit_x - 1:exit_x + 2].all():
            # Если вокруг только стены, прорубаем путь
            if exit_x == 0:
                maze[exit_y, exit_x + 1] = 0
            elif exit_x == self.width - 1:
                maze[exit_y, exit_x - 1] = 0
            elif exit_y == 0:
                maze[exit_y + 1, exit_x] = 0
            elif exit_y == self.height - 1:
                maze[exit_y - 1, exit_x] = 0

        return maze
