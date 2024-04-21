import copy
import sys

import pygame
import numpy as np
import random
import copy

import Bullet
import Level
import Player


class Enemy(pygame.sprite.Sprite):

    def __init__(self, position, hp, speed, attack_pattern):
        """Initialises an instance of the Enemy class.

        Args:
            position (List[int]): gives initial position of enemy.
        """

        super(Enemy, self).__init__()
        self.rect_size = 40
        self.surf = pygame.Surface((self.rect_size, self.rect_size))
        self.surf.fill((255, 0, 0))

        self.sprite = pygame.image.load("sprites/Bat.gif")
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))

        if attack_pattern == 'radial':
            self.surf.fill((255, 255, 0))
            self.sprite = pygame.image.load("sprites/Ghost.gif")
            self.sprite = pygame.transform.scale(self.sprite, (80, 80))

        self.rect = self.surf.get_rect(center=position)
        self.speed = speed
        self.hp = hp

        self.seen_player = False
        self.attack_direction = pygame.math.Vector2(0, 0)
        self.projectile_speed = 2.5
        self.attack_cooldown = 0
        self.dist_to_player = 1000
        self.attack_pattern = attack_pattern

    def normal_attack(self, level, cooldown):
        """Creates an enemy bullet when the player is seen by the enemy.

        Creates a bullet when seen_player is True, moving in a straight line towards the player, with speed
        self.projectile_speed, and a specified cooldown between shots.

        Args:
            level (Level): the game level.
            cooldown (int): the cooldown between bullets fired by enemies.
        """

        if self.seen_player and self.attack_cooldown == 0:
            level.enemy_bullets.add(
                Bullet.Bullet(self.rect.x + self.rect_size / 2, self.rect.y + self.rect_size / 2,
                              self.attack_direction, self.projectile_speed))
            self.attack_cooldown = cooldown

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def radial_attack(self, level, num_bullets, cooldown):
        """Radial attack pattern for enemy.

        Creates num_bullets number of bullets in a radial pattern around the enemy, at evenly spaced angles, with a
        specified cooldown between shots.

        Args:
            level (Level): the game level.
            num_bullets (int): the number of bullets to fire at a time.
            cooldown (int): number of frames between attacks.
        """

        degrees = 360 / num_bullets

        if self.seen_player and self.attack_cooldown == 0:
            for i in range(num_bullets):
                level.enemy_bullets.add(
                    Bullet.Bullet(self.rect.x + self.rect_size / 2, self.rect.y + self.rect_size / 2,
                                  pygame.math.Vector2(0, 1).rotate(degrees * i), self.projectile_speed))
            self.attack_cooldown = cooldown

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def melee_attack(self, level, cooldown):
        """Melee attack for enemy.

        Attacks the player if it is withing a specified radius of the enemy.

        Args:
            level (Level): the game level.
            cooldown (int): number of frames between attacks.
        """

        if self.seen_player and self.attack_cooldown == 0 and self.dist_to_player <= 100:
            attack_direction = self.attack_direction.normalize() * self.rect_size
            centre_vector = pygame.math.Vector2(self.rect.x + self.rect_size / 2, self.rect.y + self.rect_size / 2)
            attack_centre = centre_vector + attack_direction
            level.enemy_melee.add(
                Bullet.Melee(attack_centre.x, attack_centre.y, 40, 40, 10))
            self.attack_cooldown = cooldown

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def explosion_attack(self, level):
        """Explosion attack for enemy.

        When player is within range, the enemy explodes and kills itself.

        Args:
            level (Level): The game level.
        """

        if self.seen_player and self.attack_cooldown == 0 and self.dist_to_player <= 50:
            level.enemy_melee.add(
                Bullet.Melee(self.rect.x, self.rect.y, 150, 150, 200))

            self.kill()

    def attack(self, level, cooldown):
        """Causes enemy attack based on attack pattern.

        Args:
            level (Level): the game level.
            cooldown (int): cooldown between shots.
        """

        if self.attack_pattern == 'normal':
            self.normal_attack(level, cooldown)

        elif self.attack_pattern == 'radial':
            self.radial_attack(level, 6, cooldown)

        elif self.attack_pattern == 'melee':
            self.melee_attack(level, cooldown)

        elif self.attack_pattern == 'explosion':
            self.explosion_attack(level)

    def update_movement(self, level: Level, player: Player, min_range, max_range):
        """Moves the enemy towards the player

        Handles detection of the player, enemy pathfinding and wall collisions. The player will be initially detected
        when they get within min_range number of grid squares of the player, and the enemy will chase the player in a
        straight line until the player is outside max_range number of grid squares away from the enemy.


        Args:
            level (Level): the game level.
            player (Player): the player.
            min_range (float): number of grid squares determining initial player detection.
            max_range (float): number of grid squares determining how far away the enemy will chase the player
        """

        # Move enemy

        grid_sq_size = level.square_size

        enemy_vector2 = pygame.math.Vector2(self.rect.x, self.rect.y)

        dist_to_player = enemy_vector2.distance_to(player.vector2)
        self.dist_to_player = dist_to_player

        move_direction = pygame.math.Vector2(0, 0)

        if player.rect.width / 2 < dist_to_player < max_range * grid_sq_size and self.seen_player == True:
            move_direction = (player.vector2 - enemy_vector2).normalize()

        elif player.rect.width / 2 < dist_to_player < min_range * grid_sq_size:
            move_direction = (player.vector2 - enemy_vector2).normalize()
            self.seen_player = True

        else:
            self.seen_player = False

        # Sets projectile direction in straight line to player from enemy
        self.attack_direction = move_direction

        # Check wall collisions

        # Move in x direction
        self.rect.move_ip(move_direction.x * self.speed, 0)
        enemy_x = self.rect.x
        enemy_width = self.rect.width

        # Check collisions in x direction
        collision_index_x = self.rect.collidelistall(level.wall_list)

        if collision_index_x:

            for i in collision_index_x:
                wall_x = level.wall_list[i].x
                wall_width = level.wall_list[i].width

                if (enemy_x + enemy_width) > wall_x > enemy_x:
                    self.rect.move_ip(-(enemy_x + enemy_width - wall_x), 0)

                elif enemy_x < (wall_x + wall_width) < (enemy_x + enemy_width):
                    self.rect.move_ip((wall_x + wall_width - enemy_x), 0)

        # Move in y direction
        self.rect.move_ip(0, move_direction.y * self.speed)
        enemy_y = self.rect.y
        enemy_height = self.rect.height

        # Check collisions in x direction
        collision_index_y = self.rect.collidelistall(level.wall_list)

        if collision_index_y:

            for i in collision_index_y:
                wall_y = level.wall_list[i].y
                wall_height = level.wall_list[i].height

                if (enemy_y + enemy_height) > wall_y > enemy_y:
                    self.rect.move_ip(0, -(enemy_y + enemy_height - wall_y))

                elif enemy_y < (wall_y + wall_height) < (enemy_y + enemy_height):
                    self.rect.move_ip(0, (wall_y + wall_height - enemy_y))


