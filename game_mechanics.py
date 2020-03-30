import game_engine

from functools import wraps

def evaluate_click(grids,click):
    grid=grids[0]
    row,col=grid.evaluate_row_column_indices(click)
    move_or_mark_selected_piece(row,col)
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
            return #either move or mark
    mark_selected_piece(row,col)
            
def get_piece_on_tile(row,col):
    for piece in game1.pieces:
        if piece.row==row and piece.col==col:
            return(piece)
    return(None)

##################### CHESS Game Mechanics ########################
    
def validate_move(func):
    def function_wrapper(x):
        print("Before calling " + func.__name__)
        func(x)
        print("After calling " + func.__name__)
    return function_wrapper

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
            
    def adjust_validation(f):
        @wraps(f)
        def function_wrapper(instance,row,col):
            return(f(instance,row,col))
        return(function_wrapper)  
    
    @adjust_validation
    def validate_relative_move(self,row,col):
        valid=True
        return(valid)
        
    def try_relative_move(self,row,col):
        if self.validate_relative_move(row,col):    
            self.relative_move(row,col)
            self.update_piece_label()
        self.selected=False
           
    def relative_move(self,row,col):
        self.row+=row
        self.col+=col
   
class Pawn(Piece):
    def adjust_validation(f):
        @wraps(f)
        def function_wrapper(instance,row,col):
            if row==-1 and col==0:    
                return(f(instance,row,col))
            else:
                return(False)
        return(function_wrapper)
    
    @adjust_validation
    def validate_relative_move(self,row,col):
        print(row,col)
        valid=True
        return(valid)

    def try_relative_move(self,row,col):
        print(self.validate_relative_move(row,col))
        if self.validate_relative_move(row,col):    
            self.relative_move(row,col)
            self.update_piece_label()
        self.selected=False
        
    #def adjust_validation(self,function):
    #    def function_wrapper(row,col):
    #        print("Validated before")
    #        function(row,col)
    #        print("Validated after")
    #    return(function_wrapper)

class Rook(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass

class Queen(Piece):
    pass

class King(Piece):
    pass

 


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
                          
game1=Game()
                        
c=game_engine.Col()    
def initialize_labels(labels):
    for i,piece in enumerate(game1.pieces):    
        
        labels.append(piece.piece_label)    
    return(labels)

def initialize_grids(grids):
    grids.append(game_engine.Grid(8,8,position=[POSITION_X,POSITION_Y],cell_size=[CELL_SIZE_X,CELL_SIZE_Y],colors=[c.grey,c.darkgreen]))
    grid=grids[0]
    for i in range(len(grid.grid)):
        for j in range(len(grid.grid)):
            if i+j%2==1:
                grid.grid[i][j]==1
    return(grids)