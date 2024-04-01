# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 12:29:44 2024

@author: Jayden
"""

import AStar
import pygame
import Characters
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
screenWidth = 800
screenHeight = 800
fps = 60

# Setup initial objects
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
player = Characters.Player()
level = Level.Level([[0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                          [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                          [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 50)

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

    for wall in level.wallList:
        pygame.draw.rect(screen, (0, 255, 0), wall)

    # get all keys currently pressed
    pressedKeys = pygame.key.get_pressed()

    # update the player sprite based on user keypresses
    player.update(pressedKeys)
    level.wallCollision(player)

    screen.blit(player.surf,player.rect)

    pygame.display.flip()

    clock.tick(fps)


pygame.quit()

