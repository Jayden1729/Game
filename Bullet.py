import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, vector, speed):
        """Initialises instance of Bullet class.

        Args:
            x (int): initial x position of bullet on screen.
            y (int): initial y position of bullet on screen.
            vector (pygame.math.Vector2): direction of bullet movement.
            speed (float): speed of bullet movement.
        """
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.vector = vector.normalize()
        self.speed = speed

        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(center=(x, y))

class Melee(pygame.sprite.Sprite):

    def __init__(self, x, y, length, width, damage):
        """Initialises a new instance of the melee class

        Args:
            x (int): x position of melee attack.
            y (int): y position of melee attack.
            length (int): length of melee attack.
            width (int): width of melee attack.
            damage (int): damage of melee attack.
        """

        super(Melee, self).__init__()

        self.surf = pygame.Surface((length, width))
        self.rect = self.surf.get_rect(center=(x,y))
        self.damage = damage
        self.display_time = 1

