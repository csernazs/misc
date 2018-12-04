#!/usr/bin/python3

from collections import defaultdict


counts = defaultdict(int)
claims = []

# #7 @ 817,143: 21x16
for line in open("aoc03.txt"):
    line = line.strip()
    fields = line.split()
    claim_id = int(fields[0][1:])
    start = tuple(map(int, fields[2][:-1].split(",")))
    size = tuple(map(int, fields[3].split("x")))
#    print(start, size)
    claims.append((claim_id, start, size))


for claim_id, start, size in claims:
    for row in range(start[0], start[0] + size[0]):
        for col in range(start[1], start[1] + size[1]):
            counts[(row, col)] += 1


for claim_id, start, size in claims:
    intact = True
    for row in range(start[0], start[0] + size[0]):
        for col in range(start[1], start[1] + size[1]):
            if counts[(row, col)] > 1:
                intact = False
                break

        if not intact:
            break

    if intact:
        print(claim_id)