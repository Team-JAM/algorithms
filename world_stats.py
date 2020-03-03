import json

with open('rooms.json', 'r') as f:
    rooms_string = f.read()

rooms = json.loads(rooms_string)

titles = set()
terrain = set()
max_x = 0
max_y = 0
min_x = 999
min_y = 999
max_elevation = 0
min_elevation = 999


for room in rooms.values():
    titles.add(room['title'])
    terrain.add(room['terrain'])
    if room['x_coord'] > max_x:
        max_x = room['x_coord']
    if room['x_coord'] < min_x:
        min_x = room['x_coord']

    if room['y_coord'] > max_y:
        max_y = room['y_coord']
    if room['y_coord'] < min_y:
        min_y = room['y_coord']

    if room['elevation'] > max_elevation:
        max_elevation = room['elevation']
    if room['elevation'] < min_elevation:
        min_elevation = room['elevation']

    if room['terrain'] == 'MOUNTAIN':
        elevation = room['elevation']
        print(f'mountian {elevation}')

print(f'min x {min_x}, max x {max_x}')
print(f'min y {min_y}, max y {max_y}')
print(f'min elevation {min_elevation}, max elevation {max_elevation}')
print('Terrain types')
for t in terrain:
    print(t)
print('----')
print('Titles')
for t in titles:
    print(t)

special_rooms = {"The Peak of Mt. Holloway", "Arron's Athenaeum", "Pirate Ry's",
                 "Fully Shrine", "Linh's Shrine", "The Transmogriphier",
                 "JKMT Donuts", "Sandofsky's Sanctum", "Shop", "Glasowyn's Grave",
                 "Wishing Well"}

for room in rooms.values():
    if room['title'] in special_rooms:
        print(f'{room["id"]}: {room["title"]}')