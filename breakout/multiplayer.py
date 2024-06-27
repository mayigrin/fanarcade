from breakout import functions
import random
from breakout import screens, events
import pygame
from breakout.squares import Squares, Ball


class Multiplayer:
    """method for handling multiplayer mode"""

    def __init__(self, game, status, func):
        self.game = game
        self.st = game.st
        self.screen = game.screen
        self.joysticks = game.joysticks
        self.players = game.players

        self.status = status
        self.func = func
        self.empty_line = ['none' for i in range(game.st.square_num_x)]
        self.squares = [self.empty_line.copy() for i in range(game.st.square_num_y)]

        self.balls = []

        self.sqs_list = []
        self.player_statuses = [functions.PlayerStatus() for i in range(self.st.num_players)]

        self.reset_squares()

        game.add_player = self.add_player
        game.remove_player = self.remove_player

    def setup_bricks(self):
        for y in range(4, self.st.square_num_y//2):
            for x in range(0, self.st.square_num_x):
                self.squares[y][x] = random.choice(self.st.brick_color_names) if x % 10 < 6 else 'none'

    def reset_squares(self):
        self.setup_bricks()
        self.player_statuses = [functions.PlayerStatus() for i in range(self.st.num_players)]
        self.sqs_list = [Squares(
            self.st,
            self.status,
            self.player_statuses[i],
            screens.get_sqs_surface(self.screen, self.st),
            empty_line=self.empty_line,
            squares=self.squares,
            player=i,
            controller=self
        ) for i in range(self.st.num_players)]
        self.balls = [Ball(self.st, self.status, self.screen, self.sqs_list, self.squares, controller=self)]
        self.set_starting_positions()

    def add_ball(self):
        self.balls.append(Ball(self.st, self.status, self.screen, self.sqs_list, self.squares, controller=self))

    def add_player(self, joystick_id):
        player_status = functions.PlayerStatus()
        self.sqs_list.append(Squares(
                        self.st,
                        self.status,
                        player_status,
                        screens.get_sqs_surface(self.screen, self.st),
                        empty_line=self.empty_line,
                        squares=self.squares,
                        player=joystick_id,
                        controller=self
        ))
        self.player_statuses.append(player_status)

    def remove_player(self, index):
        self.sqs_list.pop(index)
        self.player_statuses.pop(index)

    def set_starting_positions(self):
        num_ticks = self.st.num_players + 1
        for i in range(len(self.sqs_list)):
            sqs = self.sqs_list[i]
            tick = i + 1
            sqs.curr_sq[1] = int(tick * self.st.square_num_x / num_ticks)

    def check_events(self):
        # listen to every event and respond
        for event in pygame.event.get():
            self.game.check_event(event)
            # Handle joystick input
            if hasattr(event, "instance_id") and event.instance_id in self.joysticks:
                joystick = self.joysticks[event.instance_id]

                if event.instance_id in self.players:
                    index = self.players.index(event.instance_id)
                    sqs = self.sqs_list[index]
                    player_status = self.player_statuses[index]
                    events.check_joystick(sqs, joystick, self.status, player_status)

    def update(self):
        # update positions
        for sqs in self.sqs_list:
            sqs.update()
        for ball in self.balls:
            ball.update()

        # update screen
        for i in range(len(self.balls)):
            ball = self.balls[i]
            screens.update_screen(self.screen, ball, self.func, self.status, self.st, draw_shared_squares=(i == 0))
        for i in range(len(self.sqs_list)):
            sqs = self.sqs_list[i]
            screens.update_screen(self.screen, sqs, self.func, self.status, self.st)
