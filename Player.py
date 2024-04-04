"""Player class controls attributes of the player character

"""
import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self):
        """
        Initialises the Player class.
        """
        super(Player, self).__init__()

        rect_size = 40
        self.surf = pygame.Surface((rect_size, rect_size))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(400, 400))
        self.vector2 = pygame.math.Vector2(400 - rect_size/2, 400 - rect_size/2)
        self.speed = 7
        self.exp = 0
        self.hp = 100
