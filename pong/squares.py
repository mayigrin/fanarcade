import random
from pygame import Rect, draw
from pong.clock import Clock

starting_position = 0


class Ball:
    def __init__(self, st, status, screen, sqs_list=None, vx=0, vy=1, controller=None):
        self.st = st
        self.status = status
        self.screen = screen
        self.sqs_list = sqs_list
        self.controller = controller

        self.x = int(self.st.square_num_x/2)
        self.y = int(self.st.square_num_y/2)
        self.vx = vx
        self.vy = vy

        self.clock = Clock(st)

    def draw_squares(self, draw_shared_squares=False):
        color = (255, 255, 255)
        border = False
        y = self.y
        x = self.wrap_x(self.x)

        x_pos = x * (self.st.square_space + self.st.square_length)
        y_pos = y * (self.st.square_space + self.st.square_length)
        length = self.st.square_length
        # adding borders borders
        if border:
            y_pos -= self.st.square_space
            x_pos -= self.st.square_space
            length += 2 * self.st.square_space
        rect = Rect(x_pos + self.st.square_space, y_pos + self.st.square_space, length, length)
        draw.rect(self.screen, color, rect)

    # update squares' information
    def update(self):
        updated = False  # for update screen
        if self.vx != 0 or self.vy != 0:
            updated = True
            if self.clock.is_time_to_move():
                self.x = self.wrap_x(self.x + self.vx)
                self.y += self.vy
                if self.y < 0 or self.y >= self.st.square_num_y:
                    self.status.game_status = self.status.GAMEOVER
                elif not self.valid_sq((self.y, self.x)):
                    self.vy = -1 * self.vy
                    self.vx = random.random() * 2.1 - 1
                    self.status.score += 1
                self.clock.update_move()
        return updated

    def wrap_x(self, x):
        return x % self.st.square_num_x

    def valid_sq(self, sq):
        # check border
        if sq[0] < 0 or sq[0] >= self.st.square_num_y:  # or sq[1] >= self.st.square_num_x or sq[1] < 0:
            return False
        # check crash
        for sqs in self.sqs_list:
            if self.collision(sqs):
                return False
        return True

    def collision(self, sqs):
        # check shape squares
        for sq in sqs.curr_shape:
            x = sq[1] + sqs.curr_sq[1]
            y = sq[0] + sqs.curr_sq[0]
            if x == int(self.wrap_x(self.x)) and y == self.y:
                return True
        # check center square
        return sqs.curr_sq[1] == int(self.wrap_x(self.x)) and sqs.curr_sq[0] == self.y


class Squares:

    """method for malipulating squares in the game"""
    def __init__(self, st, status, player_status, screen, empty_line=None, squares=None, player=None, controller=None):
        self.player = player

        if empty_line is None:
            self.empty_line = ['none' for i in range(st.square_num_x)]
        else:
            self.empty_line = empty_line

        if squares is None:
            self.squares = [self.empty_line.copy() for i in range(st.square_num_y)]
        else:
            self.squares = squares

        self.st = st
        self.status = status
        self.player_status = player_status
        self.screen = screen
        self.clock = Clock(st)
        self.player = player
        self.controller = controller

        self.new_sq()

    # draw all squares
    def draw_squares(self, draw_shared_squares=False):
        self.draw_curr_sq()

    # update squares' information
    def update(self):
        updated = False # for update screen
        # horizontal move
        if self.player_status.right:
            updated = True
            if self.clock.is_time_to_move_quick():
                self.right()
                self.clock.update_move_quick()
        if self.player_status.left:
            updated = True
            if self.clock.is_time_to_move_quick():
                self.left()
                self.clock.update_move_quick()
        return updated

    # renew current square
    def new_sq(self):
        y = 0 if self.player % 2 else self.st.square_num_y - 1
        x = random.randint(0, self.st.square_num_x)

        self.curr_sq = [y, x]
        shape = self.st.paddle
        self.origin_shape = shape['pos']
        self.curr_shape = shape['pos']

        self.curr_color = self.st.get_player_color(self.player)

    def decrement_x(self, x):
        return (x - 1) % self.st.square_num_x

    def increment_x(self, x):
        return (x + 1) % self.st.square_num_x

    def right(self):
        new_sq = self.curr_sq.copy()
        new_sq[1] += 1
        if self.valid(new_sq, self.curr_shape):
            self.curr_sq = self.wrap(new_sq)

    def left(self):
        new_sq = self.curr_sq.copy()
        new_sq[1] -= 1
        if self.valid(new_sq, self.curr_shape):
            self.curr_sq = self.wrap(new_sq)

    def wrap(self, square):
        sq = square.copy()
        sq[1] = sq[1] % self.st.square_num_x
        return sq

    def wrap_x(self, x):
        return x % self.st.square_num_x

    # validate the given center square and shape squires relative to center square
    def valid(self, square, shape):
        # check shape squares
        for sq in shape:
            x = sq[1] + square[1]
            y = sq[0] + square[0]
            if y >= 0 and not (self.valid_sq([y, x])):
                return False
        # check center square
        return self.valid_sq(square)

    def valid_sq(self, sq):
        # check border
        if sq[0] >= self.st.square_num_y:  # or sq[1] >= self.st.square_num_x or sq[1] < 0:
            return False
        # check crash
        return self.squares[sq[0]][self.wrap_x(sq[1])] == 'none'

    def draw_exist_sq(self):
        for y, row in enumerate(self.squares):
            for x, square in enumerate(row):
                color = self.st.colors[self.squares[y][x]]
                self.draw_square(y, x, color)

    def draw_curr_sq(self):
        # draw center
        color = self.st.colors[self.curr_color]
        self.draw_square(self.curr_sq[0], self.curr_sq[1], color)
        # draw shapes
        curr_y, curr_x = self.curr_sq[0], self.curr_sq[1]
        for y, x in self.curr_shape:
            self.draw_square(y + curr_y, x + curr_x, color)

    # draw one single square with given information
    def draw_square(self, y, x_init, color, border=False):
        x = self.wrap_x(x_init)
        x_pos = x * (self.st.square_space + self.st.square_length)
        y_pos = y * (self.st.square_space + self.st.square_length)
        length = self.st.square_length
        # adding borders borders
        if border:
            y_pos -= self.st.square_space
            x_pos -= self.st.square_space
            length += 2 * self.st.square_space
        rect = Rect(x_pos + self.st.square_space, y_pos + self.st.square_space, length, length)
        draw.rect(self.screen, color, rect)