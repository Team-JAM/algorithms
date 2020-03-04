from optimized_path import optimized_path
from optimized_travel import optimized_travel
import sys
import time
import json
import requests

if len(sys.argv) != 3:
    print('Usage: move_to_room.py player destination_room')
    sys.exit(1)

player = sys.argv[1]
destination_room = int(sys.argv[2])

if player == 'allison' or player == 'a':
    token = 'b183cb414e3eae854e3930946d0c9370040ea416'
elif player == 'matthew' or player == 'm':
    token = 'a42506e85baef70dd9c66a7d0c090b10a3af26f8'
elif player == 'jonathan' or player == 'j':
    token = '3e4095700cd0b276081a3ac8d4ae04e54a89b92e'

base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
headers = {"Authorization": f"Token {token}"}

# load room data
with open('all_rooms.json') as f:
    all_rooms = json.load(f)

# get starting room
r = requests.get(base_url + "adv/init/", headers=headers)
try:
    current_room_id = int(r.json()['room_id'])
    print(f'current room: {current_room_id}')
except KeyError:
    print('Error: room_id does not exist')
time.sleep(r.json()['cooldown'])

start = time.time()
path_directions = optimized_path(all_rooms, current_room_id, destination_room)
optimized_travel(path_directions, token, base_url, headers)
end = time.time()

print(f'Travel completed in {(end - start):.1f} seconds.')

