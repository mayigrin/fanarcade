from tetris import functions
from tetris import screens, events
import pygame

from tetris.squares import Squares

class Keyboard:
    """method for handling single player keyboard mode"""

    def __init__(self, st, status, screen, func, AI):
        self.st = st
        self.status = status
        self.screen = screen
        self.func = func
        self.AI = AI
        self.empty_line = ['none' for i in range(st.square_num_x)]
        self.squares = [self.empty_line.copy() for i in range(st.square_num_y)]

        self.joysticks = {}
        self.player_status = functions.PlayerStatus()
        self.sqs = None
        self.joystick = None

        self.reset_squares()

    def reset_squares(self):
        self.sqs = Squares(
            self.st,
            self.status,
            self.player_status,
            screens.get_sqs_surface(self.screen, self.st),
            empty_line=self.empty_line,
            squares=self.squares
        )

    def check_events(self):
        # listen to every event and respond
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                events.key_down(event.key, self.sqs, self.status, self.player_status)
            if event.type == pygame.KEYUP:
                events.key_up(event.key, self.player_status)

        if self.status.is_AI():
            self.AI.control(self.sqs, self.player_status)

    def update(self):
        if self.sqs.update():
            screens.update_screen(self.screen, self.sqs, self.func, self.status, self.st, draw_shared_squares=True)

    def adjust_for_AI(self):
        self.sqs.st.adjust_for_AI()