def evaluate_click(grids,click):
    map_grids=[grids[0]]
    for grid in map_grids:
        row,column=grid.evaluate_row_column_indices(click)
        print(row,column)
        #grid.
        
##################### CHESS Game Mechanics ########################
        
        

class Piece:
    def __init__(self,row,col,piece_type,player):
        self.row=row
        self.col=col
        self.piece_type=piece_type
        self.player=player
        
    def move(self,steps,direction): #direction = 1 ahead then clockwise to 8        
        move_mouse_in_grid(self.row,self.col,self.player.number)
        if direction in [1,2,8]:
            base_rows=1
        elif direction in [3,7]:
            base_rows=0
        else:
            base_rows=-1
        if direction in [2,3,4]:
            base_cols=1
        elif direction in [1,5]:
            base_cols=0
        else:
            base_cols=-1
            
        self.validate_move()
        drag_mouse(base_rows*steps,base_cols*steps)
        self.row+=base_rows*steps
        self.col+=base_cols*steps
        
    def validate_move(self,grid):
        if piece_type == 'P':
            if step == 1 
                if direction == 1:
                    return(True)
                if direction==2:
                    if grid[self.x+1][self.y+1]=='P': #Todo Add Black (other player's pawn)
                        return(True)
                if direction==8:
                    if grid[self.x+1][self.y-1]=='P': #Todo Add Black (other player's pawn)
                        return(True)
            
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
    steps=int(entry2.text.get())
    direction=int(entry3.text.get())
    player_on_turn.pieces[piece_index].move(steps,direction)
    switch_turns()
    #gui1.move()
    
    grid=[]
    for i in range(8):
        grid.append([])
        for j in range(8):
            has_piece=False
            for piece in player1.pieces:
                if piece.row==i+1 and piece.col==j+1:
                    grid[i].append(piece.piece_type)
                    has_piece=True
            if not has_piece:
                grid[i].append("/")
    print(grid)
                    
                