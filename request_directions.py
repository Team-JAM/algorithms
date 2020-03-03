import json
import requests

directions_url = 'https://team-jam-api.herokuapp.com/api/get_directions/'
payload = {"starting_room": 0, "destination_room": 5}

r = requests.post(directions_url, json=payload)
print(r.content)