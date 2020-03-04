import time
from map_the_world import explore_world
from gather_treasure import gather_treasure
from travel import travel

token = "a42506e85baef70dd9c66a7d0c090b10a3af26f8"
base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
headers = {"Authorization": f"Token {token}"}

start = time.time()
# explore_world(base_url, headers)
gather_treasure(55, base_url, headers)
# travel(555, base_url, headers)
end = time.time()

print(f'Travel completed in {(end - start):.1f} seconds.')
