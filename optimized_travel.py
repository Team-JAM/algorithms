import requests
import time


def optimized_travel(path_directions, token, base_url, headers):
    # initiate travel mode
    # time_for_next_action = time.time()

    for instructions in path_directions:
        travel_mode = instructions[0]
        if travel_mode == 'fly' or travel_mode == 'move':
            payload = {'direction': instructions[1], 'next_room_id': instructions[2]}
        elif travel_mode == 'dash':
            payload = {'direction': instructions[1], 'num_rooms': instructions[2], 'next_room_ids': instructions[3]}
        elif travel_mode == 'recall':
            payload = {}
        
        # sleep for cooldown
        # time.sleep(max(time_for_next_action - time.time(), 0))
        # move
        r = requests.post(f'{base_url}adv/{travel_mode}/', headers=headers, json=payload)
        print("moved to room: ", r.json()['room_id'])
        print(r.json())
        print()
        # set cooldown
        # time_for_next_action = time.time() + r.json()['cooldown']
        time.sleep(r.json()['cooldown'])