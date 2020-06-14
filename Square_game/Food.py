#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Food(object):
    def __init__(self, dis_width, dis_height):
        self.foodx = dis_width / 10 
        self.foody = dis_height / 10 * 8
    
    def random_food(self, square_block):
        self.foodx = round(random.randrange(0, dis_width - square_block) / 10.0) * 10.0
        self.foody = round(random.randrange(0, dis_height - square_block) / 10.0) * 10.0
 
    def food_draw(self, dis , col , square_block):
        pygame.draw.rect(dis, col, [self.foodx, self.foody, square_block, square_block])
        
import pygame
import time
import random
import numpy as np
import pandas as pd

