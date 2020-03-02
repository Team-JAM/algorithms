from ast import literal_eval
from utils import Queue


class Graph():
    def __init__(self):
        self.rooms = {}

    def add_room(self, data):
        """Add a room (vertex) to graph and database"""
        room_id = data['room_id']
        room_data = {'id': data['room_id'],
                     'title': data['title'],
                     'description' : data['description'],
                     'coordinates': literal_eval(data['coordinates']),
                     'elevation': data['elevation'],
                     'terrain': data['terrain'],
                     'exits' : {direction: '?' for direction in data['exits']}
                     }
        self.rooms.setdefault(room_id, room_data)

    def add_connection(self, room1_id, room2_id, direction):
        """Add directed connection (edges) between two exits"""
        opposite_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        if room1_id in self.rooms and room2_id in self.rooms:
            self.rooms[room1_id]['exits'][direction] = room2_id
            self.rooms[room2_id]['exits'][opposite_direction[direction]] = room1_id
        else:
            raise IndexError('That room does not exist!')

    def pick_unexplored(self, room_id, directions_sequence=['n', 'e', 's', 'w']):
        """Using a fixed order, return a room's first unexplored direction"""
        for direction in directions_sequence:
            egress = self.rooms[room_id]['exits'].get(direction, None)
            if egress == '?':
                return direction
        return None

    def get_exits(self, room_id):
        """Get all exits (edges) of a room (vertex)"""
        return self.rooms[room_id]['exits']

    def bfs_to_unexplored(self, starting_room_id):
        """Find path to shortest unexplored room using breadth-first search"""
        queue = Queue()
        # paths will contain tuple of (direction, room_id)
        queue.enqueue([(None, starting_room_id)])
        visited = set()

        while queue.size() > 0:
            current_path = queue.dequeue()
            current_room_id = current_path[-1][1]
            current_exits = self.get_exits(current_room_id)

            if '?' in current_exits.values():
                # slice off the current room and return path
                return current_path[1:]

            if current_room_id not in visited:
                visited.add(current_room_id)
                for direction, room_id in current_exits.items():
                    path_to_next_room = current_path + [(direction, room_id)]
                    queue.enqueue(path_to_next_room)

        return None
    