import game_engine

from functools import wraps
import random

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
            if game1.new_game==False:
                game1.play_turn()
            else:
                initialize_game()
            
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
    
    def validate_on_turn(self):
        if self.owner==game1.player_on_turn:
            return(True)
        else:
            return(False)
        
    
    def validate_grid(self,row,col):
        valid=max(self.row+row,self.col+col,7-(self.row+row),7-(self.col+col))<=7
        return(valid)
    
    def try_relative_move(self,row,col):
        if self.validate_correctness(row,col,False):           
            if(self.validate_on_turn()):
                self.relative_move(row,col)
                self.update_piece_label()
                game1.player_on_turn=int(not(bool(game1.player_on_turn-1)))+1
                print("Player on turn:",game1.player_on_turn)
        self.selected=False
           
    def relative_move(self,row,col):
        print("REL",self.row,self.col)
        self.row+=row
        self.col+=col
        print("REL",self.row,self.col)
        
    def validate_collisions(self,row,col,test_mode):
        steps=max(abs(row),abs(col),1) #1 to not divide by zero
        row_unit=row/steps
        col_unit=col/steps
        for i in range(1,steps+1):
            target_piece=get_piece_on_tile(self.row+i*row_unit,self.col+i*col_unit)
            #try:
            #    owner=target_piece.owner
            #except:
            #    owner=""
            #print(target_piece,i,steps,owner,self.owner)
            if(target_piece is not None and i<steps):
                return(False)
            elif(target_piece is not None and i==steps):
                if target_piece.owner!=self.owner and game1.player_on_turn==self.owner:
                    print("KILLER",self)#,"SEARCH MODE",search_mode)
                    if not test_mode:
                        print(target_piece,"DIES")
                        target_piece.die()
                else:
                    return(False)
        return(True)
    
    def die(self):
        index=game1.pieces.index(self)
        game1.pieces.pop(index)
        
    def get_search_space(self):
        for i in range(8):
            for j in range(8):
                return([i,j])
            
    def validate_correctness(self,row,col,test_mode):
        correct=False
        print("VALID_RELATIVE_MOVE",self.validate_relative_move(row,col))
        print("VALID_GRID",self.validate_grid(row,col))
        if self.validate_relative_move(row,col) and self.validate_grid(row,col):
            #print("VALID_COLLISION",self.validate_collisions(row,col,test_mode))
            if self.validate_collisions(row,col,test_mode):
                correct=True
        return(correct)
        
 
class Pawn(Piece):
    def validate_relative_move(self,row,col):
        target_piece=get_piece_on_tile(self.row+row,self.col+col)
        if target_piece is not None:
            owner=target_piece.owner
        else:
            owner=0
        direction=(self.owner-1)*2-1 #-1 white, 1 black
        valid=(row==direction*1 or (row==direction*2 and self.row==3.5-direction*2.5)) and ((col==0 and owner==0) or (abs(col)==1 and owner not in [0,self.owner]))
        return(valid)
    
    def promote(self):
        self.__class__=Queen
        self.init_piece_label()
    
    def try_relative_move(self,row,col):
        if self.validate_correctness(row,col,False):
            if self.validate_on_turn():
                self.relative_move(row,col)
                player_direction=(self.owner-1)*2-1 #-1 white, 1 black
                if(self.row==3.5+player_direction*3.5):
                    print("PROMOTED")
                    self.promote()
                self.update_piece_label()
                game1.player_on_turn=int(not(bool(game1.player_on_turn-1)))+1
                print("Player on turn:",game1.player_on_turn)
        self.selected=False       
        
    def get_search_space(self):
        player_direction=(self.owner-1)*2-1 #-1 white, 1 black
        search_space=[[player_direction,0],[player_direction,1],[player_direction,-1],[2*player_direction,0]]
        for i in range(len(search_space)):
            search_space[i][0]+=self.row
            search_space[i][1]+=self.col
        return(search_space)
        
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
        
    def get_search_space(self):
        search_space=[]
        for i in range(8):
            search_space.append([self.row,i])
            search_space.append([i,self.col])
        this_position=[self.row,self.col]
        search_space.pop(search_space.index(this_position))
        search_space.pop(search_space.index(this_position))
        return(search_space)
         
class Knight(Piece):
    def validate_relative_move(self,row,col):
        valid=row*row+col*col==5 #haha discrete circle
        return(valid)   
    
    def get_search_space(self):
        search_space=[]
        for i in [-2,-1,1,2]:
            for j in [-2,-1,1,2]:
                search_space.append([self.row+i,self.col+j])
        return(search_space)

class Bishop(Piece):
    def validate_relative_move(self,row,col):
        valid=(abs(row)==abs(col))
        return(valid)
    
    def get_search_space(self):
        search_space=[]
        for i in range(8):
            search_space.append([self.row-self.col+i,i]) #1st diagonal
            search_space.append([self.row+self.col-i,i]) #2nd diagonal
        this_position=[self.row,self.col]
        search_space.pop(search_space.index(this_position))
        search_space.pop(search_space.index(this_position))
        return(search_space)

