# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 21:24:03 2024

@author: Jayden
"""

import pygame

# returns if the element next to the specified element in the grid is a wall,
# either to the right or down depending on the specified direction
# grid is a 2D list [[,]] element is a list [x,y], direction is 'right' or 'down'
def isNextWall(grid, element, direction):
    if element[0]+1 >= len(grid) or element[1]+1 >= len(grid[0]):
        return False
    if direction == 'right':
        if grid[element[0]][element[1]+1] == 1:
            return True
    if direction == 'down':
        if grid[element[0]+1][element[1]] == 1:
            return True
    return False


class Level():

    def __init__(self, grid, squareSize):
        self.grid = grid
        self.squareSize = squareSize
        self.wallList = self.generateWalls()

# takes specified grid and converts it into a list describing rectangle objects to be created as walls,
# list indicates the starting y and x of the wall, the length in grid square units, and the direction
# from the starting point, either right, down, or none (only 1 square big) i.e. in format [starting y, starting x, length in grid units, direction]
# 0's in grid indicate no wall, 1's indicate a wall

    def gridToRectParams(self):
        grid = self.grid
        xDim = len(grid[0])
        yDim = len(grid)

        wallParams = []

        for i in range(yDim-1):
            for j in range(xDim-1):
                if grid[i][j] == 0:
                    continue
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    counter = 1
                    direction = 'none'

                    iIter = i
                    jIter = j

                    while isNextWall(grid,[i,jIter], 'right'):
                        counter +=1
                        jIter+=1
                        grid[i][jIter] = 0
                        direction = 'right'

                    if counter == 1:
                        while isNextWall(grid, [iIter, j], 'down'):
                            counter += 1
                            iIter += 1
                            grid[iIter][j] = 0
                            direction = 'down'

                    wallParams.append([i, j, counter, direction])

        return(wallParams)

# takes wall parameters as given by gridToRectParams, and generates list of Rects to act as walls
    def generateWalls(self):
        squareSize = self.squareSize
        wallParams = self.gridToRectParams()

        wallList = []

        for element in wallParams:
            y = element[0]*squareSize
            x = element[1]*squareSize
            length = element[2]*squareSize
            direction = element[3]

            if direction == 'right':
                wallList.append(pygame.Rect(x, y, length, squareSize))
            elif direction == 'down':
                wallList.append(pygame.Rect(x, y, squareSize, length))
            else:
                wallList.append(pygame.Rect(x, y, squareSize, squareSize))

        return(wallList)


    def wallCollision(self, player):
        wallList = self.wallList
        playerX = player.rect.x
        playerY = player.rect.y
        playerWidth = player.rect.width
        playerHeight = player.rect.height

        collisionIndex = player.rect.collidelistall(wallList)

        if collisionIndex == []:
            return

        for i in collisionIndex:
            wallX = wallList[i].x
            wallY = wallList[i].y
            wallWidth = wallList[i].width
            wallHeight = wallList[i].height


            # colliding with top edge of wall
            if (playerY + playerHeight) > wallY and playerY < wallY:
                player.rect.move_ip(0, -(playerY + playerHeight - wallY))

            elif (playerX + playerWidth) > wallX and playerX < wallX:
                print('left')
                player.rect.move_ip(-(playerX + playerWidth - wallX), 0)

            elif playerY < (wallY + wallHeight) and (playerY + playerHeight) > (wallY + wallHeight):
                print('bot')
                player.rect.move_ip(0, (wallY + wallHeight - playerY))

            elif playerX < (wallX + wallWidth) and (playerX + playerWidth) > (wallX + wallWidth):
                print('right')
                player.rect.move_ip((wallX + wallWidth - playerX), 0)



        print(collisionIndex)