class NormalEnemy(Enemy):

    def __init__(self, position):
        """Creates a normal enemy.

        Args:
            position (List[int]): the position [x, y] to spawn the enemy.
        """
        self.speed = 1.5
        self.hp = 1
        super(NormalEnemy, self).__init__(position, self.hp, self.speed, 'normal')


class RadialEnemy(Enemy):

    def __init__(self, position):
        """Creates a radial enemy.

        Args:
            position (List[int]): the position [x, y] to spawn the enemy.
        """
        self.speed = 1.5
        self.hp = 2
        super(RadialEnemy, self).__init__(position, self.hp, self.speed, 'radial')


class MeleeEnemy(Enemy):

    def __init__(self, position, ):
        """Creates a melee enemy.

        Args:
            position (List[int]): the position [x, y] to spawn the enemy.
        """
        self.speed = 2.5
        self.hp = 2
        super(MeleeEnemy, self).__init__(position, self.hp, self.speed, 'melee')


class ExplosionEnemy(Enemy):

    def __init__(self, position):
        """Creates an explosion enemy.

        Args:
            position (List[int]): the position [x, y] to spawn the enemy.
        """
        self.run_frame = 0
        self.frame_break = 0
        self.speed = 3
        self.hp = 3
        super(ExplosionEnemy, self).__init__(position, self.hp, self.speed, 'explosion')

    def animate(self, images, screen):
        """Animates the explosion enemy.

        Args:
            images (Images): Images class, contains the images to display.
            screen (pygame.display): the game screen.
        """
        if self.seen_player:
            run_images = images.explosion_enemy_run
            run_frames = images.ex_enemy_run_list

            if self.run_frame >= len(run_frames):
                self.run_frame = 1

            if self.attack_direction.x <= 0:
                run_images = pygame.transform.flip(run_images, True, False)
                screen.blit(run_images, (self.rect.x - 65, self.rect.y - 40),
                            run_frames[self.run_frame])
            else:
                screen.blit(run_images, (self.rect.x - 10, self.rect.y - 40),
                            run_frames[self.run_frame])

            if self.frame_break == 0:
                self.run_frame += 1
                self.frame_break = 15
            else:
                self.frame_break -= 1

