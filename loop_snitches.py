"""
Automatically navigates player to the well, decodes message using ls8 emulator,
navigates to the given room, captures the snitch if it is present, and repeats.
"""
from gather_treasure import gather_treasure
from utils import Queue
from loop_ls8 import decode
from optimized_path import optimized_path
from optimized_travel import optimized_travel
import time
import json
import requests
import sys

if len(sys.argv) != 2:
    print('Usage: loop_snitches.py player')
    sys.exit(1)

player = sys.argv[1]

if player == 'allison' or player == 'a':
    token = 'b183cb414e3eae854e3930946d0c9370040ea416'
elif player == 'matthew' or player == 'm':
    token = 'a42506e85baef70dd9c66a7d0c090b10a3af26f8'
elif player == 'jonathan' or player == 'j':
    token = '3e4095700cd0b276081a3ac8d4ae04e54a89b92e'

base_url = "https://lambda-treasure-hunt.herokuapp.com/api/"
headers = {"Authorization": f"Token {token}"}

WELL = 555

# load room data
with open('all_rooms.json') as f:
    all_rooms = json.load(f)

def navigate(starting_room, destination_room):
    start = time.time()
    path_directions = optimized_path(all_rooms, starting_room, destination_room)
    optimized_travel(path_directions, token, base_url, headers)
    end = time.time()

    print(f'Travel completed in {(end - start):.1f} seconds.')

def well():
    payload = {"name": "well"}
    r = requests.post(base_url + "adv/examine/", headers=headers, json=payload)
    # print(r.json())
    description = r.json()['description']
    _, message = description.split('\n\n')

    with open('wishing_well.ls8', 'w') as f:
        f.write(message)
    
    time.sleep(r.json()['cooldown'])


r = requests.get(base_url + "adv/init/", headers=headers)
try:
    current_room_id = r.json()['room_id']
    print(f'current room: {current_room_id}')
except KeyError:
    print('Error: room_id does not exist')
    print(r.json())
time.sleep(r.json()['cooldown'])

while True:
    # navigate to well 
    if current_room_id != WELL:
        navigate(current_room_id, WELL)

    # Find the next snitch room as soon as a new one appears,
    # or go anyway if 90 seconds have passed.
    # examine well
    well()
    # decode message
    message = decode()
    prev_room = int(message[24:])
    print(f'\nfirst snitch room: {prev_room}')
    room_find_start_time = time.time()
    while True:
        # examine well
        well()

        # decode message
        message = decode()
        next_room = int(message[23:])
        if next_room != prev_room or time.time() > room_find_start_time + 90:
            print(f'Time waiting: {time.time() - room_find_start_time}')
            break
    
    print(message + '\n')

    # navigate to room from message
    if next_room != WELL:
        navigate(WELL, next_room)
        current_room_id = next_room

    # capture snitch if available
    result = requests.get(base_url + "adv/init/", headers=headers)
    time.sleep(result.json()['cooldown'])
    print('Arrived in snitch room!\n')
    if 'golden snitch' in result.json()['items']:
        payload = {"name": "snitch"}
        result = requests.post(base_url + "adv/take/", headers=headers, json=payload)
        print(result.json())
        print('\n***************\n')
        time.sleep(result.json()['cooldown'])
    else:
        print('No snitch here.\n')
    