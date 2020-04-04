#different implementations of knight move

import math
def knight_moves(x,y):
    new_positions=[]
    r=math.sqrt(5) #radius of the circle
    for phi in [math.atan(2),math.atan(1/2)]: #angles in radians
        for quadrant in range(4):
            angle=phi+quadrant*math.pi/2 # add 0, 90, 180, 270 degrees in radians      
            new_x=round(x+r*math.cos(angle))
            new_y=round(y+r*math.sin(angle))
            if max(new_x,new_y,7-new_x,7-new_y)<=7: #validation whether the move is in grid
                new_positions.append([new_x,new_y])
    return(new_positions)

def validate_knight_move(x,y,x_0,y_0):
    return((x-x_0)**2+(y-y_0)**2==5)

x_0=2
y_0=4

moves=knight_moves(x_0,y_0)
print(moves)

validation=[validate_knight_move(move[0],move[1],x_0,y_0) for move in moves]
print(validation)

def knight_moves2(x,y):
    new_positions=[]
    for dx in [-2,-1,1,2]:
        for dy in [-2,-1,1,2]:
            if(validate_knight_move(x+dx,y+dy,x,y)): #is knight move?
                if max(x+dx,y+dy,7-(x+dx),7-(y+dy))<=7: #validation whether the move is in grid
                    new_positions.append([x+dx,y+dy])
    return(new_positions)

new_positions=knight_moves2(x_0,y_0)
print(new_positions)
            
def knight_moves3(x,y):
    new_positions=[]
    for dx in [-2,-1,1,2]:
        for dy in [-2,-1,1,2]:
            if abs(dx)+abs(dy)==3:
                new_positions.append([x+dx,y+dy])
    return(new_positions)

new_positions=knight_moves3(x_0,y_0)
print(new_positions)