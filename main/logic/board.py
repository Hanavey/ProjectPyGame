"""Класс для клетчатого поля."""
# Импорт библиотек
import pygame
import numpy as np


class Board:    # клетчатое поле
    def __init__(self, width: int, height: int) -> None:
        # кол-во клеток по горизонтали и вертикали
        self.width = width
        self.height = height
        # основной список доски
        self.board = np.zeros((height, width), dtype=np.uint8)
        # размещение и размер поля
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
