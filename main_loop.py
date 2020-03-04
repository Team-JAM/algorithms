"""
Automatically navigates player to the well, decodes message using ls8 emulator, navigates to the given room, remains there until mines a coin successfully, and repeats
"""
from gather_treasure import gather_treasure
from utils import Queue
import time
import json

token = "a42506e85baef70dd9c66a7d0c090b10a3af26f8"
base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
headers = {"Authorization": f"Token {token}"}

WELL = 55

# load room data
with open('all_rooms.json') as f:
    all_rooms = json.load(f)

def get_pathing(path):
    path_directions = []
    next_position = 1

    # check if room zero is first step and starting room not adjacent to room 0
    if path[1][1] == 0 and path[0][1] not in {1, 2, 4, 10}:
        # if so, start with recall
        path_directions.append(['recall'])
        next_position += 1

    while next_position < len(path):

        # check if there are enough steps for a dash
        direction = path[next_position][0]
        hops = 0
        for i in range(next_position , len(path)):
            if path[i][0] == direction:
                hops += 1
            else:
                break
        if hops > 2:
            next_room_ids = [str(path[i][1]) for i in range(next_position, next_position + hops)]
            dash = ('dash', direction, str(hops), ','.join(next_room_ids))
            path_directions.append(dash)
            next_position += hops
            continue

        # check if flying is called for (next room is not a cave)
        # next_room = Room.objects.get(id=path[next_position][1])
        next_room = all_rooms[str(path[next_position][1])]
        # if no, move; if so, fly
        path[next_position] = list(path[next_position])
        path[next_position][1] = str(path[next_position][1])
        if next_room['terrain'] == 'CAVE':
            path_directions.append(['move'] + path[next_position])
        else:
            path_directions.append(['fly'] + path[next_position])
        next_position += 1
        
    return path_directions

def get_directions(starting_room, destination_room):
    # Create an empty queue
    queue = Queue()
    # Add a path for starting_room_id to the queue
    # Add a second option that recalls to room zero first
    # paths will contain tuple of (direction, room_id)
    queue.enqueue([(None, starting_room)])
    queue.enqueue([(None, starting_room), (None, 0)])
    # Create an empty set to store visited rooms
    visited = set()
    while queue.size() > 0:
        # Dequeue the first path
        path = queue.dequeue()
        # Grab the last room from the path
        room = path[-1][1]
        # If room is the desination, return the path
        if room == destination_room:
            path_directions = get_pathing(path)
            print(path_directions)
            # travel(path_directions, token)
            # return
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

def navigate(room):
    start = time.time()
    get_directions(0, 55)
    end = time.time()

    print(f'Travel completed in {(end - start):.1f} seconds.')

# while True:
    # navigate to well 
navigate(WELL)

    # examine well

    # decode message

    # navigate to room from message

    # mine until receive a coin