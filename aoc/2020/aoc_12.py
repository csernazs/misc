#!/usr/bin/env python3

from collections import deque
from typing import List, Tuple


def parse_file(path: str):
    retval = []
    with open(path) as infile:
        for line in infile:
            cmd = line[0]
            arg = int(line[1:])
            retval.append((cmd, arg))
    return retval


def solve_1(data: List[Tuple[str, int]]):
    pos = [0, 0]
    dirs_right = deque([[-1, 0], [0, -1], [1, 0], [0, 1]])
    for cmd, arg in data:
        if cmd == "N":
            pos[1] = pos[1] + arg
        elif cmd == "S":
            pos[1] = pos[1] - arg
        elif cmd == "E":
            pos[0] = pos[0] - arg
        elif cmd == "W":
            pos[0] = pos[0] + arg
        elif cmd == "F":
            vec = dirs_right[0]
            pos[0] += vec[0] * arg
            pos[1] += vec[1] * arg
        elif cmd == "L" or cmd == "R":
            if arg % 90 != 0:
                raise ValueError(arg)
            number_of_turns = arg // 90
            if cmd == "R":
                dirs_right.rotate(0 - number_of_turns)
            elif cmd == "L":
                dirs_right.rotate(number_of_turns)

    return abs(pos[0]) + abs(pos[1])


def solve_2(data: List[Tuple[str, int]]):
    pos_wpt = [-10, 1]
    pos_ship = [0, 0]
    for cmd, arg in data:
        if cmd == "N":
            pos_wpt[1] = pos_wpt[1] + arg
        elif cmd == "S":
            pos_wpt[1] = pos_wpt[1] - arg
        elif cmd == "E":
            pos_wpt[0] = pos_wpt[0] - arg
        elif cmd == "W":
            pos_wpt[0] = pos_wpt[0] + arg
        elif cmd == "F":
            pos_ship[0] += pos_wpt[0] * arg
            pos_ship[1] += pos_wpt[1] * arg
        elif cmd == "L" or cmd == "R":
            if arg % 90 != 0:
                raise ValueError(arg)
            number_of_turns = arg // 90
            if cmd == "R":
                for _ in range(number_of_turns):
                    pos_wpt = [0 - pos_wpt[1], pos_wpt[0]]
            elif cmd == "L":
                for _ in range(number_of_turns):
                    pos_wpt = [pos_wpt[1], 0 - pos_wpt[0]]

    return abs(pos_ship[0]) + abs(pos_ship[1])


def main():
    data = parse_file("aoc_12.txt")
    print("solve_1", solve_1(data))
    print("solve_2", solve_2(data))


if __name__ == "__main__":
    main()
