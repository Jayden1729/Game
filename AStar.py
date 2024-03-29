# A* baby
import numpy as np


class point():
    position = -1
    parent = -1
    totalCost = -1
    actualCost = 0
    
    
    def __init__(self, position, parent = 0):
        self.position = position
        
        if parent != 0:
            self.parent = parent
            self.actualCost = parent.actualCost + 1
    
    def isWall(self, grid):        
        if grid[self.position[0]][self.position[1]] == 1:
            return True
        else:
            return False
    
    def cost(self, start, end):
        estimatedCost = abs(end[0] - self.position[0]) + abs(end[1] - self.position[1])
        self.totalCost = self.actualCost + 1.2 * estimatedCost


def solution(grid, start, end):
    toSearch = [start]
    searched = np.zeros(np.shape(grid))
    isEnd = False
   
    while isEnd == False:
        if end.isWall(grid) or start.isWall(grid):
            print("ERROR: END OR START IS WALL")
            break
        surroundingPoints, isEnd = updateSearch(grid, toSearch, searched, start, end)
        if len(toSearch) == 0:
            print("NO POSSIBLE PATH")
            break

    currentPoint = surroundingPoints[0]
    parent = currentPoint.parent
    while parent != -1:
        searched[currentPoint.position[0]][currentPoint.position[1]] = 2
        currentPoint = parent
        parent = currentPoint.parent
    
    searched[start.position[0]][start.position[1]] = 3
    searched[end.position[0]][end.position[1]] = 4
    
    searched = np.asarray(searched)
    grid = np.asarray(grid)
    
    print(searched + 6* grid)
    for element in toSearch:
        print(element.position)
    

def findBrian(toSearch, start, end):
    lowestCost = -1
    lowestPoint = 0
    for point1 in toSearch:
        point1.cost(start.position, end.position)
        cost = point1.totalCost
        if lowestCost == -1 or lowestCost > cost:
            lowestCost = cost
            lowestPoint = point1
    return lowestPoint


def updateSearch(grid, toSearch, searched, start, end):
    lowestPoint = findBrian(toSearch, start, end)
    searched[lowestPoint.position[0]][lowestPoint.position[1]] = 1
    toSearch.remove(lowestPoint)
    surroundingPoints, isEnd = findMichelle(grid, lowestPoint, searched, end)
    toSearch.extend(surroundingPoints)
    return surroundingPoints, isEnd
    

def findMichelle(grid, node, searched, end):
    isEnd = False
    nodePosition = node.position
    gridDim = np.shape(searched)
    surroundingPoints = [point([nodePosition[0] - 1, nodePosition[1]], node),
                         point([nodePosition[0], nodePosition[1] - 1], node),
                         point([nodePosition[0] + 1, nodePosition[1]], node),
                         point([nodePosition[0], nodePosition[1] + 1], node)]
    
    newArray = []
    for point1 in surroundingPoints:
        if point1.position == end.position:
            return [point1], True
        elif point1.position[0] < 0 or point1.position[0] > (gridDim[0] - 1) or point1.position[1] < 0 or point1.position[1] > (gridDim[1] - 1):
            i = 1
        elif point1.isWall(grid) == True:
            i = 1
        elif searched[point1.position[0]][point1.position[1]] == 1:
            i = 1
        else:
            newArray.append(point1)
    return newArray, isEnd
        
        
def main():
   '''
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
   
    
   start = point([0,0])
   end = point([0,2])
   solution(grid, start, end)
   print("3 is start, 6 is wall, 2 is path, 4 is end, things underneath are squares in the search list that were not searched")


if __name__ == '__main__':
    main()