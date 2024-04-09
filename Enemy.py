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

    def __init__(self, position):
        """Initialises an instance of the Enemy class.

        Args:
            position (List[int]): gives initial position of enemy.
        """
        super(Enemy, self).__init__()
        self.rect_size = 40
        self.surf = pygame.Surface((self.rect_size, self.rect_size))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=position)
        self.speed = 1.2

        self.seen_player = False
        self.projectile_direction = pygame.math.Vector2(0, 0)
        self.projectile_speed = random.randint(2, 3)
        self.projectile_cooldown = 0

    def attack(self, level, cooldown):
        """Creates an enemy bullet when the player is seen by the enemy.

        Creates a bullet when seen_player is True, moving in a straight line towards the player, with speed
        self.projectile_speed, and a specified cooldown between bullets.

        Args:
            level (Level): the game level.
            cooldown (int): the cooldown between bullets fired by enemies.
        """
        if self.seen_player and self.projectile_cooldown == 0:
            level.enemy_bullets.add(
                Bullet.Bullet(self.rect.x + self.rect_size / 2, self.rect.y + self.rect_size / 2,
                              self.projectile_direction, self.projectile_speed))
            self.projectile_cooldown = cooldown

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

    def radial_attack(self, level, num_bullets, cooldown):
        """Radial attack pattern for enemy.

        Creates num_bullets number of bullets in a radial pattern around the enemy, at evenly spaced angles, with a
        specified cooldown.

        Args:
            level (Level): the game level.
            num_bullets (int): the number of bullets to fire at a time.
            cooldown (int):

        """
        degrees = 360/num_bullets

        if self.seen_player and self.projectile_cooldown ==0:
            for i in range(num_bullets):
                level.enemy_bullets.add(
                    Bullet.Bullet(self.rect.x + self.rect_size / 2, self.rect.y + self.rect_size / 2,
                                  self.projectile_direction.rotate(degrees * i), self.projectile_speed))
            self.projectile_cooldown = cooldown

        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

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

        move_direction = pygame.math.Vector2(0, 0)

        if player.rect.width / 2 < dist_to_player < max_range * grid_sq_size and self.seen_player == True:
            move_direction = (player.vector2 - enemy_vector2).normalize()

        elif player.rect.width / 2 < dist_to_player < min_range * grid_sq_size:
            move_direction = (player.vector2 - enemy_vector2).normalize()
            self.seen_player = True

        else:
            self.seen_player = False

        # Sets projectile direction in straight line to player from enemy
        self.projectile_direction = move_direction

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


class Point:
    def __init__(self, position, parent=-1):
        """Initialises Point class

        Args:
            position (List[int]), optional: (y, x), position of point on grid
            parent (Point): Point from which this point was generated
        """
        self.position = position
        self.actual_cost = 0
        self.parent = parent

        if parent != -1:
            self.actual_cost = parent.actual_cost + 1


def remove_strings(grid):
    grid = copy.deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 1:
                grid[i][j] = 0
    return grid


def find_path(grid, start, end):
    """Finds a path on a grid between defined start and end points.

    Args:
        grid (List[List[int]]): 2D list of 0's and 1's. Element int(1) is treated as a wall.
        start (Point): start point.
        end (Point): end point.

    Returns:
        List[List[int]]: A 2D list of values. 4 denotes the start point, 2 denotes points along the path, 5 denotes the
        end point, 3 denotes points that were searched, and 1 denotes walls.

    Raises:
        Exception "NO POSSIBLE PATH": if there is no possible path between the start and end points.

    """
    to_search = [start]
    searched = np.zeros(np.shape(grid))

    finished = False

    while not finished:

        lowest_cost = -1

        for point in to_search:

            estimated_cost = abs(end.position[0] - point.position[0]) + abs(end.position[1] - point.position[1])
            cost = point.actual_cost + 1.2 * estimated_cost

            if lowest_cost == -1 or lowest_cost > cost:
                lowest_cost = cost
                lowest_point = point

        low_x = lowest_point.position[0]
        low_y = lowest_point.position[1]

        searched[low_x, low_y] = 3
        to_search.remove(lowest_point)

        grid_dim = np.shape(searched)

        new_points = [Point([low_x - 1, low_y], lowest_point),
                      Point([low_x, low_y - 1], lowest_point),
                      Point([low_x + 1, low_y], lowest_point),
                      Point([low_x, low_y + 1], lowest_point)]

        adjacent_points = []
        for point in new_points:
            x = point.position[0]
            y = point.position[1]

            if x < 0 or x > (grid_dim[0] - 1) or y < 0 or y > (grid_dim[1] - 1):
                continue

            if grid[x][y] == 1 or searched[x][y] == 3:
                continue

            if point.position == end.position:
                adjacent_points = [point]
                finished = True

            else:
                adjacent_points.append(point)

        to_search.extend(adjacent_points)

        if len(to_search) == 0:
            print(grid, start.position, end.position)
            raise Exception("NO POSSIBLE PATH")

    current_point = adjacent_points[0]
    parent = current_point.parent

    while parent != -1:
        searched[current_point.position[0]][current_point.position[1]] = 2
        current_point = parent
        parent = current_point.parent

    searched[start.position[0]][start.position[1]] = 4
    searched[end.position[0]][end.position[1]] = 5

    searched = np.asarray(searched)
    grid = np.asarray(grid)

    return searched + grid
