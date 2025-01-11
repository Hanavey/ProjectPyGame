from main.logic.load_images import load_image
import pygame
from queue import PriorityQueue


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, maze, tile_size, R, *groups):
        super().__init__(*groups)  # Инициализация родительского класса Sprite
        self.x = x
        self.y = y
        self.maze = maze  # Двумерный список, где 0 - проходимая клетка, 1 - стена
        self.tile_size = tile_size  # Размер одной клетки
        self.image = load_image('enemy.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))  # Масштабирование
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))  # Прямоугольник для позиционирования
        self.speed = 2
        self.field_of_view = tile_size * R  # Радиус обзора врага в пикселях
        self.path = []

        self.move_delay = 500  # Интервал движения в миллисекундах
        self.last_move_time = pygame.time.get_ticks()

    def update(self, player_pos):
        player_tile = (player_pos[0] // self.tile_size, player_pos[1] // self.tile_size)
        if self.in_field_of_view(player_pos):
            self.path = self.find_path((self.x, self.y), player_tile)

        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            self.move()
            self.last_move_time = current_time

    def move(self):
        if self.path:
            next_cell = self.path.pop(0)
            self.x, self.y = next_cell
            self.rect.topleft = (self.x * self.tile_size, self.y * self.tile_size)

    def in_field_of_view(self, player_pos):
        player_px, player_py = player_pos
        enemy_px = self.rect.centerx
        enemy_py = self.rect.centery
        distance = ((player_px - enemy_px) ** 2 + (player_py - enemy_py) ** 2) ** 0.5
        return distance <= self.field_of_view

    def find_path(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Манхэттенское расстояние

        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while not open_set.empty():
            _, current = open_set.get()

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    open_set.put((f_score[neighbor], neighbor))

        return []

    def get_neighbors(self, cell):
        x, y = cell
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if len(self.maze[0]) > nx >= 0 == self.maze[ny][nx] and 0 <= ny < len(self.maze):
                neighbors.append((nx, ny))
        return neighbors
