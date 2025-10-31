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
speed = 1
pause = 0.3

def create_level(depth):
    size = depth*2 + 5
    level = [[0]*size]*size
    middle = size//2
    level[middle][middle] = 1

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
    move = int(input())-1
    if move//3 == 2:
        position[1] += speed
    if move//3 == 0:
        position[1] -= speed
    if move % 3 == 2:
        position[0] += speed
    if move % 3 == 0:
        position[0] -= speed
    if position[0] < 0 or position[1] < 0 or position[0] > 4 or position[1] > 4:
        lose()

input()
