"""
Automatically navigates player to the well, decodes message using ls8 emulator,
navigates to the given room, captures the snitch if it is present, and repeats.
"""
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
    path_directions_time = time.time()
    print(f'\nPath directions took {path_directions_time - start} seconds to compute.\n')
    optimized_travel(path_directions, token, base_url, headers)
    end = time.time()

    print(f'Travel completed in {(end - start):.1f} seconds.')

def well():
    payload = {"name": "well"}
    r = requests.post(base_url + "adv/examine/", headers=headers, json=payload)
    # print(r.json())
    try:
        description = r.json()['description']
    except KeyError:
        print(f'KeyError, r.text: {r.text}')
    _, message = description.split('\n\n')

    with open('wishing_well.ls8', 'w') as f:
        f.write(message)

    # print(f'well_cooldown_time: {r.json()["cooldown"]}')
    # well_sleep_start = time.time()
    # print(f'well_sleep_start: {well_sleep_start}')
    time.sleep(r.json()['cooldown'])
    # well_sleep_end = time.time()
    # print(f'well_sleep_end: {well_sleep_end}')
    # print(f'time asleep in the well: {well_sleep_end - well_sleep_start}')
    # print('--------------')


def hunt_snitches(time_to_eat=None):
    # if not eating, set timer for 24 hours
    if time_to_eat is None:
        time_to_eat = time.time() + 86400
    with open('snitch start log', 'a') as f:
        current_time = time.time()
        start_message = f'Starting snitch looping at {current_time}\n'
        f.write(start_message)

    r = requests.get(base_url + "adv/init/", headers=headers)
    # print('---request text init---')
    # print(r.text)
    # print('-----------------------')
    try:
        current_room_id = r.json()['room_id']
        # print(f'current room: {current_room_id}')
    except KeyError:
        print('Error: room_id does not exist')
    # start_sleep = time.time()
    # print(f'sleeping for {r.json()["cooldown"]}')
    time.sleep(r.json()['cooldown'])
    # end_sleep = time.time()
    # print(f'slept for {end_sleep - start_sleep} seconds')

    while True:
        # navigate to well 
        if current_room_id != WELL:
            navigate(current_room_id, WELL)

        # Find the next snitch room as soon as a new one appears,
        # or go anyway if 50 seconds have passed.
        # examine well
        well()
        # decode message
        message = decode()
        # print(f'message: {message}, tail: {message[24:]}')
        next_room = int(message[24:])
        # print(f'\nfirst snitch room: {prev_room}')
        # room_find_start_time = time.time()
        # while True:
        #     # examine well
        #     well()

        #     # decode message
        #     message = decode()
        #     next_room = int(message[24:])
        #     if next_room != prev_room or time.time() > room_find_start_time + 50:
        #         room_find_end_time = time.time()
        #         print(f'Time waiting: {room_find_end_time - room_find_start_time}')
                # break
        
        print(message + '\n')

        # navigate to room from message
        if next_room != WELL:
            navigate(WELL, next_room)
            current_room_id = next_room

        # # capture snitch if available
        # response = requests.get(base_url + "adv/init/", headers=headers)
        # time.sleep(response.json()['cooldown'])
        # print('Arrived in snitch room!\n')
        # if 'golden snitch' in response.json()['items']:
        #     payload = {"name": "snitch"}
        #     response = requests.post(base_url + "adv/take/", headers=headers, json=payload)
        #     print(response.json())
        #     print('\n***************\n')
        #     with open('snitch hit log', 'a') as f:
        #         current_time = time.time()
        #         possible_snitch_message = f'possible snitch at {current_time}\n{response.json()}\n\n'
        #         f.write(possible_snitch_message)
        #     time.sleep(response.json()['cooldown'])
        # else:
        #     print('No snitch here.\n')
        #     with open('snitch miss log', 'a') as f:
        #         current_time = time.time()
        #         miss_message = f'miss at {current_time}\n'
        #         f.write(miss_message)

        # use this capture snitch method if you want to avoid the 1 sec init request
        # downside is that if the snitch is gone you encur a cooldown penalty
        payload = {"name": "snitch"}
        response = requests.post(base_url + "adv/take/", headers=headers, json=payload)
        print(response.json())
        print('\n***************\n')
        time.sleep(response.json()['cooldown'])

        response = requests.post(base_url + "adv/status/", headers=headers)
        print(f'Snitch count: {response.json()["snitches"]}')
        time.sleep(response.json()['cooldown'])

        if time_to_eat < time.time():
            return
        

        # with open('snitch wait log', 'a') as f:
        #     current_time = time.time()
        #     wait_message = f'Time waiting before event at {current_time}: {room_find_end_time - room_find_start_time}\n'
        #     f.write(wait_message)

# hunt_snitches()
    