"""Основной файл, запускающий игру."""
# Импорт библиотек
import pygame
import sys
# Импорт созданных классов и функций
from main.logic.button import Button
from main.logic.text import Text
from time import sleep
from main.logic.fade_in_out import fade_in_out


screen = pygame.display.set_mode((1920, 1080))


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
        pygame.display.update()


def play() -> None:
    screen.fill((0, 0, 0))
    Text(font_size=100, color=(255, 255, 255)).render(screen, 'Пока идет разработка(((', (960, 100), True)
    btn_return = Button(screen, (720, 300), (480, 50), text='Назад', text_color=(255, 255, 255))
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
        pygame.display.update()


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


def Main():
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
    pygame.quit()


if __name__ == '__main__':
    Main()
