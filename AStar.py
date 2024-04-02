# A* baby
import numpy as np


class point():
    position = -1
    parent = -1
    total_cost = -1
    actual_cost = 0
    def __init__(self, position, parent = 0):
        self.position = position
        
        if parent != 0:
            self.parent = parent
            self.actual_cost = parent.actual_cost + 1
    
    def is_wall(self, grid):        
        if grid[self.position[0]][self.position[1]] == 1:
            return True
        else:
            return False
    
    def cost(self, end):
        estimated_cost = abs(end[0] - self.position[0]) + abs(end[1] - self.position[1])
        self.total_cost = self.actual_cost + 1.2 * estimated_cost


def solution(grid, start, end):
    to_search = [start]
    searched = np.zeros(np.shape(grid))
    is_end = False
   
    while is_end == False:
        if end.is_wall(grid) or start.is_wall(grid):
            print("ERROR: END OR START IS WALL")
            break
        surrounding_points, is_end = update_search(grid, to_search, searched, start, end)
        if len(to_search) == 0:
            print("NO POSSIBLE PATH")
            break

    current_point = surrounding_points[0]
    parent = current_point.parent
    while parent != -1:
        searched[current_point.position[0]][current_point.position[1]] = 2
        current_point = parent
        parent = current_point.parent
    
    searched[start.position[0]][start.position[1]] = 3
    searched[end.position[0]][end.position[1]] = 4
    
    searched = np.asarray(searched)
    grid = np.asarray(grid)
    
    print(searched + 6* grid)
    for element in to_search:
        print(element.position)
    

def find_brian(to_search, start, end):
    lowest_cost = -1
    lowest_point = 0
    for point1 in to_search:
        point1.cost(start.position, end.position)
        cost = point1.total_cost
        if lowest_cost == -1 or lowest_cost > cost:
            lowest_cost = cost
            lowest_point = point1
    return lowest_point


def update_search(grid, to_search, searched, start, end):
    lowest_point = find_brian(to_search, start, end)
    searched[lowest_point.position[0]][lowest_point.position[1]] = 1
    to_search.remove(lowest_point)
    surrounding_points, is_end = find_michelle(grid, lowest_point, searched, end)
    to_search.extend(surrounding_points)
    return surrounding_points, is_end
    

def find_michelle(grid, node, searched, end):
    is_end = False
    node_position = node.position
    grid_dim = np.shape(searched)
    surrounding_points = [point([node_position[0] - 1, node_position[1]], node),
                         point([node_position[0], node_position[1] - 1], node),
                         point([node_position[0] + 1, node_position[1]], node),
                         point([node_position[0], node_position[1] + 1], node)]
    
    new_array = []
    for point1 in surrounding_points:
        if point1.position == end.position:
            return [point1], True
        elif point1.position[0] < 0 or point1.position[0] > (grid_dim[0] - 1) or point1.position[1] < 0 or point1.position[1] > (grid_dim[1] - 1):
            i = 1
        elif point1.is_wall(grid) == True:
            i = 1
        elif searched[point1.position[0]][point1.position[1]] == 1:
            i = 1
        else:
            new_array.append(point1)
    return new_array, is_end
        
        
def main():

   grid = [[0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,1,0,0],
            [0,0,0,1,1,1,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],]
   '''
   grid = [[0,1,0],
           [0,0,0],
           [0,1,0]]
   '''
    
   start = point([0,0])
   end = point([0,9])
   solution(grid, start, end)
   print("3 is start, 6 is wall, 2 is path, 4 is end, things underneath are squares in the search list that were not searched")


if __name__ == '__main__':
    main()