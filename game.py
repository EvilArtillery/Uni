import time as t
import math as m

╒═╤═╕
│ │ │
╞═╪═╡
│ │ │
╘═╧═╛
─│

═╪╡╤╧╞
╕╘╒╛
position = [-1, -1]
gameRunning = 1
def fight():


while gameRunning:
    move = int(input())-1
    if move//3 == 2:
        position[1] += speed
    if move//3 == 0:
        position[1] -= speed
    if move%3 == 2:
        position[0] += speed
    if move%3 == 0:
        position[0] -= speed
