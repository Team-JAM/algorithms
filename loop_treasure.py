from optimized_path import optimized_path
from optimized_travel import optimized_travel
from utils import Queue
import sys
import time
import json
import requests
import random

if len(sys.argv) != 3:
    print('Usage: loop_treasure.py player mode')
    sys.exit(1)

player = sys.argv[1]

if player == 'allison' or player == 'a':
    token = 'b183cb414e3eae854e3930946d0c9370040ea416'
elif player == 'matthew' or player == 'm':
    token = 'a42506e85baef70dd9c66a7d0c090b10a3af26f8'
elif player == 'jonathan' or player == 'j':
    token = '3e4095700cd0b276081a3ac8d4ae04e54a89b92e'

mode = sys.argv[2]

if mode == 's' or mode == 'sell':
    mode = 'sell'
elif mode == 't' or mode == 'transmogrify':
    mode = 'transmogrify'
elif mode == 'w' or mode == 'walk':
    mode = 'walk'
else:
    print("Error: mode not recognized")
    sys.exit(1)

base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
headers = {"Authorization": f"Token {token}"}

STORE = 1
TRANSMOGRIFIER = 495

# load room data
with open('all_rooms.json') as f:
    all_rooms = json.load(f)

def gather_treasure(path):
    time_for_next_action = time.time()

    for heading in path:
        payload = {'direction': heading[0], 'next_room_id': str(heading[1])}
        # sleep for cooldown
        time.sleep(max(time_for_next_action - time.time(), 0))
        # move
        r = requests.post(f'{base_url}fly/', headers=headers, json=payload)
        items = r.json()['items']
        print(f"entered room {r.json()['room_id']}")
        print(f"message: {r.json()['messages']}")
        print(f"items: {items}")
        print(f"errors: {r.json()['errors']}")
        print('-----')
        # set cooldown
        time_for_next_action = time.time() + r.json()['cooldown']
        # # check for items
        if len(items) > 0:
            print(f'Items found! {items}')
            # sleep for cooldown
            time.sleep(max(time_for_next_action - time.time(), 0))
            for item in items:
                # take item
                payload = {"name": item}
                # sleep for cooldown
                time.sleep(max(time_for_next_action - time.time(), 0))
                r = requests.post(f'{base_url}take/', headers=headers, json=payload)
                print(f'I picked up {item}')
                # set cooldown
                time_for_next_action = time.time() + r.json()['cooldown']
                # sleep for cooldown
                time.sleep(max(time_for_next_action - time.time(), 0))
                # check player status 
                r = requests.post(f'{base_url}status/', headers=headers)
                print(f"Inventory: {r.json()['inventory']}")
                cooldown = r.json()['cooldown']
                encumbrance = r.json()['encumbrance']
                strength = r.json()['strength']
                time.sleep(cooldown)
                if encumbrance >= strength - 1:
                    if encumbrance > strength - 1:
                        # drop an item if carrying too much
                        payload = {"name": item}
                        r_drop = requests.post(f'{base_url}drop/', headers=headers, json=payload)
                        print(f"You're carrying too much, so you dropped the {item}")
                        # set cooldown
                        time_for_next_action = time.time() + r_drop.json()['cooldown']
                        # sleep for cooldown
                        time.sleep(max(time_for_next_action - time.time(), 0))
                    if mode == 'sell':
                        sell_items(heading[1], r.json()['inventory'])
                        return "sell"
                    elif mode == 'transmogrify':
                        transmogrify_items(heading[1], r.json()['inventory'])
                        return "transmogrfy"
                    else:
                        # mode is walk, so we're gonna stop here
                        print("Inventory full, stopping walk")
                        sys.exit(0)
    time.sleep(max(time_for_next_action - time.time(), 0))
    print('Finished walking.')

    # if good jacket or pair of boots, wear item
    # if encumbered, put down smallest item until unencumbered, initiate sell mode
        # do not put down boots or jacket if they could be upgrade for other players

def sell_items(current_room, inventory):
    print('Ready to sell!')
    # sell mode
    # get path to store
    if current_room != STORE:
        path = optimized_path(all_rooms, current_room, STORE)
        # walk to store
        optimized_travel(path, token, base_url, headers)
    # sell treasure
    for item in inventory:
        payload = {'name': item, 'confirm': 'yes'}
        r = requests.post(f'{base_url}sell/', headers=headers, json=payload)
        print(f"Sold the {item}")
        time.sleep(r.json()['cooldown'])

    r = requests.post(f'{base_url}status/', headers=headers)
    print(f"Gold: {r.json()['gold']}")
    cooldown = r.json()['cooldown']
    time.sleep(cooldown)

