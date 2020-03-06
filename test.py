import sys

if len(sys.argv) != 2:
    print('Usage: loop_treasure.py player')
    sys.exit(1)

player = sys.argv[1]

print(f'Hello, {player}!')
