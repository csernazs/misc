#!/usr/bin/env python3

import re
from collections import defaultdict


def parse_file(path: str):
    retval = []
    with open(path) as infile:
        for raw_line in infile:
            line = raw_line.rstrip()
            directions = re.findall("e|se|sw|w|nw|ne", line)
            retval.append(tuple(directions))

    return retval


DIRECTIONS = {
    "e": [1, -1, 0],
    "w": [-1, 1, 0],
    "ne": [0, -1, 1],
    "sw": [0, 1, -1],
    "nw": [-1, 0, 1],
    "se": [1, 0, -1],
}


def get_coordinate(directions):
    retval = [0, 0, 0]
    for direction in directions:
        offsets = DIRECTIONS[direction]
        retval[0] += offsets[0]
        retval[1] += offsets[1]
        retval[2] += offsets[2]

    return retval


def get_adjacent(pos):
    retval = []
    for offsets in DIRECTIONS.values():
        retval.append((pos[0] + offsets[0], pos[1] + offsets[1], pos[2] + offsets[2]))

    return retval


def count_adjacent(colors, pos):
    cnt = 0
    for apos in get_adjacent(pos):
        if colors[apos]:
            cnt += 1
    return cnt


def do_round(colors):
    to_check = set()
    for pos, color in colors.items():
        if color:
            to_check.add(pos)
            to_check.update(get_adjacent(pos))

    to_flip = set()
    for pos in to_check:
        cnt = count_adjacent(colors, pos)
        is_black = colors.get(pos, False)
        # print("adjacent", pos, cnt, "black" if is_black else "white")
        if is_black and (cnt == 0 or cnt > 2):
            to_flip.add(pos)
        elif (not is_black) and cnt == 2:
            to_flip.add(pos)

    # print("to_flip", len(to_flip))
    for pos in to_flip:
        # print("flip", pos, not colors[pos])
        colors[pos] = not colors[pos]


def solve_1(data):
    colors = defaultdict(bool)
    for directions in data:
        coordinate = tuple(get_coordinate(directions))
        colors[coordinate] = not colors[coordinate]

    return sum(colors.values())


def solve_2(data):
    colors = defaultdict(bool)
    for directions in data:
        coordinate = tuple(get_coordinate(directions))
        colors[coordinate] = not colors[coordinate]

    # print("start", sum(colors.values()))

    for i in range(100):
        do_round(colors)
        # print("day {}: {}".format(i + 1, sum(colors.values())))

    return sum(colors.values())


def test_coordinate():
    assert get_coordinate(["e", "se", "w"]) == [1, 0, -1]
    assert get_coordinate(["nw", "w", "sw", "e", "e"]) == [0, 0, 0]


def main():
    data = parse_file("aoc_24.txt")
    print("solve_1", solve_1(data))
    print("solve_2", solve_2(data))


if __name__ == "__main__":
    main()
