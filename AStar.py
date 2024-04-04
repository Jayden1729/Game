# A* baby
import numpy as np


class Point:
    def __init__(self, position, parent=-1):
        """Initialises Point class
        
        Args:
            position (list): (x, y), position of point on grid
            parent (Point): Point from which this point was generated
        """
        self.position = position
        self.actual_cost = 0
        self.parent = parent

        if parent != -1:
            self.actual_cost = parent.actual_cost + 1


def pathfind(grid, start, end):
    """Finds a path on a grid between defined start and end points.

    Args:
        grid (:obj:'list' of :obj:'list' of :obj:'int'): 2D list of 0's and 1's. Element int(1) is treated as a wall.
        start (Point): start point.
        end (Point): end point.

    Returns:
        :obj:'list' of :obj:'list of :obj:'int': A 2D list of values. 4 denotes the start point, 2 denotes points
            along the path, 5 denotes the end point, 3 denotes points that were searched, and 1 denotes walls.

    Raises:
        Exception "END OR START IS WALL": if the start or end points are walls in grid.
        Exception "NO POSSIBLE PATH": if there is no possible path between the start and end points.

    """
    to_search = [start]
    searched = np.zeros(np.shape(grid))
    finished = False

    if grid[end.position[0]][end.position[1]] == 1 or grid[start.position[0]][start.position[1]] == 1:
        raise Exception("END OR START IS WALL")

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


def main():
    grid = [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    '''
   grid = [[0,1,0],
           [0,0,0],
           [0,1,0]]
   '''

    start = Point((0, 0))
    end = Point([0, 9])
    print(pathfind(grid, start, end))
    print(
        "4 is start, 1 is wall, 2 is path, 5 is end, things underneath are squares in the search list that were not searched")


if __name__ == '__main__':
    main()
