
import pygame

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, vector, speed):
        self.vector = vector.normalize()
        self.speed = speed

        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(center = (x, y))


