import requests

token = "a42506e85baef70dd9c66a7d0c090b10a3af26f8"
base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
headers = {"Authorization": f"Token {token}"}

payload = {"name": "well"}
r = requests.post(base_url + "examine/", headers=headers, json=payload)

description = r.json()['description']
_, message = description.split('\n\n')

with open('wishing_well.ls8', 'w') as f:
    f.write(message)
