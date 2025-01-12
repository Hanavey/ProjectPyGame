class Camera:
    """Класс камеры"""
    def __init__(self, world_width: int, world_height: int, screen_width: int, screen_height: int):
        self.world_width = world_width  # Ширина игрового мира
        self.world_height = world_height    # Длина игрового мира
        self.screen_width = screen_width    # Ширина экрана
        self.screen_height = screen_height  # Длина экрана
        self.offset_x = 0   # Центр по оси X
        self.offset_y = 0   # Центр по оси Y

    def apply(self, target):
        return target.rect.move(self.offset_x, self.offset_y)   # Смещенный rect объект

    def update(self, target):
        # Центрируем камеру на игроке
        self.offset_x = -target.rect.centerx + self.screen_width // 2
        self.offset_y = -target.rect.centery + self.screen_height // 2

        # Ограничиваем камеру границами игрового мира
        self.offset_x = min(0, max(self.offset_x, -(self.world_width - self.screen_width)))
        self.offset_y = min(0, max(self.offset_y, -(self.world_height - self.screen_height)))