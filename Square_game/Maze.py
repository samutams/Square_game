#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Maze(object):
    def __init__(self, dis_width, dis_height, square_block):
        self.maze_list = []
        #Define maze
        self.square_block = square_block
        self.maze = np.zeros((int(dis_height/self.square_block),int(dis_width/self.square_block)))
        self.maze[0,:] = 1
        self.maze[self.maze.shape[0] - 1,:] = 1
        self.maze[:,0] = 1
        self.maze[:,self.maze.shape[1] - 1] = 1
        self.maze[:,round(self.maze.shape[1]*0.3)] = 1
        self.maze[round(self.maze.shape[0]*0.3):round(self.maze.shape[0]*0.5),round(self.maze.shape[1]*0.3)] = 0
    
    def maze_draw(self, dis, col):
        for i in range(0,self.maze.shape[0]):
            for j in range(0,self.maze.shape[1]):
                if self.maze[i,j] == 1:
                    pygame.draw.rect(dis, col, [j * self.square_block , i * self.square_block,
                                                self.square_block, self.square_block ])     
                    self.maze_list.append([j * self.square_block  , i * self.square_block ])

import pygame
import time
import random
import numpy as np
import pandas as pd

