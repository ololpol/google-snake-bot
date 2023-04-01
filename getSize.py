import time
import pyautogui
import math

#This file aims to calculate the proportions of the field and where on the screen it is located

SCREEN_WIDTH = 1680
SCREEN_HEIGHT = 1050

def localize_color(step, colors, pic):


    for x in range(math.ceil(step/2), SCREEN_WIDTH, step):
        for y in range(math.ceil(step/2), SCREEN_HEIGHT, step):
            color = pic.getpixel((x, y))
            if color in colors:
                return (x,y)
    
    return(-1,-1,-1)

def step(step, field_pos, pic, skip_colors=[]):
    x = field_pos[0]
    y = field_pos[1]
    x_done = step[0] == 0 #False unless 0
    y_done = step[1] == 0
    color = pic.getpixel(field_pos)

    while not(x_done or y_done): #move to bottom right corner of square
        x += step[0]
        field_color = pic.getpixel((x,y))
        if (field_color != color) and field_color not in skip_colors:
            x_done = True
            x -= step[1]

        y += step[1]
        field_color = pic.getpixel((x,y))
        if (field_color != color) and field_color not in skip_colors:
            y_done = True
            y -= step[1]
    return (x,y)
        
if __name__ == "__main__":

    time.sleep(3) #time to tab out
    
    pic = pyautogui.screenshot(region=(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    print("dun")
    field_pos = localize_color(30, [(170, 215, 81), (162, 209, 73)], pic)
    color = pic.getpixel(field_pos)

    sqBottom = step((1,1), field_pos, pic)

    sqTop = step((-1,-1),field_pos, pic)

    square_size = (sqBottom[0]-sqTop[0], sqBottom[1]-sqTop[1])
    print(square_size)

    board_top = step((-square_size[0],-square_size[1]), sqTop, pic, [(170, 215, 81), (162, 209, 73)])
    print(board_top)
    board_right = step((square_size, 0), board_top, pic, [(170, 215, 81), (162, 209, 73)])
    print(board_right)
    board_bot = step((0, square_size), board_top, pic, [(170, 215, 81), (162, 209, 73)])
    print(board_bot)

    board_width = (board_right[0]-board_top[0])/square_size[0]
    board_height = (board_bot[1]-board_top[1])/square_size[1]

    print(board_width, board_height)
    







