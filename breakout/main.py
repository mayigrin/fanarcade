import requirements
import pygame
from breakout import functions, interface
from breakout.multiplayer import Multiplayer
from settings import Settings


def play_breakout(game):
    # initialisations
    pygame.init()
    pygame.joystick.init()

    status = functions.Status()
    pygame.display.set_caption(game.st.screen_name)

    func = functions.Functions(game.st, game.screen)

    controller = Multiplayer(game, status, func)
    status.game_status = status.ACTIVE

    # main loop
    while not game.EXIT:

        pygame.display.flip()
        controller.check_events()

        if status.is_game_active():
            controller.update()
        elif status.is_game_over():
            interface.game_over(game.screen, game.st)
        elif status.is_game_renew():
            status.refresh()
            status.game_status = status.ACTIVE

            controller.reset_squares()
            controller.set_starting_positions()

            game.st = Settings()
        else:
            raise RuntimeError # this should never happen

