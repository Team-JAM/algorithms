import json
from ast import literal_eval

with open('rooms1.json', 'r') as f:
    rooms_string = f.read()

rooms = json.loads(rooms_string)
max_length = 0
for room in rooms.values():
    if len(room['description']) > max_length:
        max_length = len(room['description'])
print(max_length)

# grid = [[None] * 31 for _ in range(31)]
# for room in rooms.values():
#     x, y = literal_eval(room['coordinates'])
#     grid[y][x] = room

# with open('grid.json', 'w') as f:
#     f.write(json.dumps(grid, indent=2))
