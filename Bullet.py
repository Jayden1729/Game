import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, vector, speed, colour):
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
        self.colour = colour

        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(center=(x, y))

        self.animation_frame = 0
        self.frame_break = 0

    def animate(self, screen, images):
        """Animates the bullet.

        Args:
            screen (pygame.display): the game screen.
            images (Images): an image object holding the bullet images.
        """
        offset = [3, 3]
        large_offset = [7, 7]
        frame_break = 7

        if self.colour == "red":
            bullet_images = images.red_bullet
            bullet_list = images.red_bullet_list[1:]

        elif self.colour == 'purple':
            bullet_images = images.purple_bullet
            bullet_list = images.purple_bullet_list[1:]
            offset = large_offset

        elif self.colour == 'green':
            bullet_images = images.green_bullet
            bullet_list = images.green_bullet_list[1:]
            offset = large_offset

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
