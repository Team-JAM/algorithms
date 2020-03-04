import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

# token = "a42506e85baef70dd9c66a7d0c090b10a3af26f8"
base_url = "https://lambda-treasure-hunt.herokuapp.com/api/bc/"
# headers = {"Authorization": f"Token {token}"}


def proof_of_work(last_proof, difficulty):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("\nSearching for next proof")
    proof = random.randint(0, 16777216)
    # #  TODO: Your code here
    # last_encoded = f'{last_proof}'.encode()
    # last_hash = hashlib.sha256(last_encoded).hexdigest()
    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, proof, difficulty):
    """
    Validates the Proof:  Multi-ouroborus:  Are the first x characters of
    the hash of the last proof concatenated with the new proof all zeros?
    """

    # TODO: Your code here!
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:difficulty] == '0' * difficulty

def mine(headers):
    r = requests.get(base_url + "last_proof/", headers=headers)
    print("Last proof:")
    print(r.json())

    last_proof = r.json()['proof']
    difficulty = r.json()['difficulty']

    proof = proof_of_work(last_proof, difficulty)
    proof = int(proof)

    payload = {"proof": proof}
    r = requests.post(base_url + "mine/", headers=headers, json=payload)
    print(r.json())
    print()
    return r.json()

# if __name__ == '__main__':
#     # What node are we interacting with?
#     if len(sys.argv) > 1:
#         node = sys.argv[1]
#     else:
#         node = "https://lambda-coin.herokuapp.com/api"

#     coins_mined = 0

#     # Load or create ID
#     f = open("my_id.txt", "r")
#     id = f.read()
#     print("ID is", id)
#     f.close()

#     if id == 'NONAME\n':
#         print("ERROR: You must change your name in `my_id.txt`!")
#         exit()
#     # Run forever until interrupted
#     while True:
#         # Get the last proof from the server
#         r = requests.get(url=node + "/last_proof")
#         data = r.json()
#         new_proof = proof_of_work(data.get('proof'))

#         post_data = {"proof": new_proof,
#                      "id": id}

#         r = requests.post(url=node + "/mine", json=post_data)
#         data = r.json()
#         if data.get('message') == 'New Block Forged':
#             coins_mined += 1
#             print("Total coins mined: " + str(coins_mined))
#         else:
#             print(data.get('message'))
