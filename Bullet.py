import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, vector, speed, images, damage=1):
        """Initialises instance of Bullet class.

        Args:
            x (int): initial x position of bullet on screen.
            y (int): initial y position of bullet on screen.
            vector (pygame.math.Vector2): direction of bullet movement.
            speed (float): speed of bullet movement.
            colour (str): the colour of the bullet, either 'red', 'purple' or 'green'.
        """
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.vector = vector.normalize()
        self.speed = speed
        self.damage = damage
        self.images = images

        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(center=(x, y))

        self.animation_frame = 0
        self.frame_break = 0

    def animate(self, screen):
        """Animates the bullet.

        Args:
            screen (pygame.display): the game screen.
        """
        frame_break = 7
        bullet_images = self.images[0]
        bullet_list = self.images[1][1:]
        offset = self.images[2]

        if self.animation_frame >= len(bullet_list):
            self.animation_frame = 0

        screen.blit(bullet_images, (self.rect.x - offset[0], self.rect.y - offset[1]),
                            bullet_list[-self.animation_frame])

        if self.frame_break == 0:
            self.animation_frame += 1
            self.frame_break = frame_break
        else:
            self.frame_break -= 1


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
        self.rect = self.surf.get_rect(center=(x, y))
        self.damage = damage
        self.display_time = 1
