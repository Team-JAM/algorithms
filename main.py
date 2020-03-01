import time
from explore import explore_world

token = "4011e647f744419233e5691e88d4c3fb656a248c"
base_url = "https://team-jam-django-test.herokuapp.com/api/adv/"
headers = {"Authorization": f"Token {token}"}

start = time.time()
explore_world(base_url, headers)
end = time.time()

print(f'Exploration completed in {end - start} seconds.')
