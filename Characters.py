# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 21:57:00 2024

@author: Jayden
"""
import pygame
import Level

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill((0,0,255))
        self.rect = self.surf.get_rect()
        self.speed = 5

    def update(self, pressedKeys):
        if pressedKeys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)

        if pressedKeys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressedKeys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressedKeys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(random.randint(0,800),random.randint(0, 800)
        )
        self.speed = random.randint(5, 20)
