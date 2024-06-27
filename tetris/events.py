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

    if joystick.get_axis(1) < -JOYSTICK_THRESHOLD:
        key_down(pygame.K_SPACE, sqs, status, player_status)
    else:
        key_up(pygame.K_SPACE, player_status)

    if joystick.get_axis(1) > JOYSTICK_THRESHOLD:
        key_down(pygame.K_DOWN, sqs, status, player_status)
    else:
        key_up(pygame.K_DOWN, player_status)

    button_pressed = False
    ai_enabled = False
    for i in range(0,4):
        if joystick.get_button(i) > JOYSTICK_THRESHOLD:
            button_pressed = True
            if status.is_game_new() and i == 0:
                ai_enabled = True
                key_down(pygame.K_a, sqs, status, player_status)
            else:
                key_down(pygame.K_UP, sqs, status, player_status)
    if not button_pressed:
        if ai_enabled:
            key_up(pygame.K_a, player_status)
        else:
            key_up(pygame.K_UP, player_status)


# deal with keys that are pressed down
def key_down(key, sqs, status, player_status):
    if status.is_game_new():
        if sqs.st.num_players == 0:
            sqs.st.num_players = 1
        status.game_status = status.ACTIVE
    elif status.is_game_over():
        status.game_status = status.RENEW
        status.newAI = False
        status.AI = False

    if key == pygame.K_q:   # q stands for quit
        exit()
    if key == pygame.K_DOWN:
        player_status.down = True
    elif key == pygame.K_LEFT and player_status:
        if not player_status.left:
            sqs.clock.update_left_down()
        player_status.left = True
    elif key == pygame.K_RIGHT and player_status:
        if not player_status.right:
            sqs.clock.update_right_down()
        player_status.right = True
    elif key == pygame.K_UP and player_status:
        player_status.rotate = True
    elif key == pygame.K_SPACE and player_status:
        player_status.straight_drop = True
    if key == pygame.K_a:
        status.AI = True
        status.newAI = True
        sqs.st.adjust_for_AI()


# deal with keys that are released
def key_up(key, player_status):
    if key == pygame.K_q:
        exit()
    if key == pygame.K_DOWN and player_status:
        player_status.down = False
    elif key == pygame.K_LEFT and player_status:
        player_status.left = False
    elif key == pygame.K_RIGHT and player_status:
        player_status.right = False
    elif key == pygame.K_UP and player_status:
        player_status.rotate = False
    elif key == pygame.K_SPACE and player_status:
        player_status.straight_drop = False
