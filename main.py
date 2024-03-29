# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 12:29:44 2024

@author: Jayden
"""

import AStar

grid = [[0,1,0],
        [0,0,0],
        [0,1,0]]
   
    
start = AStar.point([0,0])
end = AStar.point([0,2])
AStar.solution(grid, start, end)