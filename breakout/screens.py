import pygame

def update_screen(screen, sqs, func, status, st, draw_shared_squares=False):
    """draw one screen"""
    sqs.draw_squares(draw_shared_squares=draw_shared_squares)
    if draw_shared_squares:
        func.show_score(status.score)

def get_sqs_surface(screen, st):
    sqs_rect =  pygame.Rect(0, 0, st.game_size[0], st.game_size[1])
    return screen.subsurface(sqs_rect)
