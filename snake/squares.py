import random
from pygame import Rect, draw
from snake.clock import Clock

starting_position = 0


class Squares:

    """method for malipulating squares in the game"""
    def __init__(self, st, status, player_status, screen, squares=None, player=None, controller=None):
        self.player = player

        self.empty_line = ['none' for i in range(st.square_num_x)]
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
        self.hidden = False

        self.new_sq()

    # draw all squares
    def draw_squares(self, draw_shared_squares=False):
        if draw_shared_squares:
            for y, row in enumerate(self.squares):
                for x, square in enumerate(row):
                    color = self.st.colors[self.squares[y][x]]
                    self.draw_square(y, x, color)
        if not self.hidden:
            self.draw_curr_sq()

    # update squares' information
    def update(self):
        updated = False # for update screen
        # horizontal move
        if self.player_status.right:
            updated = True
            if self.clock.is_time_to_move():
                self.right()
                self.clock.update_move()
        if self.player_status.left:
            updated = True
            if self.clock.is_time_to_move():
                self.left()
                self.clock.update_move()
        if self.player_status.up:
            updated = True
            if self.clock.is_time_to_move():
                self.up()
                self.clock.update_move()
        if self.player_status.down:
            updated = True
            if self.clock.is_time_to_move():
                self.down()
                self.clock.update_move()
        return updated

    def set_initial_pos(self, index, x):
        if index % 2:
            y = 5
            self.player_status.down = True
            self.tail = [[y - 2, x], [y - 1, x]]
        else:
            y = self.st.square_num_y - 1 - 5
            self.player_status.up = True
            self.tail = [[y + 2, x], [y + 1, x]]

        self.curr_sq = [y, x]

    # renew current square
    def new_sq(self):
        x = random.randint(0, self.st.square_num_x)
        y = random.randint(0, self.st.square_num_y)

        self.curr_sq = [y, x]

        self.curr_color = self.st.get_player_color(self.player)

    def decrement_x(self, x):
        return (x - 1) % self.st.square_num_x

    def increment_x(self, x):
        return (x + 1) % self.st.square_num_x

    def finish_move(self, new_sq):
        if self.valid(new_sq):
            self.tail.append(self.curr_sq)
            self.curr_sq = self.wrap(new_sq)
            if not self.eat():
                self.tail.pop(0)
        else:
            print([s.player for s in self.controller.sqs_list])
            active_players = [s for s in self.controller.sqs_list if not s.hidden]
            print([a.player for a in active_players])
            if len(active_players) < 1:
                self.status.game_status = self.status.GAMEOVER
            else:
                self.hidden = True

    def right(self):
        new_sq = self.curr_sq.copy()
        new_sq[1] += 1
        self.finish_move(new_sq)

    def left(self):
        new_sq = self.curr_sq.copy()
        new_sq[1] -= 1
        self.finish_move(new_sq)

    def up(self):
        new_sq = self.curr_sq.copy()
        new_sq[0] -= 1
        self.finish_move(new_sq)

    def down(self):
        new_sq = self.curr_sq.copy()
        new_sq[0] += 1
        self.finish_move(new_sq)

    def wrap(self, square):
        sq = square.copy()
        sq[1] = sq[1] % self.st.square_num_x
        return sq

    def wrap_x(self, x):
        return x % self.st.square_num_x

    # validate the given center square and shape squires relative to center square
    def valid(self, square):
        return self.valid_sq(square)

    def valid_sq(self, sq):
        # check border
        if sq[0] < 0 or sq[0] >= self.st.square_num_y:  # or sq[1] >= self.st.square_num_x or sq[1] < 0:
            return False

        # check self crash
        for bit in self.tail:
            if bit[0] == sq[0] and bit[1] == sq[1]:
                return False

        # check others crash
        for snake in self.controller.sqs_list:
            if snake.player != self.player:
                for bit in snake.tail + [snake.curr_sq]:
                    if bit[0] == sq[0] and bit[1] == sq[1]:
                        return False

        return True

    def eat(self):
        x = self.curr_sq[1]
        y = self.curr_sq[0]
        if self.squares[y][x] != 'none':
            self.squares[y][x] = 'none'
            self.controller.add_brick()
            return True
        return False

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
        for y, x in self.tail:
            self.draw_square(y, x, color)

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