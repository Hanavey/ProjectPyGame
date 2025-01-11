import pygame

class LineEdit:
    def __init__(self, x, y, width, height, font, text_color=(0, 0, 0), bg_color=(255, 255, 255), border_color=(0, 0, 0), border_width=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.text = ""
        self.active = False  # Поле ввода активно или нет
        self.cursor_visible = True
        self.cursor_timer = 0
        self.backspace_held = False  # Зажат ли Backspace
        self.backspace_timer = 0  # Таймер для контроля удаления
        self.initial_hold_time = 500  # Время ожидания (мс) перед началом ускоренного удаления
        self.repeat_interval = 50  # Интервал между удалениями при ускорении (мс)

    def handle_event(self, event):  # Добавление текста в переменную text
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_held = True
                self.text = self.text[:-1]
                self.backspace_timer = 0
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                self.text += event.unicode

        if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
            self.backspace_held = False
            self.backspace_timer = 0

    def update(self, dt):   # Логика обновления
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 500:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = False

        if self.backspace_held:
            self.backspace_timer += dt
            if self.backspace_timer >= self.initial_hold_time:
                if (self.backspace_timer - self.initial_hold_time) % self.repeat_interval < dt:
                    self.text = self.text[:-1]

    def draw(self, screen): # Метод вывода на экран
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + text_surface.get_width()
            cursor_y = self.rect.y + 5
            cursor_height = self.rect.height - 10
            pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

    def return_text(self):
        return self.text
