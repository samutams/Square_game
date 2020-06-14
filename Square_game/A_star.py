#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class A_star():
    """
    A* Algorithm implementaion
    size - Size of the game
    start_node - Start node
    end_node - Target node
    cost - Cost function
    """
    def __init__(self, size, start_node, end_node, cost ):
        self.size = size 
        self.start_node = start_node
        self.end_node = end_node 
        self.cost = cost  
        self.g_cost_ = np.zeros((self.size, self.size)) 
        self.h_cost_ = np.zeros((self.size, self.size))
        self.f_cost_ = np.zeros((self.size, self.size))
        self.win_flag = False 
        self.neigbours_list = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        self.closed = []
        self.moves = []
        self.parent_x_ = np.zeros((self.size, self.size))
        self.parent_y_ = np.zeros((self.size, self.size))
        self.opt_closed = []
        
        
    def cost_calc(self, g_cost_m, h_cost_m, node):
        """
        Calculate Calculates G, H cost for neigbouring nodes, return matrixes with parent nodes
        """
        current = []
        parent_x = np.zeros((self.size, self.size))
        parent_y = np.zeros((self.size, self.size))
        for i in self.neigbours_list:
            ind = [sum(j) for j in zip(node, i)]
            if any([i < 0 or i > self.size - 1 for i in ind ]):
                pass
            else:
                g_cost_m[ind[0], ind[1]] = sum([abs(e1-e2) for (e1, e2) in zip(self.start_node, ind)]) * self.cost
                h_cost_m[ind[0], ind[1]] = sum([abs(e1-e2) for (e1, e2) in zip(self.end_node, ind)]) * self.cost
                parent_x[ind[0], ind[1]] = node[0]
                parent_y[ind[0], ind[1]] = node[1]
                current.append(ind)

        return([g_cost_m, h_cost_m, current, parent_x, parent_y])
    
    
    def comp_list(self, m_base, m_comp, open_m):
        """
        Compares the non zero, open nodes, and update matrixes if needed, 
        dummy matrix with updated nodes is also produces
        """
        m_base_dummy =  np.zeros((self.size, self.size))
        m_base_dummy[np.nonzero(m_base)] = 1

        m_comp_dummy =  np.zeros((self.size, self.size))
        m_comp_dummy[np.nonzero(m_comp)] = 1

        m_base_c = m_base  * m_comp_dummy * open_m
        m_comp = m_comp  * m_comp_dummy * open_m
        
        update_m = np.zeros((self.size, self.size))
        m_base[m_base_c - np.maximum(m_base_c, m_comp) < 0] = m_comp[m_base_c - np.maximum(m_base_c, m_comp) < 0] 
        update_m[m_base_c - np.maximum(m_base_c, m_comp) < 0] = 1
        return([m_base, update_m])
    
    def translate(self):
        """
             "Translates" optimal game play to pygame steps
        """
        for i in range(0, len(self.opt_closed) - 1):
            if self.opt_closed[i + 1][0] - self.opt_closed[i][0] < 0:
                self.moves.append("pygame.K_UP")
            if self.opt_closed[i + 1][1] - self.opt_closed[i][1] > 0:
                self.moves.append("pygame.K_RIGHT")
            if self.opt_closed[i + 1][1] - self.opt_closed[i][1] < 0:
                self.moves.append("pygame.K_LEFT")
            if self.opt_closed[i + 1][0] - self.opt_closed[i][0] > 0:
                self.moves.append("pygame.K_DOWN")
                
    def excel_f(self,array, sheet, writer):
        """
        Write excel 
        """
        df = pd.DataFrame (array)
        df.to_excel(writer, sheet_name = sheet)
    
    def run_excel(self):
        # Output solution
        writer = pd.ExcelWriter('out_file.xlsx', engine='xlsxwriter')
        self.excel_f(writer = writer, array = self.f_cost_, sheet = "F_cost")
        self.excel_f(writer = writer, array = self.h_cost_, sheet = "H_cost")   
        self.excel_f(writer = writer, array = self.g_cost_, sheet = "G_cost")        
        self.excel_f(writer = writer, array = self.parent_x_, sheet = "Parent_x_")
        self.excel_f(writer = writer, array = self.parent_y_, sheet = "Parent_y_")   
        closed_m = np.zeros((self.size, self.size))
        for i in self.closed:
            closed_m[i[0],i[1]] = 1
        self.excel_f(writer = writer, array = closed_m, sheet = "Closed")   
        writer.save()
        
    def opt_closed_list(self):
        """
        Caclulates "shortest path" from the considered routes
        """
        loop_flag = False
        k = 0
        while loop_flag == False:
            if k == 0:
                self.opt_closed.append(self.closed[-2])
            else:
                self.opt_closed.append([int(self.parent_x_[int(self.opt_closed[k - 1][0]), int(self.opt_closed[k - 1][1])]),
                                       int(self.parent_y_[int(self.opt_closed[k - 1][0]), int(self.opt_closed[k - 1][1])])])

            if self.opt_closed[k] == self.start_node:
                loop_flag = True
            k = k + 1
  
        self.opt_closed.reverse()
        self.opt_closed.append(self.closed[-1])  

    def solve(self, maze_outer):
        """
        A* algorithm in practice
        maze_outer - dummy matrix about the maze (0 - where maze has block, and 1 - no blocks)
        """
        self.closed.append(self.start_node)
        open_ = []
        win_flag = False
        k = 0

        while win_flag == False:
        #for k in range(0,5):

            g_cost = np.zeros((self.size, self.size))
            h_cost = np.zeros((self.size, self.size))
            f_cost = np.zeros((self.size, self.size))

            g_cost, h_cost, current, parent_x, parent_y = self.cost_calc(g_cost_m = g_cost, 
                                                                         h_cost_m = h_cost, 
                                                                         node = self.closed[k])

            f_cost = g_cost + h_cost

            # Open list
            [open_.remove(i) for i in current if i in open_] #make sure, that ther is no duplication
            open_.extend(current)
            #Remove closed cases
            [open_.remove(i) for i in self.closed if i in open_]

            open_m = np.zeros((self.size, self.size))
            for i in open_:
                open_m[i[0],i[1]] = 1

            g_cost = g_cost * open_m * maze_outer
            h_cost = h_cost * open_m * maze_outer
            f_cost = f_cost * open_m * maze_outer

            # Update f_cost_, g_cost,h_cost
            if k == 0:
                self.g_cost_ = g_cost
                self.h_cost_ = h_cost
                self.f_cost_ = f_cost
                self.parent_x_ = parent_x
                self.parent_y_ = parent_y
            else:
                self.g_cost_, update_m = self.comp_list(m_base = self.g_cost_,
                                                        m_comp = g_cost,
                                                        open_m = open_m)
                self.h_cost_, update_m = self.comp_list(m_base = self.h_cost_,
                                                        m_comp = h_cost,
                                                        open_m = open_m)
                
                self.f_cost_ = self.g_cost_ + self.h_cost_
                self.parent_x_[np.where(update_m ==1)] = parent_x[np.where(update_m ==1)]
                self.parent_y_[np.where(update_m ==1)] = parent_y[np.where(update_m ==1)]

                
            # Next Closed
            f_cost_help = self.f_cost_ * open_m
            # Min F cost 
            min_f_cost = np.where(f_cost_help == min(f_cost_help[np.nonzero(f_cost_help)]))

            # Minimum element of the matrix
            i_min = self.h_cost_[min_f_cost].argmin()

            self.closed.append([min_f_cost[0][i_min], min_f_cost[1][i_min]])


            if self.closed[k] == self.end_node:
                win_flag = True
                self.closed = self.closed[:-1]
            k = k + 1
     
        self.opt_closed_list()
        self.translate()

import pygame
import time
import random
import numpy as np
import pandas as pd

