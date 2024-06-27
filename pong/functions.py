import pygame

class Functions:
    def __init__(self, st, screen):
        self.st = st
        self.screen = screen

    def show_score(self, score):
        surface = None
        text = self.st.score + str(score)
        font = pygame.font.SysFont(self.st.score_font, self.st.score_size)
        surface = font.render(text, True, self.st.score_color)

        # adjust score font when it is too big
        adjust_x = True
        while adjust_x:
            adjust_x = ((surface.get_width() + self.st.score_pos[0]) > self.st.screen_size[0])
            if adjust_x:
                self.st.score_pos[0] -= self.st.score_font_adjust
        adjust_y = True
        while adjust_y:
            adjust_y = ((surface.get_height() + self.st.score_pos[1]) > self.st.screen_size[1])
            if adjust_y:
                self.st.score_pos[1] -= self.st.score_font_adjust
        print(self.st.score_pos)
        self.screen.blit(surface, self.st.score_pos)

class Status:
    def __init__(self):
        # some numbers
        self.GAMEOVER = 0x0
        self.NEWSTART = 0x1
        self.ACTIVE = 0x2
        self.RENEW = 0x3

        # game status
        self.game_status = self.NEWSTART
        self.refresh()

        self.newAI = False

    def is_game_active(self):
        return self.game_status == self.ACTIVE

    def is_game_over(self):
        return self.game_status == self.GAMEOVER

    def is_game_new(self):
        return self.game_status == self.NEWSTART

    def is_game_renew(self):
        return self.game_status == self.RENEW

    def is_AI(self):
        return self.AI

    def refresh(self):
        self.AI = False
        # score status
        self.score = 0


class PlayerStatus:
    def __init__(self):
        self.left = False
        self.right = False
        self.down = False
        self.rotate = False
        self.straight_drop = False

    def refresh(self):
        self.left = False
        self.right = False
        self.down = False
        self.rotate = False
        self.straight_drop = False
