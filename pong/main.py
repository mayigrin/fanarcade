import pygame
from pong import screens, functions, interface
from pong.multiplayer import Multiplayer
from settings import Settings

def play_pong():
    pass

def game_start():
    # initialisations
    pygame.init()
    pygame.joystick.init()

    status = functions.Status()
    st = Settings()

    screen = pygame.display.set_mode(st.screen_size)
    pygame.display.set_caption(st.screen_name)

    func = functions.Functions(st, screens.get_func_surface(screen, st))

    controller = Multiplayer(st, status, screen, func)
    status.game_status = status.NEWSTART

    # main loop
    while True:

        pygame.display.flip()
        controller.check_events()

        if status.is_game_active():
            controller.update()
        elif status.is_game_over():
            interface.game_over(screen, st)
        elif status.is_game_new():
            interface.start(screen, st)
        elif status.is_game_renew():
            status.refresh()
            status.game_status = status.ACTIVE

            controller.reset_squares()
            controller.set_starting_positions()

            st = Settings()
        else:
            raise RuntimeError # this should never happen


if __name__ == "__main__":
    game_start()
