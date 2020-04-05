import game_engine

from functools import wraps


def evaluate_click(grids,click):
    grid=grids[0]
    row,col=grid.evaluate_row_column_indices(click)
    move_or_mark_selected_piece(row,col)
    print(game1.pieces)
    return(row,col)
        
def mark_selected_piece(row,col):
    piece=get_piece_on_tile(row,col)
    if piece is not None:
        piece.selected=True
        print(piece)
        
def move_or_mark_selected_piece(row,col):
    for piece in game1.pieces:
        if piece.selected==True:
            piece.try_relative_move(row-piece.row,col-piece.col)
            return(8,8) #either move or mark
    mark_selected_piece(row,col)
    
            
def get_piece_on_tile(row,col):
    for piece in game1.pieces:
        if piece.row==row and piece.col==col:
            return(piece)
    return(None)

##################### CHESS Game Mechanics ########################
   
class Piece:
    def __init__(self,row,col,owner):
        self.row=row
        self.col=col
        self.owner=owner
        self.selected=False
        self.init_piece_label()
        
    def init_piece_label(self):
        if self.owner==1:
            owner_label="White"
        else:
            owner_label="Black"
        piece_name=self.__class__.__name__
        self.piece_label=game_engine.Label([3+POSITION_X+self.col*(CELL_SIZE_X+MARGIN),30+POSITION_Y+self.row*(CELL_SIZE_Y+MARGIN)],owner_label+" "+piece_name,fontsize=10)
   
    def update_piece_label(self):
        self.piece_label.position=[3+POSITION_X+self.col*(CELL_SIZE_X+MARGIN),30+POSITION_Y+self.row*(CELL_SIZE_Y+MARGIN)]

    def move(self,steps,direction): #direction = 1 ahead then clockwise to 8        
        if direction in [8,1,2]:
            self.row-=steps
        elif direction in [4,5,6]:
            self.row+=steps
        if direction in [2,3,4]:
            self.col+=steps
        elif direction in [6,7,8]:
            self.col-=steps

    def validate_relative_move(self,row,col):
        valid=True
        return(valid)
    
    def validate_grid(self,row,col):
        valid=max(self.row+row,self.col+col,7-(self.row+row),7-(self.col+col))<=7
        return(valid)
    
    def try_relative_move(self,row,col):
        print(self.validate_relative_move(row,col))
        if self.validate_relative_move(row,col) and self.validate_grid(row,col):
            if self.validate_collisions(row,col):
                self.relative_move(row,col)
                self.update_piece_label()
        self.selected=False
           
    def relative_move(self,row,col):
        self.row+=row
        self.col+=col
        
    def validate_collisions(self,row,col):
        steps=max(abs(row),abs(col),1) #1 to not divide by zero
        row_unit=row/steps
        col_unit=col/steps
        for i in range(1,steps+1):
            target_piece=get_piece_on_tile(self.row+i*row_unit,self.col+i*col_unit)
            try:
                owner=target_piece.owner
            except:
                owner=""
            print(target_piece,i,steps,owner,self.owner)
            if(target_piece is not None and i<steps):
                return(False)
            elif(target_piece is not None and i==steps):
                if target_piece.owner!=self.owner:
                    target_piece.die()
                else:
                    return(False)
        return(True)
    
    def die(self):
        index=game1.pieces.index(self)
        game1.pieces.pop(index)
        
 
class Pawn(Piece):
    def validate_relative_move(self,row,col):
        target_piece=get_piece_on_tile(self.row+row,self.col+col)
        if target_piece is not None:
            owner=target_piece.owner
        else:
            owner=0
        #print(owner)
        direction=(self.owner-1)*2-1 #-1 white, 1 black
        valid=(row==direction*1 or (row==direction*2 and self.row==3.5-direction*2.5)) and ((col==0 and owner==0) or (abs(col)==1 and owner not in [0,self.owner]))
        #print(self.owner)
        #print(abs(col)==1)
        #print(owner not in [0,self.owner])
        
        return(valid)
    
    def promote(self):
        self.__class__=Queen
        self.init_piece_label()
        self.update_piece_label()
        
        #game1.pieces.append(Queen(self.row,self.col,self.owner))
        #self.die()
    def try_relative_move(self,row,col):
        print(self.validate_relative_move(row,col))
        if self.validate_relative_move(row,col) and self.validate_grid(row,col):
            if self.validate_collisions(row,col):
                self.relative_move(row,col)
                player_direction=(self.owner-1)*2-1 #-1 white, 1 black
                if(self.row==3.5+player_direction*3.5):
                    print("PROMOTED")
                    self.promote()
                self.update_piece_label()
        self.selected=False        
        

class Rook(Piece):
    def __init__(self,row,col,owner):
        super().__init__(row,col,owner)
        self.moved=False
        
    def validate_relative_move(self,row,col):
        valid=(row==0 or col==0)
        return(valid)
    
    def relative_move(self,row,col):
        self.row+=row
        self.col+=col
        self.moved=True
   
class Knight(Piece):
    def validate_relative_move(self,row,col):
        valid=row*row+col*col==5 #haha discrete circle
        return(valid)    

class Bishop(Piece):
    def validate_relative_move(self,row,col):
        valid=(abs(row)==abs(col))
        return(valid)

class Queen(Piece):
    def validate_relative_move(self,row,col):
        valid=abs(row)==abs(col) or col==0 or row==0
        return(valid)
    
class King(Piece):
    def __init__(self,row,col,owner):
        super().__init__(row,col,owner)
        self.moved=False
    
    def validate_relative_move(self,row,col):
        valid=max([abs(row),abs(col)])<=1 #manhattan norm
        #if self.moved==False and col=2:
            
    def relative_move(self,row,col):
        self.row+=row
        self.col+=col
        self.moved=True        
    

        

 


########################## Game initialization ##########################

CELL_SIZE_X=60
CELL_SIZE_Y=60
POSITION_X=15
POSITION_Y=50
MARGIN=1

class Game:
    def __init__(self):
        self.player_on_turn=1
        self.pieces=[]
        for i in range(8):
            self.pieces.append(Pawn(6,i,1))
        for i in [0,7]:
            self.pieces.append(Rook(7,i,1))
        for i in [1,6]:
            self.pieces.append(Knight(7,i,1))
        for i in [2,5]:
            self.pieces.append(Bishop(7,i,1))
        for i in [3] :
            self.pieces.append(Queen(7,i,1))
        for i in [4] :
            self.pieces.append(King(7,i,1))


        for i in range(8):
            self.pieces.append(Pawn(1,i,2))
        for i in [0,7]:
            self.pieces.append(Rook(0,i,2))
        for i in [1,6]:
            self.pieces.append(Knight(0,i,2))
        for i in [2,5]:
            self.pieces.append(Bishop(0,i,2))
        for i in [3] :
            self.pieces.append(Queen(0,i,2))
        for i in [4] :
            self.pieces.append(King(0,i,2))


game1=Game()    
  
c=game_engine.Col()    

def initialize_game():
    game1=Game()
    return(game1)

def initialize_grids(grids):
    grids.append(game_engine.Grid(8,8,position=[POSITION_X,POSITION_Y],cell_size=[CELL_SIZE_X,CELL_SIZE_Y],colors=[c.white,c.green]))
    grid=grids[0]
    for i in range(len(grid.grid)):
        for j in range(len(grid.grid[i])):
            if((i+j)%2==1):
                grid.grid[i][j]=1
    return(grids)