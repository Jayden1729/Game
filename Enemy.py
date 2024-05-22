import copy
import sys

import pygame
import configparser
import json

import Bullet
import Level
import Player


enemy_config = configparser.SafeConfigParser()
enemy_config.read('enemy_config.ini')

class Enemy(pygame.sprite.Sprite):

    def __init__(self, position, enemy_type, images):
        """Initialises an instance of the Enemy class.

        Args:
            position (List[int]): gives initial position of enemy.
        """
        super(Enemy, self).__init__()

        enemy_dict = images.enemy_dict

        self.images = enemy_dict[enemy_type]

        # Config parameters
        config = dict(enemy_config.items(enemy_type))
        self.cooldown = json.loads(config['cooldown'])
        self.speed = json.loads(config['speed'])
        self.hp = json.loads(config['hp'])
        self.bullet_colour = config['bullet_colour']
        self.time_reward = json.loads(config['time_reward'])
        self.damage = json.loads(config['damage'])
        self.attack_pattern = enemy_type

        self.bullet_dict = images.bullet_dict

        # Define hit box
        self.rect_size = 40
        self.surf = pygame.Surface((self.rect_size, self.rect_size))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=position)

        # Track animations
        self.animation_frame = 0
        self.frame_break = 0

        # Track enemy states
        self.seen_player = False
        self.has_exploded = False
        self.is_hit = False
        self.is_attacking = False

        # Track attack variables
        self.attack_direction = pygame.math.Vector2(0, 0)
        self.projectile_speed = 2.5
        self.attack_cooldown = 0
        self.dist_to_player = 1000

    def normal_attack(self, level):
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
                              self.attack_direction, self.projectile_speed, self.bullet_dict[self.bullet_colour], self.damage))
            self.attack_cooldown = self.cooldown

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def radial_attack(self, level, num_bullets):
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
                                  pygame.math.Vector2(0, 1).rotate(degrees * i), self.projectile_speed,
                                  self.bullet_dict[self.bullet_colour], self.damage))
            self.attack_cooldown = self.cooldown

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def melee_attack(self, level):
        """Melee attack for enemy.

        Attacks the player if it is withing a specified radius of the enemy.

        Args:
            level (Level): the game level.
        """
        if self.is_attacking and self.animation_frame == 4 and self.frame_break == 5:
            attack_direction = self.attack_direction.normalize() * self.rect_size
            centre_vector = pygame.math.Vector2(self.rect.x + self.rect_size / 2, self.rect.y + self.rect_size / 2)
            attack_centre = centre_vector + attack_direction
            level.enemy_melee.add(
                Bullet.Melee(attack_centre.x, attack_centre.y, 40, 40, self.damage))

        elif self.seen_player and self.attack_cooldown == 0 and self.dist_to_player <= 100:
            self.attack_cooldown = self.cooldown
            self.is_attacking = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def explosion_attack(self, level):
        """Explosion attack for enemy.

        When player is within range, the enemy explodes and kills itself.

        Args:
            level (Level): The game level.
        """

        if self.seen_player and self.attack_cooldown == 0 and self.dist_to_player <= 30 and not self.has_exploded:
            level.enemy_melee.add(
                Bullet.Melee(self.rect.x, self.rect.y, 150, 150, self.damage))

            self.set_death_conditions()
            self.has_exploded = True

    def update_movement(self, level: Level, player: Player, range):
        """Moves the enemy towards the player

        Handles detection of the player, enemy pathfinding and wall collisions. The player will be initially detected
        when they get within range number of grid squares of the player, then the enemy will chase the player in a
        straight line until the player.


        Args:
            level (Level): the game level.
            player (Player): the player.
            max_range (float): number of grid squares determining how far away the enemy will see the player
        """

        # Move enemy

        grid_sq_size = level.square_size

        enemy_vector2 = pygame.math.Vector2(self.rect.x, self.rect.y)

        dist_to_player = enemy_vector2.distance_to(player.vector2)
        self.dist_to_player = dist_to_player

        move_direction = pygame.math.Vector2(0, 0)

        if player.rect.width / 2 < dist_to_player < range * grid_sq_size:
            move_direction = (player.vector2 - enemy_vector2).normalize()
            self.seen_player = True

            # Sets projectile direction in straight line to player from enemy
            self.attack_direction = move_direction

        elif player.rect.width / 2 > dist_to_player:
            move_direction = pygame.math.Vector2(0, 0)

        else:
            self.seen_player = False

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

    def run_animation(self, run_images, run_frames, screen, left_offset, right_offset, frame_break=10, xbool=True, ybool=False):
        """Runs an animation.

        Args:
            run_images (png): png file containing all animation poses.
            run_frames (List[pygame.Rect]): list of pygame.Rect objects containing the location of each frame in
                run_images.
            screen (pygame.display): The game screen.
            left_offset (List[int]): a list [x, y] containing the offset for the image to be displayed when the player
                is to the left of the enemy.
            right_offset (List[int]): a list [x, y] containing the offset for the image to be displayed when the player
                is to the right of the enemy.
        """
        if self.animation_frame >= len(run_frames):
            self.animation_frame = 0

        if self.attack_direction.x <= 0:
            run_images = pygame.transform.flip(run_images, xbool, ybool)
            screen.blit(run_images, (self.rect.x - left_offset[0], self.rect.y - left_offset[1]),
                        run_frames[self.animation_frame])
        else:
            screen.blit(run_images, (self.rect.x - right_offset[0], self.rect.y - right_offset[1]),
                        run_frames[self.animation_frame])

        if self.frame_break == 0:
            self.animation_frame += 1
            self.frame_break = frame_break
        else:
            self.frame_break -= 1

    def animate(self, screen):
        """Animates the enemy.

        Args:
            screen (pygame.display): the game screen.
        """
        # Explosion animation
        if self.has_exploded:
            explosion_list = self.images['explosion']
            self.run_animation(explosion_list[0], explosion_list[1], screen,
                               explosion_list[2], explosion_list[3], 7, xbool=False)

            if self.animation_frame >= len(explosion_list[1]):
                self.kill()

        # Death animation
        elif self.hp == 0:
            death_list = self.images['death']
            self.run_animation(death_list[0], death_list[1], screen, death_list[2], death_list[3])

            if self.animation_frame >= len(death_list[1]):
                self.kill()

        # Hit animation
        elif self.is_hit:
            hit_list = self.images['hit']
            self.run_animation(hit_list[0], hit_list[1], screen, hit_list[2], hit_list[3])

            if self.animation_frame >= len(hit_list[1]):
                self.is_hit = False

        # Attack animation
        elif self.is_attacking:
            attack_list = self.images['attack']
            self.run_animation(attack_list[0], attack_list[1], screen, attack_list[2], attack_list[3])

            if self.animation_frame >= len(attack_list[1]):
                self.is_attacking = False

        # Running animation
        elif self.seen_player:
            run_list = self.images['run']
            self.run_animation(run_list[0], run_list[1], screen, run_list[2], run_list[3])

    def set_death_conditions(self):
        """Changes the conditions of the enemy when it dies, so that player attacks don't collide, and it cannot move.
        """
        self.animation_frame = 0
        self.frame_break = 0
        self.speed = 0
        self.rect = pygame.Rect(self.rect.x, self.rect.y, 0, 0)

    def attack(self, level):
        '''Handles the enemy attack type.

            Determines which attack pattern to execute for the enemy. Accepted attack patterns are: 'normal', 'radial',
            'melee', and 'explosion'

        Args:
            level (Level): the game level.

        Raises:
            'Enemy attack pattern is not specified correctly': if enemy attack pattern is not an accepted enemy type.
        '''
        if self.hp > 0:
            if self.attack_pattern == 'normal':
                self.normal_attack(level)
            elif self.attack_pattern == 'radial':
                self.radial_attack(level, 6)
            elif self.attack_pattern == 'melee':
                self.melee_attack(level)
            elif self.attack_pattern == 'explosion':
                self.explosion_attack(level)
            else:
                raise('Enemy attack pattern is not specified correctly')