import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, position):
        """Initialises an instance of the Enemy class.

        Args:
            position (List[int]): gives initial position of enemy.
        """
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(topleft=position)
        self.hp = 100
