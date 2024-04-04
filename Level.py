# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 21:24:03 2024

@author: Jayden
"""

import pygame

import Enemy


def is_adjacent_wall(grid, element, direction):
    """Checks if adjacent element in specified direction is a wall in given grid.

    Args:
        grid (List[List[int,str]]): a 2D list of ints and strings.
        element (List[int]): a list [x, y], specifying a position within the grid.
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


class Level:

    def __init__(self, grid, square_size):
        """Initialises an instance of the Level class.

        Args:
            grid (List[List[int, str]]): a 2D list, representing the game grid.
            square_size (int): the grid square size (in pixels) to be displayed on the screen.
        """
        self.grid = grid
        self.square_size = square_size
        self.wall_list = self.generate_walls()
        self.enemy_list = self.generate_enemies()
        self.origin_coordinates = [square_size/2, square_size/2]

    def generate_walls(self):
        """Generates maze walls from grid.

        Generates walls from grid contained in Level object. 0's represent empty space, and 1's represent walls.

        Returns:
            List[pygame.Rect]: A list of pygame.Rect objects, matching with the position of walls inputted into grid.

        """
        grid = self.grid
        x_dim = len(grid[0])
        y_dim = len(grid)
        square_size = self.square_size

        wall_params = []
        wall_list = []

        for i in range(y_dim - 1):
            for j in range(x_dim - 1):
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    counter = 1
                    direction = 'none'

                    i_iter = i
                    j_iter = j

                    while is_adjacent_wall(grid, (i, j_iter), 'right'):
                        counter += 1
                        j_iter += 1
                        grid[i][j_iter] = 0
                        direction = 'right'

                    if counter == 1:
                        while is_adjacent_wall(grid, (i_iter, j), 'down'):
                            counter += 1
                            i_iter += 1
                            grid[i_iter][j] = 0
                            direction = 'down'

                    wall_params.append([i, j, counter, direction])

        for element in wall_params:
            y = element[0] * square_size
            x = element[1] * square_size
            length = element[2] * square_size
            direction = element[3]

            if direction == 'right':
                wall_list.append(pygame.Rect(x, y, length, square_size))
            elif direction == 'down':
                wall_list.append(pygame.Rect(x, y, square_size, length))
            else:
                wall_list.append(pygame.Rect(x, y, square_size, square_size))

        return wall_list

    def generate_enemies(self):
        """Generates enemies at specified starting location on grid.

        'e' on the grid indicates places for enemies to be generated.

        Returns:
            List[List[int, str]]: a list of Enemy objects

        """
        grid = self.grid
        x_dim = len(grid[0])
        y_dim = len(grid)
        square_size = self.square_size

        enemy_list = []

        for i in range(y_dim - 1):
            for j in range(x_dim - 1):
                if grid[i][j] == 'e':
                    enemy_list.append(Enemy.Enemy(((j + 0.5) * square_size, (i + 0.5) * square_size)))

        return enemy_list
