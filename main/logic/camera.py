class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0
        self.offset_y = 0

    def apply(self, target):
        return target.rect.move(self.offset_x, self.offset_y)

    def update(self, target):
        # Центрируем камеру на игроке
        self.offset_x = -target.rect.centerx + self.screen_width // 2
        self.offset_y = -target.rect.centery + self.screen_height // 2

        # Ограничиваем камеру границами игрового мира
        self.offset_x = min(0, max(self.offset_x, -(self.world_width - self.screen_width)))
        self.offset_y = min(0, max(self.offset_y, -(self.world_height - self.screen_height)))