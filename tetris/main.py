import requirements
import pygame
import sys
import functions, interface
from keyboard import Keyboard
from multiplayer import Multiplayer
from settings import Settings
import AI_player

def play_tetris():
    pass

def play_ai_tetris():
    pass

def game_start():
    # initialisations
    pygame.init()
    pygame.joystick.init()

    status = functions.Status()
    st = Settings()

    if "--AI" in sys.argv:
        st.keyboard_mode = True
        status.AI = True
    if "--keyboard" in sys.argv:
        st.keyboard_mode = True

    screen = pygame.display.set_mode(st.screen_size)
    pygame.display.set_caption(st.screen_name)

    func = functions.Fucntions(st, screen)

    AI = AI_player.AI()

    if st.keyboard_mode:
        controller = Keyboard(st, status, screen, func, AI)
        status.game_status = status.ACTIVE
    else:
        controller = Multiplayer(st, status, screen, func, AI)

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
            AI_mode = status.newAI
            status.refresh()
            status.game_status = status.ACTIVE

            controller.reset_squares()

            st = Settings()
            if AI_mode:
                status.AI = True
                controller.adjust_for_AI()
        else:
            raise RuntimeError # this should never happen


if __name__ == "__main__":
    requirements.check()
    game_start()
