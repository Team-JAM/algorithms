# import requests
import json

# token = "4011e647f744419233e5691e88d4c3fb656a248c"
# base_url = "https://team-jam-django-test.herokuapp.com/api/adv/"
# headers = {"Authorization": f"Token {token}"}

# r = requests.get(base_url + "init/", headers=headers)
# print(r.json())

ob = {"tup": (3, 4), "str_tup": '(5, 6)', "li": [7, 8], "str_li": '[9, 0]'}

json_ob = json.dumps(ob)
ob2 = json.loads(json_ob)
print(type(ob))
print(ob)
print(json_ob)
print(ob2)
