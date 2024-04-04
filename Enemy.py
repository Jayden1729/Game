import pygame
import random


class Enemy(pygame.sprite.Sprite):

    def __init__(self, position):
        """Initialises an instance of the Enemy class.

        Args:
            position (List[int]): gives initial position of enemy.
        """
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=position)
        self.hp = 100
        self.speed = random.randint(3,7)

    def update_movement(self, level, player):
        max_range = 9
        min_range = 3

        enemy_vector2 = pygame.math.Vector2(self.rect.x, self.rect.y)

        dist_to_player = enemy_vector2.distance_to(player.vector2)

        if player.rect.width/2 < dist_to_player < min_range * level.square_size:
            direction = (player.vector2 - enemy_vector2).normalize()
            self.rect.move_ip(direction.x * self.speed, direction.y * self.speed)
