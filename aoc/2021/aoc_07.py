#!/usr/bin/env python3

import sys
from icecream import ic
from typing import List
import math


def compute_fuel(positions: List[int], wanted: int, dist_fn):
    retval = 0
    for p in positions:
        retval += dist_fn(abs(p - wanted))
    return retval


def main():
    with open("aoc_07.txt") as infile:
        positions = [int(x) for x in infile.readline().strip().split(",")]

    # positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    candidates = set(positions)

    min_fuel = None
    for i in candidates:
        fuel = compute_fuel(positions, i, lambda x: x)
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel

    print(min_fuel)

    min_fuel = None
    for i in candidates:
        fuel = compute_fuel(positions, i, lambda x: math.comb(x + 1, 2))
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel

    print(min_fuel)

if __name__ == "__main__":
    sys.exit(main())
