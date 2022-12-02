#!/usr/bin/env python3

import sys
import numpy as np


def step(fish: np.array):
    fish = fish - 1

    no_selected = np.count_nonzero(fish == -1)

    fish = np.where(fish == -1, 6, fish)

    if no_selected > 0:
        fish = np.concatenate((fish, np.full(no_selected, 8)))

    return fish


def main():
    with open("aoc_06.txt") as infile:
        input_fish = np.array([int(x) for x in infile.readline().strip().split(",")], dtype=np.int8)

    fish = input_fish
    for _ in range(80):
        fish = step(fish)

    print(len(fish))

    fish = input_fish
    for idx in range(256):
        fish = step(fish)
        print(idx, len(fish))

    print(len(fish))


if __name__ == "__main__":
    sys.exit(main())
