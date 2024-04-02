# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 21:24:03 2024

@author: Jayden
"""

import pygame


def is_next_wall(grid, element, direction):
    """Checks if adjacent element in specified direction is a wall in given grid.

    Args:
        grid (list): a 2D list of 0's and 1's.
        element (tuple): a tuple (x, y), specifying a position within the grid.
        direction (str): 'right' indicates to check the right adjacent element,
                         'down' indicates to check the below adjacent element.

    Returns:
        bool: True if neighbour element in specified direction is 1, False if not.

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


class Level():

    def __init__(self, grid, square_size):
        """Initialises an instance of the Level class.

        Args:
            grid (list): a 2D list of 1's and 0's, representing the game grid.
            square_size (int): the grid square size (in pixels) to be displayed on the screen.
        """
        self.grid = grid
        self.square_size = square_size
        self.wall_list = self.generate_walls()

    def generate_walls(self):
        """Generates maze walls from grid.

        Generates walls from grid contained in Level object.
        0's represent empty space, and 1's represent walls.

        Returns:
            list: A list of pygame.rect objects, matching with the position of walls inputted into grid.

        """
        grid = self.grid
        x_dim = len(grid[0])
        y_dim = len(grid)
        square_size = self.square_size

        wall_params = []
        wall_list = []

        for i in range(y_dim - 1):
            for j in range(x_dim - 1):
                if grid[i][j] == 0:
                    continue
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    counter = 1
                    direction = 'none'

                    i_iter = i
                    j_iter = j

                    while is_next_wall(grid, (i, j_iter), 'right'):
                        counter += 1
                        j_iter += 1
                        grid[i][j_iter] = 0
                        direction = 'right'

                    if counter == 1:
                        while is_next_wall(grid, (i_iter, j), 'down'):
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

        return (wall_list)

    def update_walls(self, player, pressed_keys):
        """Moves walls around player on key press and handles wall collisions.

        Moves walls around player to give illusion of player movement, and handles wall collisions.
        Movement speed is equal to player.speed.

        Args:
            player (Player): the player character
            pressed_keys (bools): sequence of bools indicating which keys are pressed
        """
        wall_list = self.wall_list
        player_x = player.rect.x
        player_y = player.rect.y
        player_width = player.rect.width
        player_height = player.rect.height

        # Move walls in x direction
        if pressed_keys[pygame.K_LEFT]:
            for wall in wall_list:
                wall.move_ip(player.speed, 0)

        if pressed_keys[pygame.K_RIGHT]:
            for wall in wall_list:
                wall.move_ip(-player.speed, 0)

        # Check collisions in x direction
        collision_index_x = player.rect.collidelistall(wall_list)

        if collision_index_x:

            for i in collision_index_x:
                wall_x = wall_list[i].x
                wall_width = wall_list[i].width

                if (player_x + player_width) > wall_x > player_x:
                    for wall in wall_list:
                        wall.move_ip((player_x + player_width - wall_x), 0)

                elif player_x < (wall_x + wall_width) < (player_x + player_width):
                    for wall in wall_list:
                        wall.move_ip(-(wall_x + wall_width - player_x), 0)

        # Move walls in y direction
        if pressed_keys[pygame.K_UP]:
            for wall in wall_list:
                wall.move_ip(0, player.speed)

        if pressed_keys[pygame.K_DOWN]:
            for wall in wall_list:
                wall.move_ip(0, -player.speed)

        # Check collisions in y direction
        collision_index_y = player.rect.collidelistall(wall_list)

        if collision_index_y:

            for i in collision_index_y:
                wall_y = wall_list[i].y
                wall_height = wall_list[i].height

                if (player_y + player_height) > wall_y > player_y:
                    for wall in wall_list:
                        wall.move_ip(0, (player_y + player_height - wall_y))

                elif player_y < (wall_y + wall_height) < (player_y + player_height):
                    for wall in wall_list:
                        wall.move_ip(0, -(wall_y + wall_height - player_y))
