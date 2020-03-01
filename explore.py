import json
import requests
import time
from graph import Graph

def explore_world(base_url, headers):
    print("Starting!\n-----------\n")
    # create a graph object
    explore_world = Graph()

    # create a player
    r = requests.get(base_url + "init/", headers=headers)
    explore_world.add_room(r.json())
    current_room_id = r.json()['room_id']
    cooldown = r.json()['cooldown']

    # while there are unexplored rooms
        # find path to nearest room with an unexplored exit
        # while still path left to travel
            # sleep for cooldown
            # move
            # set cooldown
    # while there are unexplored exits
    print(f'Starting in room {current_room_id}')
    while True:
        # pick an unexplored direction
        direction = explore_world.pick_unexplored(current_room_id)
        if direction is None:
            break
        payload = {'direction': direction}
        print(f'Heading to the {direction}.')
        # sleep for cooldown
        time.sleep(cooldown)
        # move
        prev_room_id = current_room_id
        r = requests.post(f'{base_url}move/', headers=headers, json=payload)
        current_room_id = r.json()['room_id']
        print(f'Arrived in room {current_room_id}')
        # store new info
        explore_world.add_room(r.json())
        explore_world.add_connection(prev_room_id, current_room_id, direction)
        # set cooldown
        cooldown = r.json()['cooldown']

    with open('world.json', 'w') as f:
        f.write(json.dumps(explore_world.world_map))

    with open('rooms.json', 'w') as f:
        f.write(json.dumps(explore_world.rooms))

    print("-----------\nAll done!")