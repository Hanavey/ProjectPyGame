"""Класс для клетчатого поля."""
# Импорт библиотек
import pygame
import numpy as np
import random


class Board:    # клетчатое поле
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

    def generate_maze(self):
        if self.width % 2 == 0:
            self.width -= 1
        if self.height % 2 == 0:
            self.height -= 1

        # Инициализация: всё поле — стены
        maze = np.ones((self.height, self.width), dtype=int)

        # Рекурсивная генерация лабиринта
        def carve(x, y):
            """
            Рекурсивно создаёт лабиринт начиная с точки (x, y).
            """
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]  # Сдвиги: вверх, вправо, вниз, влево
            random.shuffle(directions)  # Случайный порядок направлений

            for dx, dy in directions:
                nx, ny = x + dx, y + dy  # Новая клетка
                if nx > 0 and nx < self.width - 1 and ny > 0 and ny < self.height - 1:  # Проверка на границы
                    if maze[ny, nx] == 1:  # Если клетка — стена
                        maze[ny, nx] = 0  # Создаём проход
                        maze[ny - dy // 2, nx - dx // 2] = 0  # Убираем стену между клетками
                        carve(nx, ny)  # Рекурсивно идём дальше

        # Начальная точка (гарантированно нечётная)
        start_x, start_y = 1, 1
        maze[start_y, start_x] = 0  # Создаём первый проход

        # Запускаем генерацию
        carve(start_x, start_y)

        exit_x, exit_y = random.choice(
            [(0, random.randint(1, self.height - 2)), (self.width - 1, random.randint(1, self.height - 2)),
             (random.randint(1, self.width - 2), 0), (random.randint(1, self.width - 2), self.height - 1)])

        maze[exit_y, exit_x] = 0

        return maze
