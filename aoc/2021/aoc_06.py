#!/usr/bin/env python3

import sys
from typing import Dict
from collections import Counter


def step(fish: Dict[int, int]):
    new_fish = {}
    for number, amount in fish.items():
        new_fish[number - 1] = amount

    new_fish[8] = new_fish.get(-1, 0)
    new_fish[6] = new_fish.get(6, 0) + new_fish.pop(-1, 0)

    return new_fish


def main():
    with open("aoc_06.txt") as infile:
        number_list = [int(x) for x in infile.readline().strip().split(",")]

    # number_list = [3, 4, 3, 1, 2]
    input_fish = dict(Counter(number_list))

    fish = input_fish.copy()
    for _ in range(80):
        fish = step(fish)

    print(sum(fish.values()))

    fish = input_fish.copy()
    for _ in range(256):
        fish = step(fish)

    print(sum(fish.values()))


if __name__ == "__main__":
    sys.exit(main())
