import pygame


def fade_in_out(screen: pygame.Surface, surface: pygame.Surface, fade_in: bool = True, speed: int = 5, max_alpha: int = 255, min_alpha: int = 0) -> pygame.Surface:
    alpha = max_alpha if fade_in else min_alpha
    step = -speed if fade_in else speed
    fade_screen = pygame.Surface(screen.get_size())

    while min_alpha <= alpha <= max_alpha:
        screen.blit(surface, (0, 0))
        fade_screen = pygame.Surface(screen.get_size())
        fade_screen.set_alpha(alpha)
        fade_screen.fill((0, 0, 0))
        screen.blit(fade_screen, (0, 0))
        alpha += step
        pygame.display.flip()

    return fade_screen
