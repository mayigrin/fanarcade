import pygame
from snake import functions
from snake.multiplayer import Multiplayer
import interface


def play_snake(game):
    status = functions.Status()

    controller = Multiplayer(game, status)
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
        else:
            raise RuntimeError # this should never happen

