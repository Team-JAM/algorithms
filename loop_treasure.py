from optimized_path import optimized_path, get_directions
from optimized_travel import optimized_travel
import sys
import time
import json
import requests
import random

if len(sys.argv) != 3:
    print('Usage: loop_treasure.py player destination_room')
    sys.exit(1)

player = sys.argv[1]
destination_room = int(sys.argv[2])

if player == 'allison' or player == 'a':
    token = 'b183cb414e3eae854e3930946d0c9370040ea416'
elif player == 'matthew' or player == 'm':
    token = 'a42506e85baef70dd9c66a7d0c090b10a3af26f8'
elif player == 'jonathan' or player == 'j':
    token = '3e4095700cd0b276081a3ac8d4ae04e54a89b92e'

base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
headers = {"Authorization": f"Token {token}"}

STORE = 1

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
            for item in items:
                payload = {"name": item}
                # sleep for cooldown
                time.sleep(max(time_for_next_action - time.time(), 0))
                r = requests.post(f'{base_url}take/', headers=headers, json=payload)
                print(f'I picked up {item}')
                # set cooldown
                time_for_next_action = time.time() + r.json()['cooldown']
                # sleep for cooldown
                time.sleep(max(time_for_next_action - time.time(), 0))
                r = requests.post(f'{base_url}status/', headers=headers)
                if r.json()['encumbrance'] >= r.json()['strength'] - 1:
                    sell_items(heading[1], r.json()['inventory'])
                    return
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
        r = requests.post(f'{base_url}sell/', headers=headers, payload=payload)
        print(f"Sold the {item}")
        time.sleep(r.json()['cooldown'])

r = requests.get(base_url + "adv/init/", headers=headers)
try:
    current_room_id = r.json()['room_id']
    print(f'current room: {current_room_id}')
except KeyError:
    print('Error: room_id does not exist')
    print(r.json())
time.sleep(r.json()['cooldown'])

# caves, traps, or any rooms only reachable by walking through caves or traps
danger_zone = (488, 412, 310, 259, 263, 499, 456, 275, 242, 218, 216, 450, 445, 339, 287, 252, 234, 474, 447, 405, 303, 284, 368, 418, 415, 406, 361, 302, 469, 425, 454, 423, 408, 470, 459, 458, 422, 426, 457, 461)

destination_room = random.randint(0, 499)
while True:
    # find a path to destination room
    path = get_directions(all_rooms, current_room_id, destination_room)

    # travel along path, picking up treasure along the way
    # when reach max encumbrance, sell items
    print(f"Walking to room {destination_room}")
    gather_treasure(path)

    # pick a new destination room
    new_room = random.randint(0, 499)
    while new_room == destination_room or new_room in danger_zone:
        new_room = random.randint(0, 499)
    destination_room = new_room
