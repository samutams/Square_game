#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Player(object):
    def __init__(self, square_block, dis_width, dis_height):
        self.dis_width = dis_width
        self.dis_height = dis_height
        self.x = self.dis_width / 10 * 8
        self.y = self.dis_height / 2
        self.last_change = ""
        self.square_block = square_block
        
    def moveRight(self):
        self.x = self.x + self.square_block
        self.last_change = "Right"
 
    def moveLeft(self):
        self.x = self.x - self.square_block
        self.last_change = "Left" 

    def moveUp(self):
        self.y = self.y - self.square_block
        self.last_change = "Up" 

    def moveDown(self):
        self.y = self.y + self.square_block
        self.last_change = "Down"    
    
    def repeat(self):
        time.sleep(0.05)
        if self.last_change == "Right":
            self.moveRight()
        elif self.last_change == "Left":
            self.moveLeft()
        elif self.last_change == "Up":
            self.moveUp()                   
        elif self.last_change == "Down":
            self.moveDown()
            
    def reset(self):
        self.x = self.dis_width / 10 * 8
        self.y = self.dis_height / 2
        self.last_change = ""
        
    def player_draw(self, dis, col, square_block):
        pygame.draw.rect(dis, col, [self.x, self.y, square_block, square_block])
        
import pygame
import time
import random
import numpy as np
import pandas as pd        

