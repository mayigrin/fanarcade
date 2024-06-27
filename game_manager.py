from time import process_time

import pygame
from pygame import Rect, draw

from breakout.main import play_breakout
from pong.main import play_pong
from tetris.main import play_ai_tetris, play_tetris

JOYSTICK_THRESHOLD = .5


class GameManager:
    EXIT = False

    def __init__(self, st, screen):
        self.st = st
        self.screen = screen

        self.joysticks = {}
        self.players = []

        # options are menu, tetris, pong, breakout
        self.current_game = "menu"

        self.games = ["tetris", "pong", "breakout"]
        self.selected = 0

        self.last_awake = process_time()
        self.time_to_screen_saver = process_time()

        self.add_player = None
        self.remove_player = None

    def switch_to_menu(self):
        self.current_game = "menu"
        self.last_awake = process_time()

    def handle_cycle(self):
        self.check_events()

        if GameManager.EXIT:
            self.switch_to_menu()

        current_time = self.time_to_screen_saver

        if self.current_game == "tetris":
            play_tetris()

        elif self.current_game == "pong":
            play_pong()

        elif self.current_game == "breakout":
            play_breakout()

        elif current_time - self.last_awake > self.time_to_screen_saver:
            play_ai_tetris()

        else:
            self.show_menu()

    def show_menu(self):
        self.screen.fill(self.st.bg_color)
        for i in range(0,  len(self.games)):
            text = self.games[i]
            self.render_menu_button(i, text)

        self.render_player_count()

    def render_menu_button(self, i, text):
        x_multiplier = (i + 1) / (len(self.games) + 2)
        x_pos = x_multiplier * self.st.screen_size[0]
        y_mid = self.st.screen_size[0] // 2
        font = pygame.font.SysFont(self.st.menu_font, self.st.menu_size)
        surface = font.render(text, True, self.st.menu_color)
        surface = pygame.transform.rotate(surface, 90)
        y_pos = y_mid - surface.get_height()
        rect = Rect(
            x_pos,
            y_pos,
            surface.get_width(),
            surface.get_height()
        )
        draw.rect(
            self.screen,
            self.st.selected_button_color if self.selected == i else self.st.unselected_button_color,
            rect
        )
        self.screen.blit(surface, (x_pos, y_pos))

    def render_player_count(self):
        x_multiplier = (len(self.games) + 1) / (len(self.games) + 2)
        x_pos = x_multiplier * self.st.screen_size[0]
        font = pygame.font.SysFont(self.st.menu_font, self.st.menu_size)
        y_mid = self.st.screen_size[0] // 2
        text = f"{self.st.num_players} players connected"
        surface = font.render(text, True, self.st.menu_color)
        surface = pygame.transform.rotate(surface, 90)
        y_pos = y_mid - surface.get_height()
        self.screen.blit(surface, (x_pos, y_pos))

    def player_join(self, pid):
        self.players.append(pid)
        if self.add_player:
            self.add_player()

    def player_leave(self, pid):
        self.players.remove(pid)
        if self.remove_player:
            self.remove_player()

    def check_events(self):
        # listen to every event and respond
        for event in pygame.event.get():
            # Handle joystick input
            if hasattr(event, "instance_id") and event.instance_id in self.joysticks:
                joystick = self.joysticks[event.instance_id]

                # Press start on joycon
                if joystick.get_button(6) > JOYSTICK_THRESHOLD:
                    # If player not registered, register
                    if event.instance_id not in self.players:
                        self.player_join(event.instance_id)
                    # If registered, remove
                    else:
                        self.player_leave(event.instance_id)

                # Press select on joycon
                if joystick.get_button(5) > JOYSTICK_THRESHOLD:
                    GameManager.EXIT = True

                # Press up on joycon
                if joystick.get_axis(1) < -JOYSTICK_THRESHOLD:
                    self.selected = (self.selected - 1) % len(self.games)

                # Press down on joycon
                if joystick.get_axis(1) > JOYSTICK_THRESHOLD:
                    self.selected = (self.selected + 1) % len(self.games)

            if event.type == pygame.QUIT:
                exit()

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                self.player_join(joy.get_instance_id())

            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]
                self.player_leave(event.instance_id)



