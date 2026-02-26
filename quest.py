import random as r
from time import time

player = {"health":7, "damage":3, "has_treasure":0}
dungeon = []
GameRunning = 1

def lose():
    print("\033[31mYOU LOSE\033[0m")
    global GameRunning
    GameRunning = 0

def win():
    print("\033[32mYOU WIN\033[0m")
    global GameRunning
    GameRunning = 0

def battle(enemy):
    turn = r.randint(0, 1) 
    enemy[0] = int(enemy[0]) #enemy health
    enemy[1] = int(enemy[1]) #enemy damage
    while min(player["health"], enemy[0]) > 0: #player and the enemy take alternating turns until one of them dies
        if 0 == turn:
            enemy[0] -= player["damage"]
            print(f"You deal {player["damage"]} damage to the monster!")
            turn = 1
        else:
            player["health"] -= enemy[1]
            print(f"The enemy deals {enemy[1]} damage!")
            turn = 0
    
    if enemy[0] <= 0:
        health_increase = r.randint(1, min(4, enemy[1]))
        damage_increase = r.randint(1, 2)
        player["damage"] += damage_increase
        player["health"] += health_increase
        print(f"You won the battle! You receive \033[32m{health_increase} health\033[0m and \033[32m{damage_increase} damage\033[0m!")
        return 1
    else:
        print("You lost...")
        lose()
        return 0

def see_room(room):
    print("\033[96m-------------------------------\033[0m")
    doors_out = 0
    if depth == 1:
        print("\033[35mThe entrance to the dungeon looms behind you.\033[0m")
    elif depth == 2:
        print("\033[35mThe entrance to the dungeon is still visible, but it's getting further.\033[0m")
    elif depth == 3:
        print("\033[35mYou don't see the entrance anymore, but you are sure you can go back the way you came.\033[0m")
    elif depth == 4:
        print("\033[35mYou are deep in the dungeon, but you can still go back the way you came.\033[0m")
    elif depth == 5 and doors_out > 0:
        print("\033[35mYou are very deep in the dungeon. Does it ever end?\033[0m")
    elif depth == 5 and doors_out == 0:
        print("\033[35mYou are very deep in the dungeon. However, it seems like there are no more ways to go deeper...\033[0m")
    else:
        print("\033[35mYou have a feeling this is the end of the dungeon... Nothing can be deeper than this.\033[0m")
    if len(room):
        length = len(room)
        for i in range(length):
            if isinstance(room[doors_out], list):
                doors_out += 1
                continue
            entity = list(room.pop(doors_out).split())
            if entity[0] == "enemy":
                print("There's an \033[31menemy\033[0m in the room! It charges straight at you!")
                print("You begin the \033[31mbattle\033[0m...")
                if(battle(entity[1:]) != 1):
                    global GameRunning
                    GameRunning = 0
                    return 0
            elif entity[0] == "treasure":
                print("There's \033[1;93mthe relic\033[0m in the room!")
                print("You quickly pocket it.")
                print("Now you just need to \033[95mget out\033[0m...")
                player["has_treasure"] = 1
            elif entity[0] == "health_potion":
                print("There's a \033[32mhealth potion\033[0m in the room!")
                print("You drink it. \033[32mYour health increases.\033[0m")
                player["health"] += 2
            elif entity[0] == "weapon":
                print("There's a \033[32mbetter weapon\033[0m in the room!")
                print("You feel \033[32mmore dangerous\033[0m now.")
                player["damage"] += 1
        
        if doors_out == 0:
            input("There are no ways out of this room. You can only go back...")
            return 0
        elif doors_out == 1:
            print("There is 1 way out of this room. You can also go back...")
        else:
            print(f"There are {doors_out} ways out of this room. You can also go back...")
        chosen_way = -1
        while chosen_way not in range(0, doors_out+1):
            try:
                chosen_way = int(input(f"Choose a way to go (enter a number from 0 (go back) to {doors_out}): "))
            except ValueError:
                print("That's not a valid number. Please try again.")
        return chosen_way
    else:
        input("The room is \033[90mempty\033[0m and it's a \033[90mdead end\033[0m. Perhaps you should go back...")
        return 0

