import pygame

def start(screen, st):
    num_lines = len(st.start_surface)
    for i in range(num_lines):
        surface = st.start_surface[i]
        if st.start_pos == "center":
            x, y = get_center_pos(screen, surface)
        else:
            x, y = st.start_pos
        multiplier = i - num_lines/2
        y += (multiplier * st.start_size) + (15 * i)
        screen.blit(surface, (x, y))

def game_over(screen, st):
    num_lines = len(st.game_over_surface)
    for i in range(num_lines):
        surface = st.game_over_surface[i]
        if st.game_over_pos == "center":
            x, y = get_center_pos(screen, surface)
        else:
            x, y = st.game_over_pos
        multiplier = i - num_lines / 2
        y += (multiplier * st.game_over_size) + (15 * i)
        screen.blit(surface, (x, y))

def get_center_pos(screen, text):
    screen_rect = screen.get_rect()
    text_rect = text.get_rect()
    text_rect.centerx = screen_rect.centerx
    text_rect.centery = screen_rect.centery
    return (text_rect.x, text_rect.y)
