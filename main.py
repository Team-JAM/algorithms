import time
from map_the_world import explore_world
from gather_treasure import gather_treasure

token = "b183cb414e3eae854e3930946d0c9370040ea416"
base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
headers = {"Authorization": f"Token {token}"}

start = time.time()
# explore_world(base_url, headers)
gather_treasure(134, base_url, headers)
end = time.time()

# print(f'Exploration completed in {end - start} seconds.')