def generate_dungeon():
    dungeon.append([])
    address = dungeon[0]
    r.seed(int(time()))
    maxdepth = r.randint(5, 7)
    moveorder = [1] #this list is a sequence of depths of the rooms
    iteration = 0
    treasure_added = 0
    while iteration < len(moveorder):
        depth = moveorder[iteration]
        item_count = 2 + r.randint(1, 10)//3 #how many items are there in the room, including ways to other rooms
        items = list(range(item_count))
        for j in items:
            new_room = []
            pull = r.randint(1, 100)
            if depth < 3:
                if pull <= 99-32*j: #the more times we try to create rooms, the less chance of creating a room is.
                                    #this also prevents potentially infinite generations
                    pull2 = r.randint(1, 100)
                    if pull2 <= 55:
                        items.append(items[-1] + 1) #to create many ways, we add another item to the current room
                                                    # this works because every item is actually a door to other rooms
                    elif pull2 <= 85:
                        new_room.append(f"enemy {r.randint(max(depth-2, 1), max(depth+1, 4))} {r.randint(1, 3)}")
                        #enemy with health between depth-1 and depth+2 (but no less than 1), and damage between 1 and 3
                    elif pull2 <= 95:
                        new_room.append("health_potion")
                    else:
                        new_room.append("weapon")
                    address.append(new_room)
                else:
                    if 0 == treasure_added:
                        new_room.append("treasure")
                        treasure_added = 1
                    address.append(new_room)
            else:
                if pull <= 90-20*j:
                    if depth <= maxdepth:
                        pull2 = r.randint(1, 10)
                        new_room = []
                        if pull2 < 3:
                            items.append(items[-1] + 1)
                        elif pull2 < 7:
                            new_room.append(f"enemy {r.randint(max(depth, 4), max(2*depth+1, 7))} {r.randint(3, 5)}")
                        elif pull2 < 9:
                            new_room.append("health_potion")
                        else:
                            new_room.append("weapon")
                        address.append(new_room)
                    else:
                        if 0 == treasure_added:
                            address.append("treasure")
                            treasure_added = 1
                        return 0
                else:
                    if 0 == treasure_added:
                        address.append("treasure")
                        treasure_added = 1
        
        address = new_room
        if depth == moveorder[-1]:
            moveorder.append(iteration+1)
        else:
            moveorder.insert(iteration+1, depth+1)
        iteration += 1
    if 0 == treasure_added:
        address = dungeon[0]
        rooms_deeper = [0]
        while rooms_deeper:
            rooms_deeper = []
            for i in range(len(address)):
                if isinstance(address[i], list):
                    rooms_deeper.append(i)
            if rooms_deeper:
                address = address[r.choice(rooms_deeper)]
        address.append("treasure")        


generate_dungeon()
current_player_position = dungeon[0]
depth = 1
moves = [None]*6
print("\033[95mThe dungeon door opens up, revealing an empty room with many doors leading deeper.")
print("The rumours say there's an ancient \033[93mrelic\033[95m inside, granting many powers to the one who wields it.")
print("You need that treasure. Go find it.\033[0m")
while GameRunning:
    player_action = see_room(current_player_position)
    if player_action == 0:
        current_player_position = dungeon[0]
        if depth == 1:
            if player["has_treasure"]:
                win()
            else:
                print("\033[35mYou can't just walk away without \033[1mthe relic\033[0;35m...\033[0m")
                depth = 1
        else:
            depth -= 1
            for i in range(depth-1):
                current_player_position = current_player_position[moves[i]]
    else:
        current_player_position = current_player_position[player_action-1]
        moves[depth-1] = player_action-1
        depth += 1
