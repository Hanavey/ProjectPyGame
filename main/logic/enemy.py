from main.logic.load_images import load_image

class Enemy:
    def __init__(self, maze):
        self.image = load_image('enemy.png')
        self.x = 0
        self.y = 0
        self.maze = maze
        self.dir = 'down'  # Начальное направление

    def move(self):
        # Определение следующего направления в зависимости от текущего направления и положения стен
        if self.dir == 'down':
            if self.can_move('right'):
                self.dir = 'right'
            elif self.can_move('down'):
                self.y += 1
            else:
                self.dir = 'left'
        elif self.dir == 'right':
            if self.can_move('up'):
                self.dir = 'up'
            elif self.can_move('right'):
                self.x += 1
            else:
                self.dir = 'down'
        elif self.dir == 'up':
            if self.can_move('left'):
                self.dir = 'left'
            elif self.can_move('up'):
                self.y -= 1
            else:
                self.dir = 'right'
        elif self.dir == 'left':
            if self.can_move('down'):
                self.dir = 'down'
            elif self.can_move('left'):
                self.x -= 1
            else:
                self.dir = 'up'

    def can_move(self, dir):
        # Проверка возможности перемещения в заданном направлении
        if dir == 'up':
            return self.maze[self.y - 1][self.x] != 1
        elif dir == 'down':
            return self.maze[self.y + 1][self.x] != 1
        elif dir == 'left':
            return self.maze[self.y][self.x - 1] != 1
        elif dir == 'right':
            return self.maze[self.y][self.x + 1] != 1