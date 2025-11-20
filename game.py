from time import sleep, time
import random as r

def lose():
    global gameRunning
    gameRunning = 0
    pause = 0.3
    print('        \033[1;91m', end='')
    sleep(pause)
    for i in "YOU LOSE":
        print(i, end='')
        sleep(pause)
    print('\033[0m')

def win():
    global gameRunning
    gameRunning = 0
    pause = 0.3
    print('        \033[1;92m', end='')
    sleep(pause)
    for i in "YOU WIN":
        print(i, end='')
        sleep(pause)
    print('\033[0m')

def generate_folder(address, depth, seed, treasurecount):
    r.seed(seed)
    for i in range(r.randint(2,4)):
        pull = r.randint(1, 100)
        if pull <= 91 - depth*30:
            address.append([])
            treasurecount += generate_folder(address[-1], depth+1, seed+1, treasurecount)
        elif pull == 92 - depth*30:
            if treasurecount < 1:
                address.append('treasure.txt')
                treasurecount += 1
            else:
                address.append('win_button.txt')
        elif pull <= 96 - depth*15:
            address.append('atkbonus.txt')
        else:
            address.append('monster.txt')
    return treasurecount

def generate_world(seed):
    world = ['readme.txt']
    if generate_folder(world, 0, seed, 0) == 0:
        world.append('treasure.txt')
    return world

player = {'health':3, 'attack':1, 'wincon':0}
gameRunning = 1

while gameRunning:
    seed = time()
    world = generate_world(int(seed))
    # The rest of the game loop would go here, handling player actions and interactions with the generated world.
    print(world)  # Placeholder to show the generated world structure
    action = input().lower()
    if action in ['q', 'quit']:
        lose()
    if player['health'] <= 0:
        lose()
    if player['wincon'] == 1:
        win()