def transmogrify_items(current_room, inventory):
    print('Ready to transmogrify!')
    # get path to transmogrifier
    if current_room != TRANSMOGRIFIER:
        path = optimized_path(all_rooms, current_room, TRANSMOGRIFIER)
        # walk to store
        optimized_travel(path, token, base_url, headers)
    # check lambda coin balance
    r = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/', headers=headers)
    message = r.json()['messages'][0]
    balance = int(message[22:24])
    print(message)
    time.sleep(r.json()['cooldown'])
    # transmogrify treasure
    for item in inventory:
        if balance > 0:
            payload = {'name': item}
            r = requests.post(f'{base_url}transmogrify/', headers=headers, json=payload)
            print(r.json()['messages'][0])
            balance -= 1
            time.sleep(r.json()['cooldown'])
        else:
            print("You're out of Lambda coins :(")
            sys.exit(2)

def get_directions(starting_room, destination_room, all_rooms):
    # Create an empty queue
    queue = Queue()
    # Add a path for starting_room_id to the queue
    # Add a second option that recalls to room zero first
    # paths will contain tuple of (direction, room_id)
    queue.enqueue([(None, starting_room)])
    # queue.enqueue([(None, starting_room), (None, 0)])
    # Create an empty set to store visited rooms
    visited = set()
    while queue.size() > 0:
        # Dequeue the first path
        path = queue.dequeue()
        # Grab the last room from the path
        room = path[-1][1]
        # If room is the desination, return the path
        if room == destination_room:
            return path[1:]
        # If it has not been visited...
        if room not in visited:
            # Mark it as visited
            visited.add(room)
            # Then add a path all neighbors to the back of the queue
            current_room = all_rooms[str(room)]
            adjacent_rooms = []
            for e in current_room['exits']:
                adjacent_rooms.append((e, current_room['exits'][e]))
            for next_room in adjacent_rooms:
                queue.enqueue(path + [next_room])

def hunt_treasure(time_to_eat=None):
    # if not eating, set timer for 24 hours
    if time_to_eat is None:
        time_to_eat = time.time() + 86400
        
    r = requests.get(base_url + "adv/init/", headers=headers)
    try:
        current_room_id = r.json()['room_id']
        print(f'current room: {current_room_id}')
    except KeyError:
        print('Error: room_id does not exist')
        print(r.json())
    time.sleep(r.json()['cooldown'])

    # warp player if not in light world
    if current_room_id not in range(0, 500):
        print("Warping to light world")
        r = requests.post(base_url + "adv/warp/", headers=headers)
        print(r.json()['messages'][0])
        current_room_id = r.json()['room_id']
        print(f"Now in room {current_room_id}")
        time.sleep(r.json()['cooldown'])

    r = requests.post(f'{base_url}status/', headers=headers)
    time.sleep(r.json()['cooldown'])
    if r.json()['encumbrance'] >= r.json()['strength'] - 1:
        if mode == 'sell':
            sell_items(current_room_id, r.json()['inventory'])
            current_room_id = STORE
        elif mode == 'transmogrify':
            transmogrify_items(current_room_id, r.json()['inventory'])
            current_room_id = TRANSMOGRIFIER

    # caves, traps, or any rooms only reachable by walking through caves or traps
    danger_zone = (488, 412, 310, 259, 263, 499, 456, 275, 242, 218, 216, 450, 445, 339, 287, 252, 234, 474, 447, 405, 303, 284, 368, 418, 415, 406, 361, 302, 469, 425, 454, 423, 408, 470, 459, 458, 422, 426, 457, 461)

    while True:
        # eat when hungry
        if time_to_eat < time.time():
            return
        # pick a new destination room
        destination_room = random.randint(0, 499)
        while current_room_id == destination_room or destination_room in danger_zone:
                destination_room = random.randint(0, 499)

        # find a path to destination room
        path = get_directions(current_room_id, destination_room, all_rooms)
        print(path)

        # travel along path, picking up treasure along the way
        # when reach max encumbrance, sell or transmogrify items
        print(f"Walking to room {destination_room}")
        action = gather_treasure(path)

        if action == 'sell':
            current_room_id = STORE
        elif action == 'transmogrify':
            current_room_id = TRANSMOGRIFIER
        else: 
            current_room_id = destination_room
