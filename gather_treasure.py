import json
import requests
import time

directions_url = 'https://team-jam-api.herokuapp.com/api/get_directions/'

def gather_treasure(destination, base_url, headers):

    # initiate gather treasure mode
    r = requests.get(base_url + "init/", headers=headers)
    current_room_id = r.json()['room_id']
    print(f'current room: {current_room_id}')
    # set cooldown
    time_for_next_action = time.time() + r.json()['cooldown']

    payload = {"starting_room": current_room_id, "destination_room": destination}
    r = requests.post(directions_url, json=payload)
    path = r.json()['path']
    for heading in path:
            payload = {'direction': heading[0], 'next_room_id': str(heading[1])}
            # sleep for cooldown
            time.sleep(max(time_for_next_action - time.time(), 0))
            # move
            r = requests.post(f'{base_url}move/', headers=headers, json=payload)
            items = r.json()['items']
            print(f"entered room {r.json()['room_id']}")
            print(f"message: {r.json()['messages']}")
            print(f"items: {items}")
            print(f"errors: {r.json()['errors']}")
            print('-----')
            # set cooldown
            time_for_next_action = time.time() + r.json()['cooldown']
            # # check for items
            # if len(items) > 0:
            #     print(f'Items found! {items}')
            #     for item in items:
            #         payload = {"name": item}
            #         # sleep for cooldown
            #         time.sleep(max(time_for_next_action - time.time(), 0))
            #         r = requests.post(f'{base_url}take/', headers=headers, json=payload)
            #         print(f'I picked up {item}')
            #         # set cooldown
            #         time_for_next_action = time.time() + r.json()['cooldown']
            #         # sleep for cooldown
            #         time.sleep(max(time_for_next_action - time.time(), 0))
            #         r = requests.post(f'{base_url}status/', headers=headers)
            #         if r.json()['encumbrance'] >= r.json()['strength'] - 1:
            #             sell_items()
            #             return
    print('Finished walking.')

    # if good jacket or pair of boots, wear item
    # if encumbered, put down smallest item until unencumbered, initiate sell mode
        # do not put down boots or jacket if they could be upgrade for other players

def sell_items():
    print('Ready to sell!')
    # sell mode
    # get path to store
    # walk to store
    # sell treasure
    # anounce if good boots or jacket available to share
    # announce when 1000 gold aquired