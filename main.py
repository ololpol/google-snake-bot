import keyboard
import pyautogui
import random
import time
import logging

logger = logging.getLogger("main")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

stream_h = logging.StreamHandler()
stream_h.setLevel(logging.DEBUG)
stream_h.setFormatter(formatter)
logger.addHandler(stream_h)

file_h = logging.FileHandler("logs.log")
file_h.setLevel(logging.INFO)
file_h.setFormatter(formatter)
logger.addHandler(file_h)


# Defining functions

# Moves the snake in given direction.
def move(direction, use_key=True):
    global game_state, apple, facing, direction_decoder, facing_decoder, apple_state
    if use_key:
        keyboard.press(direction_decoder[direction])
        keyboard.release(direction_decoder[direction])
    if facing != direction:
        facing = direction
    snake.insert(0, (x + facing_decoder[direction][0], y + facing_decoder[direction][1]))
    if apple in snake and apple_state:
        apple = ()
        apple_state = -1
    else:
        snake.pop()
    if (snake[0] not in grid) or (snake[0] in snake[1:]):
        print(f"death at ({x}, {y})")

        raise Exception("Program terminated due to death")


# Returns true if a path in given direction and depth is found
def check(direction, pos, depth=1, d=1, checked=[]):
    # False if all paths in given direction is dead at given depth, true if there is a path.
    global check_grid
    p = (pos[0] + facing_decoder[direction][0], pos[1] + facing_decoder[direction][1])  # P=the checked position
    if depth == 0:  # For testing
        return True
    if d == 1:  # Clear list of checked squares when at start of new check iteration
        check_grid.clear()
    if p in checked:  # False if position p already has been checked in current branch
        return False
    if not (p in (safe + snake[(-d):])):  # False if p is not safe to visit
        return False
    if depth == 1:  # If no previous check failed and bottom depth is reached -
        return True  # True because valid continuation found
    if direction == "L":
        return ((
                        check("L", p, depth - 1, d + 1, checked + [p])
                        or check("U", p, depth - 1, d + 1, checked + [p]))
                or check("D", p, depth - 1, d + 1, checked + [p]))
    if direction == "R":
        return ((
                        check("R", p, depth - 1, d + 1, checked + [p])
                        or check("U", p, depth - 1, d + 1, checked + [p]))
                or check("D", p, depth - 1, d + 1, checked + [p]))
    if direction == "U":
        return ((
                        check("L", p, depth - 1, d + 1, checked + [p])
                        or check("R", p, depth - 1, d + 1, checked + [p]))
                or check("D", p, depth - 1, d + 1, checked + [p]))
    if direction == "D":
        return ((
                        check("L", p, depth - 1, d + 1, checked + [p])
                        or check("R", p, depth - 1, d + 1, checked + [p]))
                or check("D", p, depth - 1, d + 1, checked + [p]))
        # Branch in all directions except back at one less depth
        # If one of the branches has a path(True) then the entire expression is valid.


# Displays pythons idea of how the game looks. Useful for debugging.
def display():
    for coord in grid:  # Displaying game
        if coord in snake:
            if snake.index(coord) < 10:
                print(snake.index(coord), end="")
            else:
                print("*", end="")
        elif coord == apple:
            print("a", end="")
        else:
            print("-", end="")
        if coord[0] == width - 1:
            print(" ")
    print("")


def gen_apple():
    global apple, apple_state
    apple = random.choice(list(set(grid) - set(snake)))
    apple_state = 1


# Testing function
def set_apple(x, y):
    global apple, apple_state
    apple = (x, y)
    apple_state = 1


def get_apple():
    global apple, game_state, apple_state
    pic = pyautogui.screenshot(region=(28, 196, 572, 678))
    if pic.getpixel((10, 10))[0] == 51:
        game_state = False
        return
    for pxx in range(16, 16 + (32 * 17), 32):
        for pxy in range(16, 16 + (32 * 15), 32):
            _, _, b = pic.getpixel((pxx, pxy))
            if b == 38:
                apple = ((pxx - 16) / 32, (14 - ((pxy - 16) / 32)))
                apple_state = 1
                return


