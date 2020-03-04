import json
import requests
import time

# directions_url = 'https://team-jam-api.herokuapp.com/api/get_directions/'
directions_url = 'http://localhost:8000/api/get_directions/'

def travel(destination, base_url, headers):

    # initiate travel mode
    r = requests.get(base_url + "init/", headers=headers)
    try:
        current_room_id = r.json()['room_id']
        print(f'current room: {current_room_id}')
    except KeyError:
        print('Error: room_id does not exist')
    # set cooldown
    time_for_next_action = time.time() + r.json()['cooldown']

    payload = {"starting_room": str(current_room_id), "destination_room": str(destination)}
    print(payload)
    r = requests.post(directions_url, json=payload)
    print(r.json())
    path = r.json()['path']
    for instructions in path:
        travel_mode = instructions[0]
        if travel_mode == 'fly' or travel_mode == 'move':
            payload = {'direction': instructions[1], 'next_room_id': instructions[2]}
        elif travel_mode == 'dash':
            payload = {'direction': instructions[1], 'num_rooms': instructions[2], 'next_room_ids': instructions[3]}
        elif travel_mode == 'recall':
            payload = {}
        
        # sleep for cooldown
        time.sleep(max(time_for_next_action - time.time(), 0))
        # move
        print(f'{base_url}{travel_mode}/', headers, payload)
        r = requests.post(f'{base_url}{travel_mode}/', headers=headers, json=payload)
        # set cooldown
        time_for_next_action = time.time() + r.json()['cooldown']
        print(f"{travel_mode} to room {r.json()['room_id']}")
        print(f"message: {r.json()['messages']}")
        print(f"items: {r.json()['items']}")
        print(f"errors: {r.json()['errors']}")
        print('-----')

    print('Finished traveling.')