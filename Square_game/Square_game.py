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
        self.a_star = A_star(size = int(self.dis_width / self.square_block), 
                             start_node = [int(self.player.y/ self.square_block),int(self.player.x/self.square_block) ], 
                             end_node = [int(self.food.foody/self.square_block),int(self.food.foodx/self.square_block) ] , 
                             cost = 10)
        self.maze_outer = np.zeros((20,20))
        self.maze_outer[self.maze.maze == 0] = 1
        self.a_star.solve(maze_outer = self.maze_outer)

        

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

    def update(self):
            self.dis.fill(self.display_col)
            self.maze.maze_draw(dis = self.dis, col = self.maze_col)
            self.food.food_draw(dis = self.dis, col = self.food_col, square_block = self.square_block)
            self.player.player_draw(dis = self.dis, col = self.player_col , square_block = self.square_block)
            pygame.display.update()
            self.eval_()
    
    def gameLoop(self):  # creating a functionű
        self.game_over = False
        self.game_close = False
        self.game_win = False
        clock = pygame.time.Clock()
        k = 0
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
                        

            self.update()

            try:
                if self.a_star.moves[k] == 'pygame.K_LEFT':
                    self.player.moveLeft()
                    time.sleep(0.5)
                    self.update()

                elif self.a_star.moves[k] == 'pygame.K_RIGHT':
                    self.player.moveRight()
                    time.sleep(0.5)
                    self.update()

                elif self.a_star.moves[k] == 'pygame.K_UP':
                    self.player.moveUp()
                    time.sleep(0.5)
                    self.update()

                elif self.a_star.moves[k] == 'pygame.K_DOWN':
                    self.player.moveDown() 
                    time.sleep(0.5)
                    self.update()
                    
            except IndexError:
                self.game_close = True
                
            #newevent = pygame.event.Event(pygame.KEYDOWN, key=moves[k], mod=pygame.KMOD_NONE) #create the event
            #pygame.event.post(newevent)
             
            
            clock.tick(self.square_block)
            
            k = k + 1
        
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

