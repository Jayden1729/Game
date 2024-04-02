# -*- coding: utf-8 -*-
"""
Naming conventions:

class: CapWords
variable: lower_case
constants: CAPITAL_CASE



"""

import AStar
import pygame
import Player
import Level

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


# initialise pygame
pygame.init()

# Variables
screen_width = 800
screen_height = 800
fps = 90

# Setup initial objects
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
player = Player.Player()
level = Level.Level([[0, 0, 0, 0, 0, 'e', 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                          [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 'e', 0, 0, 0, 0, 0, 0, 0],
                          [1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
                          [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                          [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
                          [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 80)

running = True

# Game Loop
while running:
    screen.fill((90,90,90))

    # for loop through event queue
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    for wall in level.wall_list:
        pygame.draw.rect(screen, (0, 150, 0), wall)

    # get all keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # move walls based on key presses
    level.update_walls(player, pressed_keys)

    screen.blit(player.surf,player.rect)

    pygame.display.flip()

    clock.tick(fps)


pygame.quit()

