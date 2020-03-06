from utils import Queue

def optimized_path(all_rooms, starting_room, destination_room):
    path = get_directions(starting_room, destination_room, all_rooms)
    path_directions = get_pathing(path, all_rooms)
    return path_directions

def get_pathing(path, all_rooms):
    path_directions = []
    next_position = 1

    while next_position < len(path):

        # first, check for a warp command
        if path[next_position][0] == 'warp':
            path_directions.append(['warp'])
            next_position += 1
            continue

        # check for a recall command
        if path[next_position][0] == 'recall':
            path_directions.append(['recall'])
            next_position += 1
            continue

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

def get_directions(starting_room, destination_room, all_rooms):
    # Create an empty queue
    queue = Queue()
    # Add a path for starting_room_id to the queue
    # paths will contain tuple of (direction, room_id)
    queue.enqueue([(None, starting_room)])
    # Create an empty set to store visited rooms
    visited = set()
    while queue.size() > 0:
        # reorder the queue with dashes counting as a single step
        if queue.size() > 1:
            reorder_queue(queue)
        # Dequeue the first path
        path = queue.dequeue()
        # Grab the last room from the path
        room = path[-1][1]
        # If room is the desination, return the path
        if room == destination_room:
            return path
        # If it has not been visited...
        if room not in visited:
            # Mark it as visited
            visited.add(room)
            # Add a path all neighbors to the back of the queue
            current_room = all_rooms[str(room)]
            adjacent_rooms = []
            # Add recall to room zero unless in or adjacent to room zero (fly instead)
            if room not in {0, 1, 2, 4, 10} and 0 not in visited:
                adjacent_rooms.append(('recall', 0))
            # Add room's warp counterpart to the list of adjacent rooms
            if room < 500 and (room + 500) not in visited:
                adjacent_rooms.append(('warp', room + 500))
            elif room >= 500 and (room - 500) not in visited:
                adjacent_rooms.append(('warp', room - 500))
            # Add adjecent rooms
            for e in current_room['exits']:
                if current_room['exits'][e] not in visited:
                    adjacent_rooms.append((e, current_room['exits'][e]))
            for next_room in adjacent_rooms:
                queue.enqueue(path + [next_room])

def reorder_queue(queue):
    # for each list in the queue
    for path in queue.queue:
        # calcuate the steps and append the number of steps
        steps = 0
        hops = 0
        next_position = 1
        direction = path[next_position][0]
        while next_position < len(path):
            if path[next_position][0] == direction:
                hops += 1
            else:
                break
            if hops > 2:
                next_position += hops
                # add 1 for dash not having wise explorer bonus
                steps += 1
            else:
                next_position += 1
        steps += 1
        path.append(steps)
    # sort lists by last value (steps)
    queue.queue.sort(key=lambda path: path[-1])
    # remove the steps values
    for i in range(queue.size()):
        queue.queue[i] = queue.queue[i][:-1]
    return None
