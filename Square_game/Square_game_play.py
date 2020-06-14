#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Square_game():
 
    display_col = (255, 255, 255)
    player_col = (0, 0, 0)
    text_col = (255, 0, 0)
    food_col = (0, 0, 255)
    maze_col = (50, 205, 55)

    dis_width = 400
    dis_height = 400

    square_block = 20
 
    game_over = False
    game_close = False
    game_win = False
    
    def __init__(self):
        self.player = Player(square_block = self.square_block, dis_width = self.dis_width, dis_height = self.dis_height)                                       
        self.maze = Maze(dis_width = self.dis_width, dis_height = self.dis_height, square_block = self.square_block)
        self.food = Food(dis_width = self.dis_width, dis_height = self.dis_height) 
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))

    def message(self,msg, color, dis):
        font_style = pygame.font.SysFont(None, 20)
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [self.dis_width/4, self.dis_height/2])

    def eval_(self):
        for i in self.maze.maze_list:
            if i[0] == self.player.x and i[1] == self.player.y:
                self.game_close = True    

        if self.player.x == self.food.foodx and self.player.y == self.food.foody:
            self.game_close = True
            self.game_win = True   


    def gameLoop(self):  # creating a functionű
        self.game_over = False
        self.game_close = False
        self.game_win = False
        clock = pygame.time.Clock()
        while not self.game_over:

            while self.game_close == True:
                if self.game_win == True:
                    self.dis.fill(self.display_col)    
                    self.message("You Won! Press Q-Quit or P-Play Again", self.text_col, dis = self.dis)
                    pygame.display.update()

                if self.game_win == False: 
                    self.dis.fill(self.display_col)    
                    self.message("You Lost! Press Q-Quit or P-Play Again", self.text_col, dis = self.dis)
                    pygame.display.update()


                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        if event.key == pygame.K_p:
                            self.player.reset() 
                            self.gameLoop()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.moveLeft()
                    elif event.key == pygame.K_RIGHT:
                        self.player.moveRight()
                    elif event.key == pygame.K_UP:
                        self.player.moveUp()
                    elif event.key == pygame.K_DOWN:
                        self.player.moveDown()

            self.dis.fill(self.display_col)
            self.maze.maze_draw(dis = self.dis, col = self.maze_col)
            self.food.food_draw(dis = self.dis, col = self.food_col, square_block = self.square_block)
            self.player.player_draw(dis = self.dis, col = self.player_col , square_block = self.square_block)
            pygame.display.update()

            self.eval_()

             
            
            clock.tick(self.square_block)
        
        pygame.display.quit()
        #pygame.quit()
        #quit()
        
    def run_game(self):
        pygame.init()
        pygame.display.set_caption('Snake like Game by Tamas')
        font_style = pygame.font.SysFont(None, 30)
        self.gameLoop()
        
        
import pygame
import time
import random
import numpy as np
import pandas as pd

from Square_game.Maze import *
from Square_game.A_star import *
from Square_game.Player import *
from Square_game.Food import *

