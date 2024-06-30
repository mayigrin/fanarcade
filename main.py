import requirements
import pygame

from game_manager import GameManager
from settings import Settings

FAN_SCREEN_SIZE = [1280, 720]
ORIGIN = [140, 180]

def game_start():
    # initialisations
    pygame.init()
    pygame.joystick.init()

    st = Settings()

    screen = pygame.display.set_mode(FAN_SCREEN_SIZE)
    screen.fill((0,0,0))

    sqs_rect = pygame.Rect(*ORIGIN, st.game_size[0], st.game_size[1])
    game_screen = screen.subsurface(sqs_rect)

    pygame.display.set_caption(st.screen_name)

    game_manager = GameManager(st, game_screen)

    # main loop
    while True:

        pygame.display.flip()
        game_manager.handle_cycle()


if __name__ == "__main__":
    requirements.check()
    try:
        game_start()
    except Exception as e:
        print(e)
        print("restarting")
        game_start()

