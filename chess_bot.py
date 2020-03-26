import pynput.mouse
import pynput.keyboard
import time
#from pynput import Button, Controller

mouse = pynput.mouse.Controller()
button = pynput.mouse.Button
keyboard = pynput.keyboard.Controller()
key = pynput.keyboard.Key


def drag_mouse(relative_rows,relative_cols):
    mouse.press(button.left)
    mouse.move(relative_cols*SIZE_X, -relative_rows*SIZE_Y)
    mouse.release(button.left)

#Website parameters
#Single player - second screen maximized
SIZE_X=68
SIZE_Y=68
OFFSET_X=2480
OFFSET_Y=200

#Two players - second screen split
OFFSET_X=2000
OFFSET_Y=200
OFFSET_X2=2960
OFFSET_Y2=200

def move_mouse_in_grid(row,col,player=1):
    if player==1:
        mouse.position=OFFSET_X+SIZE_X*(col-1),OFFSET_Y+SIZE_Y*(8-row)
    elif player==2:
        mouse.position=OFFSET_X2+SIZE_X*(col-1),OFFSET_Y2+SIZE_Y*(8-row)

class Piece:
    def __init__(self,row,col,type_input,player):
        self.row=row
        self.col=col
        self.type=type_input
        self.player=player
        
    def move(self,steps,direction): #direction = 1 ahead then clockwise to 8
        
        move_mouse_in_grid(self.row,self.col,self.player.number)
        drag_mouse(1,0)
        self.row+=1

class Player:
    def __init__(self,number):
        self.number=number
        if self.number==1:
            self.on_turn=True
        else:
            self.on_turn=False
        self.pieces=[]
        for i in range(1,9):
            piece=Piece(2,i,"P",self)
            self.pieces.append(piece)
            
        for i in [1,8]:  
            piece=Piece(1,i,"R",self)
            self.pieces.append(piece)

   
import dogui.dogui_core as dg

player1=Player(1)
player2=Player(2)
players=[]
players.append(player1)
players.append(player2)


def switch_turns():
    player1.on_turn=player2.on_turn
    player2.on_turn=not player1.on_turn
    
def gui_move_piece():
    if player1.on_turn:    
        player_on_turn=player1
    else:
        player_on_turn=player2
    piece_index=int(entry1.text.get())
    player_on_turn.pieces[piece_index].move(1,1)
    switch_turns()
    #gui1.move()


gui1=dg.GUI()

entry1=dg.Entry(gui1.window,1,1)

button1=dg.Button(gui1.window,"Move",gui_move_piece,1,2)


gui1.build_gui()    


    
