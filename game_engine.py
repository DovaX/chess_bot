import pygame
import random
import numpy as np
import math
import game_mechanics

class Col:
    """Defines all used colours"""
    def __init__(self):
        self.black=(0,0,0)
        self.white=(255,255,255)
        self.red=(255,0,0)
        
        self.yellow=(255,255,0)
        self.green=(0,200,0)
        self.blue=(0,0,255)
        self.purple=(155,0,255)
        self.cyan=(0,255,255)
        self.grey=(120,120,120)
        self.pink=(255,120,120)
        self.darkgreen=(0,50,0)
        self.brown=(140,42,42)
c=Col()

class Position:
    def __init__(self,position):
        self.position=position
        self.x=position[0]
        self.y=position[1]
    def distance(self,diff_position):
        return(math.hypot(self.x-diff_position.x,self.y-diff_position.y))
    
class Rectangle(Position):
    def __init__(self,position,size):
        super().__init__(position)
        self.size = size #list of two values
    def width(self):
        return(self.size[0]) 
    def height(self):
        return(self.size[1])
    
class Window(Rectangle):
    def __init__(self,size,position=[0,0],bg_color=c.black):
        super().__init__(position,size)
        self.bg_color=bg_color
        self.screen = pygame.display.set_mode(self.size)
        
    def initialize_game(self):    
        pygame.init()
        pygame.display.set_caption("Chess bot")
        clock=pygame.time.Clock()
        self.screen.fill(self.bg_color)
        #gameIcon = pygame.image.load('icon.png')
        #pygame.display.set_icon(gameIcon)
        return(clock)  
      
    def draw_grid(self,grid):
        for row in range(grid.rows):
            for column in range(grid.columns):
                value=grid.grid[row][column]
                #print(value)
                color = grid.colors[value]
                pygame.draw.rect(self.screen,
                                 color,
                                 [(grid.margin + grid.cell_size[0]) * column + grid.margin + grid.position[0],
                                  (grid.margin + grid.cell_size[1]) * row + grid.margin + grid.position[1],
                                  grid.cell_size[0],
                                  grid.cell_size[1]]) 
                
    def select_cell(self,grid,row,col):
        if row is not None and col is not None:
            pygame.draw.rect(self.screen,
                                     c.black,
                                     [(grid.margin + grid.cell_size[0]) * col + grid.margin + grid.position[0],
                                      (grid.margin + grid.cell_size[1]) * row + grid.margin + grid.position[1],
                                      grid.cell_size[0],
                                      grid.cell_size[1]],2) 
            
        
    def draw_label(self,label):
        myfont = pygame.font.SysFont(label.font, label.fontsize)
        lbl = myfont.render(label.text, 1, label.color)
        self.screen.blit(lbl, (label.position[0], label.position[1]))
        
    def remove_label(self,label):
        myfont = pygame.font.SysFont(label.font, label.fontsize)
        lbl = myfont.render(label.text, 1, self.bg_color)
        self.screen.blit(lbl, (label.position[0], label.position[1]))
    
class Label(Position):
    def __init__(self,position,text,color=(0,0,0),font="Cambria",fontsize=10):
        super().__init__(position)
        self.text=text
        self.color=color
        self.font=font
        self.fontsize=fontsize

    
class Grid(Rectangle):
    def __init__(self,rows,columns,position=[0,0],cell_size=[20,20],margin=1,colors=[c.white]):
        size=[(cell_size[0]+margin)*columns+margin,(cell_size[1]+margin)*columns+margin]
        super().__init__(position,size)
        self.colors=colors
        self.cell_size=cell_size
        self.margin=margin
        self.rows=rows
        self.columns=columns
        self.grid = []
        for row in range(rows):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(columns):
                self.grid[row].append(0)  # Append a cell 
                

    def get_element_index(self,row,column):
        if not(column>=self.columns or row>=self.rows or column<0 or row<0):
            row_len=self.columns
            print(row,column,self.columns)
            index=row_len*row+column
            return(index)
                
    def evaluate_row_column_indices(self,click):
        column = (click[0]-self.position[0]) // (self.cell_size[0] + self.margin)
        row = (click[1]-self.position[1]) // (self.cell_size[1] + self.margin)
        return(row,column)


def main_program_loop(window,clock):
    done = False
    grids=[]
    labels=[]
                              
    game1=game_mechanics.game1
    grids=game_mechanics.initialize_grids(grids)
    time_fr=0 #1/60 sec
    time=0 #1 sec
    #gameIcon = pygame.image.load('icon.png')
    #window.screen.blit(gameIcon,(10,10))
    selected_row=None
    selected_col=None
    number_of_turns_list=[]
    number_of_turns=0
    while not done:     
        game1=game_mechanics.game1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected_row,selected_col=game_mechanics.evaluate_click(grids,pos)
        
        for grid in grids:
            window.draw_grid(grid)
            window.select_cell(grid,selected_row,selected_col)
        labels=[piece.piece_label for piece in game1.pieces]
        for label in labels:
            window.draw_label(label)                   
        
        clock.tick(60)
        
        time_fr+=1
        if time_fr%1==0:
            #pass
            if game1.new_game==False:
                game1.play_turn()
                number_of_turns+=1
            else:
                number_of_turns_list.append(number_of_turns)
                number_of_turns=0
                game_mechanics.initialize_game()
            #game_mechanics.time_event(grids,time_fr)
        if time_fr%60==0:
            time+=1
            print("time:",time,"SCORE:",game_mechanics.SCORE,"TURNS:",number_of_turns_list)
                        
        pygame.display.flip()
        
def run():
    window=Window([1600,900])
    clock = window.initialize_game()
    main_program_loop(window, clock)
    pygame.quit()
    

if __name__=='__main__':
    run()