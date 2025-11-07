import time as t
import math as m
import random as r

#╒═╤═╕ ┌─┬─┐
#│ │ │ │ │ │
#╞═╪═╡ ├─┼─┤
#│ │ │ │ │ │
#╘═╧═╛ └─┴─┘



position = [-1, -1]
previous_position = [-1, -1]
gameRunning = 1
pause = 0.3
depth = 0
size = 0
level = []
player = {'health':0, 'speed':1}


def create_level(size):
    level = [[0]*size]*size
    middle = size//2
    level[middle][middle] = 1
    return level

def damage_player(damage):
    return 1
def lose():
    global gameRunning
    gameRunning = 0
    print("\033[1;91m        ", end='')
    t.sleep(pause)
    print("Y", end='')
    t.sleep(pause)
    print("O", end='')
    t.sleep(pause)
    print("U", end='')
    t.sleep(pause)
    print(" ", end='')
    t.sleep(pause)
    print("L", end='')
    t.sleep(pause)
    print("O", end='')
    t.sleep(pause)
    print("S", end='')
    t.sleep(pause)
    print("E", end='')
    t.sleep(pause)
    print("\033[0m")

while gameRunning:
    if size != depth*2 + 5 or len(level) == 0:
        size = depth*2 + 5
        level = create_level(size)
    action = int(input())-1
    if action == 0:
    elif action > 8:
    else:
        if action//3 == 2:
            position[1] += player['speed']
        if action//3 == 0:
            position[1] -= player['speed']
        if action % 3 == 2:
            position[0] += player['speed']
        if action % 3 == 0:
            position[0] -= player['speed']
        if position[0] < 0 or position[1] < 0 or position[0] > size or position[1] > size:
            lose()
        if 0 == level[position[0]][position[1]]:
            depth += 1
            damage_player(r.randint(1, 8))

input()
