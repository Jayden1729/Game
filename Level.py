# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 21:24:03 2024

@author: Jayden
"""

import pygame
import copy
import random

import Enemy


class Level:

    def __init__(self, grid, square_size, images):
        """Initialises an instance of the Level class.

        Args:
            grid (List[List[int, str]]): a 2D list, representing the game grid.
            square_size (int): the grid square size (in pixels) to be displayed on the screen.
        """
        self.grid = grid
        self.origin_coords = [0, 70]
        self.floor_image_grid = randomise_floor_grid(copy.deepcopy(grid))
        self.square_size = square_size
        self.wall_list = self.generate_walls()
        self.enemy_list = self.generate_enemies(images)
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemy_melee = pygame.sprite.Group()
        self.time = 15000

    def generate_walls(self):
        """Generates walls from new_grid.

        Generates walls from new_grid contained in Level object. 0's represent empty space, and 1's represent walls.

        Returns:
            List[pygame.Rect]: a list of pygame.Rect objects, matching with the position of walls inputted into new_grid.

        """
        new_grid = copy.deepcopy(self.grid)
        x_dim = len(new_grid[0])
        y_dim = len(new_grid)
        square_size = self.square_size

        wall_params = []
        wall_list = []

        for i in range(y_dim):
            for j in range(x_dim):
                if new_grid[i][j] == 1:
                    new_grid[i][j] = 0
                    counter = 1
                    direction = 'none'

                    i_iter = i
                    j_iter = j

                    while is_adjacent_wall(new_grid, (i, j_iter), 'right'):
                        counter += 1
                        j_iter += 1
                        new_grid[i][j_iter] = 0
                        direction = 'right'

                    if counter == 1:
                        while is_adjacent_wall(new_grid, (i_iter, j), 'down'):
                            counter += 1
                            i_iter += 1
                            new_grid[i_iter][j] = 0
                            direction = 'down'

                    wall_params.append([i, j, counter, direction])

        for element in wall_params:
            y = element[0] * square_size + self.origin_coords[1]
            x = element[1] * square_size + self.origin_coords[0]
            length = element[2] * square_size
            direction = element[3]

            if direction == 'right':
                wall_list.append(pygame.Rect(x, y, length, square_size))
            elif direction == 'down':
                wall_list.append(pygame.Rect(x, y, square_size, length))
            else:
                wall_list.append(pygame.Rect(x, y, square_size, square_size))

        return wall_list

    def generate_enemies(self, images):
        """Generates enemies at specified starting location on grid.

        'e' on the grid indicates places for normal enemies to be generated.
        'r' on the grid indicates places for radial attack enemies to be generated.
        'm' on the grid indicates places for melee attack enemies to be generated.

        Returns:
            pygame.Group[Enemy]: a pygame Group of Enemy objects.

        """
        grid = self.grid
        x_dim = len(grid[0])
        y_dim = len(grid)
        square_size = self.square_size

        enemy_list = pygame.sprite.Group()

        for i in range(y_dim - 1):
            for j in range(x_dim - 1):
                enemy_x = (j + 0.5) * square_size + self.origin_coords[0]
                enemy_y = (i + 0.5) * square_size + self.origin_coords[1]
                if grid[i][j] == 'e':
                    enemy_list.add(Enemy.Enemy((enemy_x, enemy_y), 'normal', images))
                elif grid[i][j] == 'r':
                    enemy_list.add(Enemy.Enemy((enemy_x, enemy_y), 'radial', images))
                elif grid[i][j] == 'm':
                    enemy_list.add(Enemy.Enemy((enemy_x, enemy_y), 'melee', images))
                elif grid[i][j] == 'x':
                    enemy_list.add(Enemy.Enemy((enemy_x, enemy_y), 'explosion', images))

        return enemy_list

    def update_player_bullets(self, screen, show_hitboxes):
        """Moves and displays player bullets and checks collisions with walls and enemies.

        Moves player bullets by bullet.speed in direction bullet.vector. If a bullet collides with a wall it is killed.
        If a bullet collides with an enemy, both the bullet and enemy are killed. The bullets are also displayed on the
        screen.

        Args:
            screen (pygame.display): the screen to draw bullets on.
            show_hitboxes (bool): True to show bullet hixboxes.
        """
        for bullet in self.player_bullets:
            bullet.rect.move_ip(bullet.vector.x * bullet.speed, bullet.vector.y * bullet.speed)
            if bullet.rect.collidelistall(self.wall_list):
                bullet.kill()

            for enemy in self.enemy_list:
                if pygame.Rect.colliderect(bullet.rect, enemy.rect):
                    bullet.kill()
                    enemy.is_hit = True
                    enemy.animation_frame = 0
                    enemy.frame_break = 0
                    enemy.hp -= 1
                    if enemy.hp == 0:
                        enemy.set_death_conditions()
                        self.time += enemy.time_reward

                    break

            bullet.animate(screen)

            if show_hitboxes:
                screen.blit(bullet.surf, bullet.rect)

    def update_enemy_bullets(self, screen, player, show_hitboxes):
        """Moves and displays enemy bullets, checks collisions with walls and the player.

        Moves enemy bullets by bullet.speed in direction bullet.vector. If a bullet collides with a wall it is killed.
        If a bullet collides with the player, the bullet is killed and player.hp is reduced by 10. The bullets are also
        displayed on the screen.

        Args:
            screen (pygame.display): the screen to display bullets on.
            player (Player): the player character.
            show_hitboxes (bool): True to show bullet hixboxes.
        """
        for bullet in self.enemy_bullets:
            bullet.rect.move_ip(bullet.vector.x * bullet.speed, bullet.vector.y * bullet.speed)
            if bullet.rect.collidelistall(self.wall_list):
                bullet.kill()

            if pygame.Rect.colliderect(player.rect, bullet.rect):
                self.time -= bullet.damage
                bullet.kill()

            bullet.animate(screen)

            if show_hitboxes:
                screen.blit(bullet.surf, bullet.rect)


def is_adjacent_wall(grid, element, direction):
    """Checks if adjacent element in specified direction is a wall in given grid.

    Args:
        grid (List[List[int,str]]): a 2D list of ints and strings.
        element (List[int]): a list [y, x], specifying a position within the grid.
        direction (str): 'right' indicates to check the right adjacent element,
                         'down' indicates to check the below adjacent element.

    Returns:
        bool: True if neighbour element in specified direction is int(1), False if not.

    """
    if element[0] + 1 >= len(grid) or element[1] + 1 >= len(grid[0]):
        return False
    if direction == 'right':
        if grid[element[0]][element[1] + 1] == 1:
            return True
    if direction == 'down':
        if grid[element[0] + 1][element[1]] == 1:
            return True
    return False


def randomise_floor_grid(grid):
    """Randomises the floor tiles in the grid.

    For each floor tile, a number between 0 and 4 is chosen, corresponding to the type of floor tile to be displayed.

    Args:
        grid (List[List[int and str]]): The level grid.

    Returns:
        List[List[int and str]]: a 2d list containing ints and strings. A value of 'n' indicates a square with no floor
            tile, while a value between 0 and 4 corresponds to the type of floor tile to be displayed on the screen.

    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '0':
                grid[i][j] = 'n'
            elif grid[i][j] != 1:
                grid[i][j] = random.choices([0, 1, 2, 3, 4], [72, 7, 7, 7, 7])[0]
            else:
                grid[i][j] = 'n'

    return grid
