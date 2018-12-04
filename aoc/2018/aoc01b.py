from itertools import cycle

seen = set([0])
state = 0

lines = open("aoc01.txt").readlines()

for line in cycle(lines):
    change = int(line)
    state += change
    if state in seen:
        print(state)
        break
    else:
        seen.add(state)
