import requirements
import pygame

from game_manager import GameManager
from settings import Settings

def game_start():
    # initialisations
    pygame.init()
    pygame.joystick.init()

    st = Settings()

    screen = pygame.display.set_mode(st.screen_size)
    pygame.display.set_caption(st.screen_name)

    game_manager = GameManager(st, screen)


    # main loop
    while True:

        pygame.display.flip()
        game_manager.handle_cycle()


if __name__ == "__main__":
    requirements.check()
    game_start()
