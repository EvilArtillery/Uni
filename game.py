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
    subfoldercount = 0
    for i in range(r.randint(2,4)):
        pull = r.randint(1, 100)
        if pull <= 91 - depth*30:
            # create a uniquely named folder and store children in 'children'
            global_folder_name = f"Folder_{generate_folder.folder_counter}"
            generate_folder.folder_counter += 1
            new_folder = {'name': global_folder_name, 'children': []}
            address.append(new_folder)
            # recurse into the children list
            treasurecount += generate_folder(new_folder['children'], depth+1, seed+2*subfoldercount, treasurecount)
            subfoldercount += 1
        elif pull <= 92 - depth*25:
            if treasurecount < 1:
                address.append('treasure.txt')
                treasurecount += 1
            else:
                address.append('win.txt')
        elif pull <= 96 - depth*15:
            address.append('atkbonus.txt')
        else:
            address.append('monster.txt')
    return treasurecount

def generate_world(seed):
    # world is a list of items: file strings or folder dicts { 'name':..., 'children':[...] }
    world = ['readme.txt']
    # initialize folder counter for unique names
    generate_folder.folder_counter = 1
    if generate_folder(world, 0, seed+1, 0) == 0:
        world.append('treasure.txt')
    return world

def traverse(address, path):
    """Return the directory at `path`.
    `path` is a list of indices leading from the root `address` to the
    target directory. An empty list returns the top-level `address`.
    Returns `None` if the path is invalid or doesn't point to a folder."""
    if not path:
        return address
    idx = path[0]
    if not isinstance(idx, int) or idx < 0 or idx >= len(address):
        return None
    item = address[idx]
    # folder representation is a dict with a 'children' list
    if not isinstance(item, dict) or 'children' not in item:
        return None
    return traverse(item['children'], path[1:])


def get_node(address, path):
    """Return the folder node (dict) for the given path.

    For the root (empty path) return a synthetic node {'name': 'root', 'children': address}.
    Returns None for invalid paths.
    """
    if not path:
        return {'name': 'root', 'children': address}
    idx = path[0]
    if not isinstance(idx, int) or idx < 0 or idx >= len(address):
        return None
    item = address[idx]
    if not isinstance(item, dict) or 'children' not in item:
        return None
    if len(path) == 1:
        return item
    return get_node(item['children'], path[1:])


def get_breadcrumb(address, path):
    if not path:
        return 'C:/'
    parts = []
    cur = address
    for idx in path:
        if not isinstance(idx, int) or idx < 0 or idx >= len(cur):
            return None
        item = cur[idx]
        if not isinstance(item, dict) or 'name' not in item or 'children' not in item:
            return None
        parts.append(item['name'])
        cur = item['children']
    return 'C:/' + '/'.join(parts) + '/'

def open_file(filename, position, player, world):
    current_dir = traverse(world, position)
    if current_dir is None:
        print("\033[91mCurrent directory not found.\033[0m")
        return

    # find filename in current_dir; files are strings, folders are dicts
    found_idx = None
    found_item = None
    for i, item in enumerate(current_dir):
        if isinstance(item, str) and item == filename:
            found_idx = i
            found_item = item
            break
        if isinstance(item, dict) and item.get('name') == filename:
            found_idx = i
            found_item = item
            break
    # not found or found is a folder (can't 'read' a folder)
    if found_idx is None or isinstance(found_item, dict):
        print("\033[91mFile not found.\033[0m")
        return

    if filename == 'readme.txt':
        print("\033[92mWelcome to the game! Here's a basic tutorial you'll absolutely need to win.")
        print("Navigate the file system using 'cd <foldername>' and read files using 'read <filename>'.")
        print("Your goal is to find the treasure file. There's only one in the whole world, so good luck!\033[0m")
    elif filename == 'treasure.txt':
        print("\033[92mYou found a treasure!\033[0m")
        player['wincon'] = 1
    elif filename == 'win.txt':
        print("\033[91mIt's a trap!")
        dmg = r.randint(1, 2+len(position))
        player['health'] -= dmg
        print(f"You lost {dmg} health.\033[0m")
        print(f"\033[94mCurrent health: {player['health']}\033[0m")
    elif filename == 'atkbonus.txt':
        print("You found an attack bonus! Your attack increases by 1.")
        player['attack'] += 1
        print(f"\033[94mCurrent attack: {player['attack']}\033[0m")
    elif filename == 'monster.txt':
        if player['attack'] > r.randint(1,3):
            print("You encountered a monster and \033[92mdefeated it\033[0m!")
            if r.randint(1, 5) == 1:
                print("The monster dropped a health potion! You gain 1 health.")
                player['health'] += 1
        else:
            print("You encountered a monster and \033[91mwere defeated\033[0m!")
            player['health'] -= 1
        print(f"\033[94mCurrent health: {player['health']}\033[0m")
    # delete the file after reading
    try:
        del current_dir[found_idx]
    except Exception:
        # best-effort: if deletion fails, ignore and continue
        pass

    input("Press Enter to continue...")

