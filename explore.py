import json
import requests
import time
from graph import Graph

def limit_world(data):
    if data['room_id'] == 0:
        data['exits'] = ["n", "s", "e"]
    elif data['room_id'] == 1:
        data['exits'] = ["w"]
    return data

def explore_world(base_url, headers):
    print("Starting!\n-----------\n")
    # create a graph object
    explore_world = Graph()

    # create a player
    r = requests.get(base_url + "init/", headers=headers)
    # explore_world.add_room(r.json())
    restricted_world = limit_world(r.json())
    explore_world.add_room(restricted_world)
    # switch statements above
    current_room_id = r.json()['room_id']
    # set cooldown
    time_for_next_action = time.time() + r.json()['cooldown']

    print(f'Starting in room {current_room_id}')
    # while there are unexplored rooms
    while True:
        # find path to nearest room with an unexplored exit
        path = explore_world.bfs_to_unexplored(current_room_id)
        if path is None:
            break
        # while still path left to travel
        for heading in path:
            payload = {'direction': heading[0], 'next_room_id': str(heading[1])}
            print(f'Heading to the {heading[0]} to room {heading[1]}.')
            # sleep for cooldown
            time.sleep(time_for_next_action - time.time())
            # move
            prev_room_id = current_room_id
            r = requests.post(f'{base_url}move/', headers=headers, json=payload)
            current_room_id = r.json()['room_id']
            cd = r.json()['cooldown']
            msg = r.json()['messages']
            print(f'Arrived in room {current_room_id}')
            print(f'cooldown: {cd}')
            print(f'message: {msg}')
            print('-----')
            # set cooldown
            time_for_next_action = time.time() + r.json()['cooldown']
        # while there are unexplored exits
        while True:
            # pick an unexplored direction
            direction = explore_world.pick_unexplored(current_room_id)
            if direction is None:
                break
            payload = {'direction': direction}
            print(f'Heading to the {direction}.')
            prev_room_id = current_room_id
            # sleep for cooldown
            time.sleep(time_for_next_action - time.time())
            # move
            r = requests.post(f'{base_url}move/', headers=headers, json=payload)
            current_room_id = r.json()['room_id']
            cd = r.json()['cooldown']
            msg = r.json()['messages']
            print(f'Arrived in room {current_room_id}')
            print(f'cooldown: {cd}')
            print(f'message: {msg}')
            print('-----')
            # store new info
            # explore_world.add_room(r.json())
            restricted_world = limit_world(r.json())
            explore_world.add_room(restricted_world)
            # switch statements above
            explore_world.add_connection(prev_room_id, current_room_id, direction)
            # set cooldown
            time_for_next_action = time.time() + r.json()['cooldown']

    # with open('rooms.json', 'w') as f:
    #     f.write(json.dumps(explore_world.rooms, indent=2))

    print("-----------\nAll done!")