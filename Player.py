"""Player class controls attributes of the player character

"""
import pygame
import Level
import Bullet


class Player(pygame.sprite.Sprite):

    def __init__(self):
        """
        Initialises the Player class.
        """
        super(Player, self).__init__()
        rect_size = 20
        self.surf = pygame.Surface((rect_size, rect_size))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(400, 400))
        self.vector2 = pygame.math.Vector2(400, 400)
        self.speed = 5
        self.projectile_speed = 10
        self.attack_cooldown = 0

        self.grid_x = None
        self.grid_y = None

        self.sprite = pygame.image.load("sprites/Player_sprite.png")
        self.sprite = pygame.transform.scale(self.sprite, (64, 64))


    def attack(self, player_bullets):
        """Creates a bullet and adds to player_bullets group

        Args:
            player_bullets (pygame.Group[Bullets]): a pygame.Group object of Bullet objects.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_vector = pygame.math.Vector2(mouse_x, mouse_y)

        bullet_vector = mouse_vector - self.vector2

        player_bullets.add(Bullet.Bullet(400, 400, bullet_vector, self.projectile_speed))
        self.attack_cooldown = 20