class Queen(Piece):
    def validate_relative_move(self,row,col):
        valid=abs(row)==abs(col) or col==0 or row==0
        return(valid)
    
    def get_search_space(self):
        search_space=[]
        for i in range(8):
            search_space.append([self.row,i])
            search_space.append([i,self.col])
            search_space.append([self.row-self.col+i,i]) #1st diagonal
            search_space.append([self.row+self.col-i,i]) #2nd diagonal
        this_position=[self.row,self.col]
        search_space.pop(search_space.index(this_position))
        search_space.pop(search_space.index(this_position))
        search_space.pop(search_space.index(this_position))
        search_space.pop(search_space.index(this_position))
        return(search_space)
    
class King(Piece):
    def __init__(self,row,col,owner):
        super().__init__(row,col,owner)
        self.moved=False
    
    def validate_relative_move(self,row,col):
        valid=max([abs(row),abs(col)])<=1 #manhattan norm
        if self.moved==False and abs(col)==2 and row==0: #for both players
            valid_right=self.castling(row,col,3)
            valid_left=self.castling(row,col,-4)
            print(valid_right,valid_left)
            valid=valid_right or valid_left
        return(valid)
    
    def castling(self,col,row,rook_relative_col):
        valid=False
        castling=True
        sign=int(rook_relative_col>0)*2-1
        for i in range(sign,rook_relative_col,sign):
            castling=self.check_tile_for_castling(castling,i)
        target_piece=get_piece_on_tile(self.row,self.col+rook_relative_col)
        if target_piece is None:
            castling=False  
        elif not (isinstance(target_piece,Rook) and target_piece.owner==self.owner and target_piece.moved==False):
            castling=False
        if castling==True:
            valid=True
        return(valid)
    
    def check_tile_for_castling(self,castling,relative_col):
        target_piece=get_piece_on_tile(self.row,self.col+relative_col)
        if target_piece is None:
            castling=False
        return(castling)
           
    def relative_move(self,row,col):
        if row==0 and col==2: #validation done
            target_piece=get_piece_on_tile(self.row,self.col+3)
            target_piece.relative_move(0,-2)        
            target_piece.init_piece_label()
            
        elif row==0 and col==-2: #validation done
            target_piece=get_piece_on_tile(self.row,self.col-4)
            target_piece.relative_move(0,3)        
            target_piece.init_piece_label()
            
        self.row+=row
        self.col+=col
        self.moved=True  
        
    def die(self):
        game1.new_game=True
        #super().die()
        
    def get_search_space(self):
        search_space=[]
        for i in range(-1,2):
            for j in range(-1,2):
                search_space.append([self.row+i,self.col+j])
        search_space.append([self.row,self.col-2])
        search_space.append([self.row,self.col+2])
        this_position=[self.row,self.col]
        search_space.pop(search_space.index(this_position))
        return(search_space)


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
        self.new_game=False
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

    
    def play_turn(self):

        print(self.pieces)
        current_pieces=[x for x in self.pieces if x.owner==self.player_on_turn]
        current_player=self.player_on_turn
        total_search_space=[]
        for i in range(len(current_pieces)):
            piece=current_pieces[i]
            search_space=piece.get_search_space()
            for j in range(len(search_space)-1,-1,-1):
                print("")
                valid=piece.validate_correctness(search_space[j][0]-piece.row,search_space[j][1]-piece.col,True)
                if not valid:
                    search_space.pop(j)
            total_search_space.append(search_space)
            #print(len(search_space))
                
        
            
        #print("TOTAL SEARCH SPACE",len(total_search_space),total_search_space)
        if self.player_on_turn==2:
            k=0
            tile_dict={}
            for i in range(len(total_search_space)):
                for j in range(len(total_search_space[i])):
                    tile_dict[k]=[i,j]
                    k+=1
            #print("TURN",k)
            
            choice=random.randint(0,k-1)
            i=tile_dict[choice][0]
            j=tile_dict[choice][1]
            #print(i,j)
            chosen_piece=current_pieces[i]
            chosen_move=total_search_space[i][j]
            
            print("MOVING",chosen_piece,"TO TILE:",chosen_move)
            chosen_piece.try_relative_move(chosen_move[0]-chosen_piece.row,chosen_move[1]-chosen_piece.col)

            

#game1=Game()    
 

def initialize_game():
    print("NEW GAME")
    global game1
    game1=Game()

initialize_game()    
c=game_engine.Col()  

def initialize_grids(grids):
    grids.append(game_engine.Grid(8,8,position=[POSITION_X,POSITION_Y],cell_size=[CELL_SIZE_X,CELL_SIZE_Y],colors=[c.white,c.green]))
    grid=grids[0]
    for i in range(len(grid.grid)):
        for j in range(len(grid.grid[i])):
            if((i+j)%2==1):
                grid.grid[i][j]=1
    return(grids)