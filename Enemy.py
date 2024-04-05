import copy

import pygame
import numpy as np
import random
import copy


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
        self.speed = random.randint(2, 4)

    def update_movement(self, level, player):
        max_range = 9
        min_range = 2

        grid_sq_size = level.square_size

        enemy_vector2 = pygame.math.Vector2(self.rect.x, self.rect.y)

        dist_to_player = enemy_vector2.distance_to(player.vector2)

        if player.rect.width / 2 < dist_to_player < min_range * grid_sq_size:
            move_direction = (player.vector2 - enemy_vector2).normalize()
            self.rect.move_ip(move_direction.x * self.speed, move_direction.y * self.speed)

        elif min_range * level.square_size < dist_to_player < max_range * level.square_size:
            vec_to_origin = level.origin_coords - enemy_vector2
            grid_location = [-round(vec_to_origin.y / grid_sq_size), -round(vec_to_origin.x / grid_sq_size)]

            player_vec_origin = level.origin_coords - player.vector2
            player_grid_loc = [-round(player_vec_origin.y / grid_sq_size), -round(player_vec_origin.x / grid_sq_size)]

            path_grid = find_path(remove_strings(level.grid), Point(grid_location), Point(player_grid_loc))



            print(path_grid)


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
