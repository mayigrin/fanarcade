import pygame

class Settings:
    def __init__(self):
        self.keyboard_mode = False
        self.num_players = 0

        self.add_ball = 10
        self.brick_color_names = ['red', 'green', 'blue', 'yellow', 'purple', 'cyan']

        # times or speed, in seconds, you can adjust this if youre not satisfied by the default
        self.time_drop = 0.8  # period to force drop
        self.time_drop_adjust = 0.99 # every score up, decrease drop time by this factor
        self.time_stop = 0.5 # time player can adjust pos at bottom
        self.time_move = 0.1 # minimum time interval to move
        self.time_rotate = 0.2 # minimum time interval to rotate
        self.time_to_quick = 0.3 # time interval to activate quick move mode
        self.time_before_drop = 0.3 # time to wait from one stop to drop
        self.time_quick_drop = 0.01 # minimum time interval to drop in quick mode
        self.time_move_quick = 0.05 # minimum time interval to move in quick mode
        self.time_to_straight_drop = 0.3 # time to do another down straight

        # colors, you can change it to be an artist
        self.brick_color_names = ['red', 'green', 'blue', 'yellow', 'purple', 'cyan']
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red'  : (255, 0, 0),
            'green': (0, 255, 0),
            'blue' : (0, 0, 255),
            'yellow': (255, 255, 0),
            'purple': (255, 0, 255),
            'cyan' : (0, 255, 255),

            'none' : (45, 45, 45),    # dark grey
            'tip'  : (100, 100, 100)  # grey
        }

        self.bg_color = (30, 30, 30) # black
        self.square_color = (245, 245, 245) # white
        self.space_color = (35, 35, 35) # slightly lighter than bg

        # shapes, dont touch this if you are not clear what this dose
        self.paddle = (
            {'pos':([0, 1], [0, 2], [0, -1]), 'color':'white', 'rotate':2} # |
        )

        # positions
        self.square_length = 5
        self.square_num_x = 100
        self.square_num_y = 36
        self.square_space = 0
        # self.square_length = 1
        # self.square_num_x = 1000
        # self.square_num_y = 360
        # self.square_space = 0
        self.new = [int(self.square_num_y/2), int(self.square_num_x/2)]    # upper center

        # surfaces
        self.func_width = 200
        self.game_size = self.get_game_size(self)
        self.func_size = self.get_func_size(self)
        self.screen_size = self.get_screen_size(self)
        self.screen_name = "Pong"

        # texts
        self.text_margin = 30
        self.text_adjust_factor = 1
        self.score = "Score: "
        self.score_font = "Comic Sans MS"
        self.score_size = 25
        self.score_color = (255, 255, 255) # white

        self.start_font = "Comic Sans MS"
        self.start_size = 100
        self.start_color = (0, 255, 0) # green
        self.start_pos = "center"
        self.start_surface = self.adjust_start_size(self)

        self.game_over = "   Press any key to play again   "
        self.game_over_font = self.start_font
        self.game_over_size = self.start_size
        self.game_over_color = (255, 0, 0) # red
        self.game_over_pos = "center"
        self.game_over_surface = self.adjust_game_over_size(self)

        self.COLOR_MULTIPLIER = 50
        self.COLOR_OFFSET = 10

    def get_score_pos(self):
        return [self.screen_size[0] * 80/500, self.screen_size[1] * 150/180]

    def adjust_for_AI(self):
        self.time_drop = 0  # period to force drop
        self.time_drop_adjust = 0 # every score up, decrease drop time by this factor
        self.time_stop = 0 # time player can adjust pos at bottom
        self.time_move = 0 # minimum time interval to move
        self.time_rotate = 0 # minimum time interval to rotate
        self.time_before_drop = 0 # time to wait from one stop to drop
        self.time_quick_drop = 0 # minimum time interval to drop in quick mode
        self.time_move_quick = 0 # minimum time interval to move in quick mode
        self.screen_name = 'Tetris: AI playing...'

    def get_player_color(self, player):
        if player == 0:
            return 'red'
        elif player == 1:
            return 'blue'
        elif player == 2:
            return 'yellow'
        elif player == 3:
            return 'green'
        else:
            return 'purple'

    @staticmethod
    def get_game_size(self):
        x = ((self.square_length + self.square_space)\
            * self.square_num_x) + self.square_space
        y = ((self.square_length + self.square_space)\
            * self.square_num_y) + self.square_space
        return (x, y)

    @staticmethod
    def get_func_size(self):
        x = self.func_width
        y = self.game_size[1]
        return (x, y)

    @staticmethod
    def get_screen_size(self):
        x = self.game_size[0]
        y = self.game_size[1]
        return (x, y)

    @staticmethod
    def adjust_start_size(self):
        adjust = True  # at least calculate surface once
        start = ["Press X to connect controller", "Press B to start", f"{self.num_players} players connected"]
        for line in start:
            while adjust:
                font = pygame.font.SysFont(self.start_font, self.start_size)
                surface = font.render(line, True, self.start_color)
                # adjust font if it is too big
                adjust = ((surface.get_width() + 2 * self.text_margin) > self.screen_size[0])
                if adjust:
                    self.start_size -= self.text_adjust_factor
                else:
                    break

        return [font.render(line, True, self.start_color) for line in start]

    @staticmethod
    def adjust_game_over_size(self):
        adjust = True  # at least calculate surface once
        while adjust:
            font = pygame.font.SysFont(self.game_over_font, self.game_over_size)
            surface = font.render(self.game_over, True, self.game_over_color)
            # adjust font if it is too big
            adjust = ((surface.get_width() + 2 * self.text_margin) > self.screen_size[0])
            if adjust:
                self.game_over_size -= self.text_adjust_factor
            else:
                return surface