def get_head():
    global x, y
    pic = pyautogui.screenshot(region=((43 + (x * 32)), 213 + (448 - (y * 32)),
                                       46 + (x * 32), 216 + (448 - (y * 32))))
    #     Screenshot centered at middle of destination square
    if pic.getpixel((1, 1))[2] in range(220, 245):
        return True
    return False


def full_get():
    global game_state, apple_state, snake, apple

    pic = pyautogui.screenshot(region=(28, 207, 572, 687))

    # 207-687 or 198-678
    for pxx in range(16, 16 + (32 * 17), 32):
        for pxy in range(16, 16 + (32 * 15), 32):
            _, _, b = pic.getpixel((pxx, pxy))
            if b in range(241, 245):  # locate head
                if ((pxx - 16) / 32, (14 - ((pxy - 16) / 32))) != head_pos:
                    return True

    return False


# x: 28 - 624(32 px between, start at 44)
# y: 188 - 712(32 Px between, start at 214) or 207-687 for windowed chrome


# -----------------------------------------CONFIG--------------------------------------------------------
start = (4, 7)
facing = "R"  # (L)eft, (R)ight, (U)p, (D)own
length = 4
width = 17
height = 15

# -----------------------------------------SETUP-------------------------------------------------------

apple_state = -1  # false-Apple not found, True - Apple found
grid = [(a, b) for b in reversed(range(height)) for a in range(width)]
result = 0
facing_decoder = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}

direction_decoder = {
    "R": "d",
    "L": "a",
    "U": "w",
    "D": "s"
}

game_state = True
check_grid = []

# Positions of all snake parts, ordered head first, tail last
snake = [(start[0] - n * facing_decoder[facing][0], start[1] - n * facing_decoder[facing][1]) for n in range(length)]
safe = [(-2, -2)]
apple = ()  # not yet on grid

head = snake[0]
x = head[0]
y = head[1]
head_pos = head

# --------------------------------------GAMEPLAY/SIMULATION--------------------------------------------------
if 1 and __name__ == '__main__':
    display()
    time.sleep(2)
    move(facing)
    display()

    try:
        while game_state:
            # Redeclaring variables based on new snake position
            safe = list(set(grid) - set(snake))
            head = snake[0]
            x = head[0]
            y = head[1]
            if apple == () and apple_state > -1:
                get_apple()
            elif apple_state == -1:
                apple_state += 1
            # Calculating next direction to go
            for i in reversed(range(0, 13, 3)):
                # if i == 9: print("base check failed")
                if (apple == () or ((x < apple[0]) or i < 12)) and check("R", head, i):
                    # move("R", False)
                    facing = "R"
                    break
                if (apple == () or ((x > apple[0]) or i < 12)) and check("L", head, i):
                    # move("L", False)
                    facing = "L"
                    break
                if (apple == () or ((y < apple[1]) or i < 12)) and check("U", head, i):
                    # move("U", False)
                    facing = "U"
                    break
                if (apple == () or ((y > apple[1]) or i < 12)) and check("D", head, i):
                    # move("D", False)
                    facing = "D"
                    break
            # wait until snake head is on a new tile, then commit the planned move.
            while 1:
                if get_head():
                    # keyboard.press(direction_decoder[facing])
                    move(facing)
                    head_pos = head
                    break
            # display()
    except KeyboardInterrupt:
        print("Interrupted by user")
        head = snake[0]
    print(check_grid)
    display()
    print(snake)
    print(apple)
    print(len(snake))
set_apple(0, random.randint(1, 8))


while 0:
    safe = list(set(grid) - set(snake))
    head = snake[0]
    x = head[0]
    y = head[1]
    if apple == () and apple_state > -1:
        gen_apple()
    elif apple_state == -1:
        apple_state += 1
    if keyboard.is_pressed("d"):
        move("R", False)
        display()
        time.sleep(0.3)
    if keyboard.is_pressed("a"):
        move("L", False)
        display()
        time.sleep(0.3)
    if keyboard.is_pressed("s"):
        move("D", False)
        display()
        time.sleep(0.3)
    if keyboard.is_pressed("w"):
        move("U", False)
        display()
        time.sleep(0.3)
    if keyboard.is_pressed("c"):
        print(f"check values is R-{check('R', head)}, L-{check('L', head)}, U-{check('U', head)}, D-{check('D', head)}")
        time.sleep(0.3)