def print_world(address, depth=0):
    for item in address:
        if isinstance(item, str):
            print('  ' * depth + '- ' + item)
        elif isinstance(item, dict):
            print('  ' * depth + '- ' + item.get('name', 'Folder'))
            print_world(item.get('children', []), depth + 1)
        else:
            print('  ' * depth + '- Unknown')

def print_folder(node_or_list, breadcrumb=None):
    if isinstance(node_or_list, list):
        node = {'name': 'root', 'children': node_or_list}
    else:
        node = node_or_list

    name = node.get('name', 'Folder')
    children = node.get('children', [])

    # header: use breadcrumb if provided, otherwise folder name
    header = breadcrumb if breadcrumb is not None else name

    print("\033[95mA list of commands:"
          "\nread <filename>"
          "\ncd <foldername>\033[0m")

    print(f"\033[1;96m{header}\033[0m")

    print("\033[1;93m..\033[0m")

    # list children
    for item in children:
        if isinstance(item, dict):
            print(item.get('name', 'Folder'))
        elif isinstance(item, str):
            print(item)
        else:
            print('Unknown')

player = {'health':3, 'attack':1, 'wincon':0}
position = []  # path of indices from root to current folder
gameRunning = 1
seed = time()
world = generate_world(int(seed))

while gameRunning:
    # The rest of the game loop would go here, handling player actions and interactions with the generated world.
    # print_world(world) # For debugging: print the entire world structure
    node = get_node(world, position)
    if node is None:
        print("\033[91mCurrent directory not found.\033[0m")
    else:
        breadcrumb = get_breadcrumb(world, position)
        if breadcrumb is None:
            breadcrumb = node.get('name', 'Folder')
        print_folder(node, breadcrumb)
    action = list(input().split())
    if action[0] in ['q', 'quit']:
        lose()
    elif action[0] == 'cd' and len(action) > 1:
        if action[1] == '..':
            if position:
                position.pop()
            else:
                input("\033[93mAlready at root.\nPress Enter to continue...\033[0m")
        else:
            current_dir = traverse(world, position)
            if current_dir is None:
                print("\033[91mCurrent directory not found.\033[0m")
            else:
                found_idx = None
                for i, item in enumerate(current_dir):
                    if isinstance(item, dict) and item.get('name') == action[1]:
                        found_idx = i
                        break
                if found_idx is None:
                    print("\033[91mFolder not found.\033[0m")
                else:
                    # ensure it's a folder (dict with children)
                    if isinstance(current_dir[found_idx], dict) and 'children' in current_dir[found_idx]:
                        position.append(found_idx)
                    else:
                        print("\033[91mNot a folder.\033[0m")
    elif action[0] == 'read' and len(action) > 1:
        open_file(action[1], position, player, world)
    else:
        print("\033[91mUnknown command. Try \"read readme.txt\".\033[0m\n\n")
    if player['health'] <= 0:
        lose()
    if player['wincon'] == 1:
        win()
