#!/usr/bin/python3

from collections import defaultdict


claims = defaultdict(int)

# #7 @ 817,143: 21x16
for line in open("aoc03.txt"):
    line = line.strip()
    fields = line.split()
    start = list(map(int, fields[2][:-1].split(",")))
    size = list(map(int, fields[3].split("x")))
#    print(start, size)
    for row in range(start[0], start[0] + size[0]):
        for col in range(start[1], start[1] + size[1]):
            claims[(row, col)] += 1


sol = 0
for key, value in claims.items():
    if value > 1:
        sol += 1

print(sol)
