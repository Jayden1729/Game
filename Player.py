"""Player class controls attributes of the player character

"""
import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self):
        """
        Initialises the Player class.
        """
        super(Player, self).__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(400, 400))
        self.speed = 7
        self.exp = 0
        self.hp = 100
