from graph import Graph
import json
import requests
# from models import Room
import time

def explore_world(base_url, headers):
    """Navigate the map and log all rooms"""
    print("Starting!\n-----------\n")
    # open file for appending
    append_file = open('rooms_underworld_appending.json', 'a')

    # Room.objects.all().delete()
    explore_world = Graph()

    r = requests.get(base_url + "init/", headers=headers)
    explore_world.add_room(r.json())
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
            print(f'rooms explored: {len(explore_world.rooms)}')
            print('-----')
            # store new info
            append_file.write(json.dumps(r.json(), indent=2))
            append_file.write('\n')

            explore_world.add_room(r.json())
            explore_world.add_connection(prev_room_id, current_room_id, direction)
            # set cooldown
            time_for_next_action = time.time() + r.json()['cooldown']
            # append info


    # close file
    append_file.close()

    # write in one pass
    with open('rooms_underworld.json', 'w') as f:
        f.write(json.dumps(explore_world.rooms, indent=2))

    print("-----------\nAll done!")