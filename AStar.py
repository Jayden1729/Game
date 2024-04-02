# A* baby
import numpy as np


class Point():
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

def solution(grid, start, end):
    """

    Args:
        grid (list): grid to search for path
        start (Point): start point
        end (Point): end point

    Returns:

    """
    to_search = [start]
    searched = np.zeros(np.shape(grid))
    is_end = False

    if grid[end.position[0]][end.position[1]] == 1 or grid[start.position[0]][start.position[1]] == 1:
        print("ERROR: END OR START IS WALL")
        is_end = True

    while not is_end:

        lowest_cost = -1
        for point in to_search:
            estimated_cost = abs(end.position[0] - point.position[0]) + abs(end.position[1] - point.position[1])
            cost = point.actual_cost + 1.2 * estimated_cost
            if lowest_cost == -1 or lowest_cost > cost:
                lowest_cost = cost
                lowest_point = point

        low_x = lowest_point.position[0]
        low_y = lowest_point.position[1]

        searched[low_x, low_y] = 1
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

            if grid[x][y] == 1 or searched[x][y] == 1:
                continue

            if point.position == end.position:
                adjacent_points = [point]
                is_end = True

            else:
                adjacent_points.append(point)

        to_search.extend(adjacent_points)

        if len(to_search) == 0:
            print("NO POSSIBLE PATH")
            break

    current_point = adjacent_points[0]
    parent = current_point.parent
    while parent != -1:
        searched[current_point.position[0]][current_point.position[1]] = 2
        current_point = parent
        parent = current_point.parent

    searched[start.position[0]][start.position[1]] = 3
    searched[end.position[0]][end.position[1]] = 4

    searched = np.asarray(searched)
    grid = np.asarray(grid)

    print(searched + 6 * grid)

def main():
    grid = [[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ]
    '''
   grid = [[0,1,0],
           [0,0,0],
           [0,1,0]]
   '''

    start = Point((0, 0))
    end = Point([0, 9])
    solution(grid, start, end)
    print(
        "3 is start, 6 is wall, 2 is path, 4 is end, things underneath are squares in the search list that were not searched")


if __name__ == '__main__':
    main()
