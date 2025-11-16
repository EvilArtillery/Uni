from time import sleep

def lose():
    global gameRunning
    gameRunning = 0
    pause = 0.3
    print('        \033[1:91m', end='')
    sleep(pause)
    for i in "YOU LOSE":
        print(i, end='')
        sleep(pause)
    print('\033[0m')

player = {'health':3, 'wincon':0}
gameRunning = 1

while gameRunning:
    if input() in ['q', 'quit']:
        lose()
