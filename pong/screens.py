import pygame


def update_screen(screen, sqs, st, draw_shared_squares=False):
    """draw one screen"""
    sqs.draw_squares(draw_shared_squares=draw_shared_squares)


def get_sqs_surface(screen, st):
    sqs_rect =  pygame.Rect(0, 0, st.game_size[0], st.game_size[1])
    return screen.subsurface(sqs_rect)


def get_func_surface(screen, st):
    func_surface = pygame.Rect(st.game_size[0] - st.func_size[0], 0, st.func_size[0], st.func_size[1])
    return screen.subsurface(func_surface)
