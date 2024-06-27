import requirements
import pygame
import sys
from tetris import functions, AI_player
from tetris.keyboard import Keyboard
from tetris.multiplayer import Multiplayer
from settings import Settings
import interface


def play_tetris(game):
    status = functions.Status()

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

        else:
            raise RuntimeError  # this should never happen

def play_ai_tetris(game):
    status = functions.Status()
    status.AI = True

    status = functions.Status()

    func = functions.Functions(game.st, game.screen)
    AI = AI_player.AI()

    controller = Keyboard(game, status, func, AI)
    status.game_status = status.ACTIVE

    # main loop
    while not game.EXIT:

        pygame.display.flip()
        controller.check_events()

        if status.is_game_active():
            controller.update()
        elif status.is_game_over():
            AI_mode = status.newAI
            status.refresh()
            status.game_status = status.ACTIVE

            controller.reset_squares()

            if AI_mode:
                status.AI = True
                controller.adjust_for_AI()
        else:
            raise RuntimeError  # this should never happen
