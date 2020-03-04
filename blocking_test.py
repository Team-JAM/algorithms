import json
import requests
import time

url = 'https://team-jam-api.herokuapp.com/api/get_directions'
# url = 'http://localhost:8000/api/get_directions'

def move_allison(starting_room, destination_room):

    payload = {"starting_room": str(starting_room), "destination_room": str(destination_room), "token": "b183cb414e3eae854e3930946d0c9370040ea416"}
    r = requests.post(url, json=payload)
    print("allison")
    print(r.content)

def move_matthew(starting_room, destination_room):

    payload = {"starting_room": str(starting_room), "destination_room": str(destination_room), "token": "a42506e85baef70dd9c66a7d0c090b10a3af26f8"}
    # breakpoint()
    res = requests.post(url, json=payload)
    print("matthew")
    print(res.content)
    print('---dir(r)---')
    print(dir(res))
    print('---r.text---')
    print(res.text)
    breakpoint()

t_start = time.time()

m_start = time.time()
move_matthew(145, 461)
m_end = time.time()
print(f'matthew time: {m_end - m_start}')

# a_start = time.time()
# move_allison(330, 495)
# a_end = time.time()
# print(f'allison time: {a_end - a_start}')

t_end = time.time()

print(f'total time: {t_end - t_start}')
