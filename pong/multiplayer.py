from pong import functions
from pong import interface
from pong import screens, events
import pygame
from pong.squares import Squares, Ball


class Multiplayer:
    """method for handling multiplayer mode"""

    def __init__(self, st, status, screen, func):
        self.st = st
        self.status = status
        self.screen = screen
        self.func = func
        self.empty_line = ['none' for i in range(st.square_num_x)]
        self.squares = [self.empty_line.copy() for i in range(st.square_num_y)]

        self.ball = Ball(self.st, self.status, self.screen, self.squares)

        self.joysticks = {}
        self.players = []
        self.sqs_list = []
        self.player_statuses = [functions.PlayerStatus() for i in range(self.st.num_players)]

        self.reset_squares()

    def reset_squares(self):
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
        self.ball = Ball(self.st, self.status, self.screen, self.sqs_list, controller=self)

    def add_player(self, joystick_id):
        self.st.num_players += 1
        player_n = len(self.sqs_list)
        player_status = functions.PlayerStatus()
        self.sqs_list.append(Squares(
                        self.st,
                        self.status,
                        player_status,
                        screens.get_sqs_surface(self.screen, self.st),
                        empty_line=self.empty_line,
                        squares=self.squares,
                        player=player_n,
                        controller = self
        ))
        self.player_statuses.append(player_status)
        self.players.append(joystick_id)

    def set_starting_positions(self):
        num_ticks = self.st.num_players // 2 + 1
        for i in range(len(self.sqs_list)):
            sqs = self.sqs_list[i]
            tick = i // 2 + 1
            sqs.curr_sq[1] = int(tick * self.st.square_num_x / num_ticks)

    def check_events(self):
        # listen to every event and respond
        for event in pygame.event.get():
            # Handle joystick input
            if hasattr(event, "instance_id") and event.instance_id in self.joysticks:
                joystick = self.joysticks[event.instance_id]

                if event.instance_id not in self.players:
                    if self.status.is_game_new() and events.x_button_pressed(joystick):
                        self.add_player(event.instance_id)
                        self.st.start_surface = self.st.adjust_start_size(self.st)
                        interface.start(self.screen, self.st)
                        continue
                else:
                    index = self.players.index(event.instance_id)
                    sqs = self.sqs_list[index]
                    player_status = self.player_statuses[index]
                    events.check_joystick(sqs, joystick, self.status, player_status)

            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                events.key_down(event.key, None, self.status, None)
            if event.type == pygame.KEYUP:
                events.key_up(event.key, None)

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy

            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]

    def update(self):
        for i in range(len(self.sqs_list)):
            sqs = self.sqs_list[i]
            sqs.update()
            screens.update_screen(self.screen, sqs, self.func, self.status, self.st, draw_shared_squares=(i == 0))

        self.ball.update()
        screens.update_screen(self.screen, self.ball, self.func, self.status, self.st, draw_shared_squares=False)
