from loop_snitches import hunt_snitches, navigate
import requests
import sys
import time
from optimized_path import optimized_path
from optimized_travel import optimized_travel

if len(sys.argv) != 2:
    print('Usage: snitches_command.py player')
    sys.exit(1)

player = sys.argv[1]

if player == 'allison' or player == 'a':
    token = 'b183cb414e3eae854e3930946d0c9370040ea416'
elif player == 'matthew' or player == 'm':
    token = 'a42506e85baef70dd9c66a7d0c090b10a3af26f8'
elif player == 'jonathan' or player == 'j':
    token = '3e4095700cd0b276081a3ac8d4ae04e54a89b92e'
base_url = "https://lambda-treasure-hunt.herokuapp.com/api/"
headers = {"Authorization": f"Token {token}"}

DONUT_SHOP = 15

def hunt_snitches_fast():
    ### Group Mode ###
    # start with at least 2000 gold
    # move to donut shop
    # buy donut
    # set 5 minute timer
    # hunt snitches for 5 minutes
    # set 10 minute timer
    # gather treasure for 10 minutes

    ### Solo Mode ###
    while True:
        # start with at least 2000 gold 
        # move to donut shop
        r = requests.get(base_url + "adv/init/", headers=headers)
        try:
            current_room_id = r.json()['room_id']
            print(f'current room: {current_room_id}')
        except KeyError:
            print('Error: room_id does not exist')
            print(r.json())
        time.sleep(r.json()['cooldown'])
        # go to donut shop
        if current_room_id != DONUT_SHOP:
            navigate(current_room_id, DONUT_SHOP)

        # buy donut
        payload = {"name": "donut", "confirm": "yes"}
        response = requests.post(base_url + "adv/buy/", headers=headers, json=payload)
        print(response.json()['messages'])
        # set 5 minute timer
        time_to_eat = time.time() + 300
        time.sleep(response.json()['cooldown'])

        # hunt snitches for 5 minutes
        hunt_snitches(time_to_eat=time_to_eat)
        # if less than 2000 gold
            # set 5 minute timer
            # gather treasure
            # repeat if needed

hunt_snitches_fast()

while True:
    time.sleep(40)
    hunt_snitches_fast()
