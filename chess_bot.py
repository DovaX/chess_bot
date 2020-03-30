import pynput.mouse
import pynput.keyboard
import time
#from pynput import Button, Controller


################# MOUSE CONTROLLING #######################


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
