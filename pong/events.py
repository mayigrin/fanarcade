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
    if status.is_game_new() and not b_button_pressed(joystick):
        return

    if joystick.get_axis(0) < -JOYSTICK_THRESHOLD:
        key_down(pygame.K_LEFT, sqs, status, player_status)
    else:
        key_up(pygame.K_LEFT, player_status)

    if joystick.get_axis(0) > JOYSTICK_THRESHOLD:
        key_down(pygame.K_RIGHT, sqs, status, player_status)
    else:
        key_up(pygame.K_RIGHT, player_status)

    for i in range(10):
        if joystick.get_button(i) > JOYSTICK_THRESHOLD:
            key_down(pygame.K_TAB, sqs, status, player_status)


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
    elif key == pygame.K_LEFT and player_status:
        if not player_status.left:
            sqs.clock.update_move()
        player_status.left = True
    elif key == pygame.K_RIGHT and player_status:
        if not player_status.right:
            sqs.clock.update_move()
        player_status.right = True


# deal with keys that are released
def key_up(key, player_status):
    if key == pygame.K_q:
        exit()
    elif key == pygame.K_LEFT and player_status:
        player_status.left = False
    elif key == pygame.K_RIGHT and player_status:
        player_status.right = False
