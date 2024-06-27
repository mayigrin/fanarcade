from tetris import functions
from tetris import interface
from tetris import screens, events
import pygame
from tetris.squares import Squares


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

        self.sqs_list = []
        self.player_statuses = [functions.PlayerStatus() for i in range(self.st.num_players)]

        self.reset_squares()

        game.add_player = self.add_player
        game.remove_player = self.remove_player

    def reset_squares(self):
        self.player_statuses = [functions.PlayerStatus() for i in range(self.st.num_players)]
        self.sqs_list = [Squares(
            self.st,
            self.status,
            self.player_statuses[i],
            screens.get_sqs_surface(self.screen, self.st),
            empty_line=self.empty_line,
            squares=self.squares,
            player=i
        ) for i in range(self.st.num_players)]

    def add_player(self, joystick_id):
        player_status = functions.PlayerStatus()
        self.sqs_list.append(Squares(
                        self.st,
                        self.status,
                        player_status,
                        screens.get_sqs_surface(self.screen, self.st),
                        empty_line=self.empty_line,
                        squares=self.squares,
                        player=joystick_id
                    ))
        self.player_statuses.append(player_status)
        self.players.append(joystick_id)

    def remove_player(self, index):
        self.sqs_list.pop(index)
        self.player_statuses.pop(index)

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
        updated = False
        for i in range(len(self.sqs_list)):
            sqs = self.sqs_list[i]
            sqs.update()
            screens.update_screen(self.screen, sqs, self.func, self.status, self.st, draw_shared_squares=(i == 0))
