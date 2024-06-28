import time

import pygame
from sys import exit

JOYSTICK_THRESHOLD = .5


def x_button_pressed(joystick):
    return joystick.get_button(2) > JOYSTICK_THRESHOLD

def b_button_pressed(joystick):
    return joystick.get_button(1) > JOYSTICK_THRESHOLD

def a_button_pressed(joystick):
    return joystick.get_button(0) > JOYSTICK_THRESHOLD


def check_joystick(sqs, joystick, status, player_status):
    if status.is_game_over() and not joystick.get_button(4) > JOYSTICK_THRESHOLD:
        key_down(pygame.K_TAB, None, status, None)

    if joystick.get_axis(0) < -JOYSTICK_THRESHOLD:
        player_status.refresh()
        player_status.left = True

    if joystick.get_axis(0) > JOYSTICK_THRESHOLD:
        player_status.refresh()
        player_status.right = True

    if joystick.get_axis(1) < -JOYSTICK_THRESHOLD:
        player_status.refresh()
        player_status.up = True

    if joystick.get_axis(1) > JOYSTICK_THRESHOLD:
        player_status.refresh()
        player_status.down = True


# deal with keys that are pressed down
def key_down(key, sqs, status, player_status):
    if status.is_game_new():
        if sqs.st.num_players == 0:
            sqs.st.num_players = 1
        sqs.controller.set_starting_positions()
        status.game_status = status.ACTIVE
    elif status.is_game_over():
        status.game_status = status.RENEW
        status.newAI = False
        status.AI = False

    if key == pygame.K_q:   # q stands for quit
        exit()
