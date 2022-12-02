#!/usr/bin/env python3

import sys
from icecream import ic
import numpy as np


def parse(lines):
    retval = []
    for line in lines:
        left, right = line.split(" -> ")
        leftpos = [int(x) for x in left.split(",")]
        rightpos = [int(x) for x in right.split(",")]
        retval.append((leftpos, rightpos))
    return retval


def filter_hv(positions):
    for left, right in positions:
        if left[0] == right[0] or left[1] == right[1]:
            yield (left, right)

def filter_diag(positions):
    # 10, 15 -> 20, 25
    # 20, 25 -> 10, 15
    # 20, 15 -> 10, 25
    # 10, 25 -> 20, 15
    for left, right in positions:
        if abs(left[0] - right[0]) == abs(left[1] - right[1]):
            yield (left, right)

def minmax(positions):
    selection = []
    for left, right in positions:
        selection.extend(left)
        selection.extend(right)

    return min(selection), max(selection)


def fill_hv(grid, data):
    for left, right in data:
        if left[0] == right[0]:  # vertical
            if left[1] < right[1]:
                start = left[1]
                end = right[1] + 1
            else:
                start = right[1]
                end = left[1] + 1
            for y in range(start, end):
                grid[left[0], y] += 1
        elif left[1] == right[1]:  # horizontal
            if left[0] < right[0]:
                start = left[0]
                end = right[0] + 1
            else:
                start = right[0]
                end = left[0] + 1

            for x in range(start, end):
                grid[x, left[1]] += 1
        else:
            raise ValueError((left, right))

def fill_diag(grid, data):
    for left, right in data:
        if left[0] < right[0]:
            step0 = 1
        else:
            step0 = -1

        if left[1] < right[1]:
            step1 = 1
        else:
            step1 = -1

        pos0 = left[0]
        pos1 = left[1]
        while pos0 != right[0]:
            grid[pos0, pos1] += 1
            pos0 += step0
            pos1 += step1
        grid[right[0], right[1]] += 1


def main():
    with open("aoc_05.txt") as infile:
        data = parse([x.strip() for x in infile])

    data_hv = list(filter_hv(data))
    size = minmax(data)[1] + 1
    ic(data_hv)
    grid = np.zeros((size, size), dtype=np.int64)
    fill_hv(grid, data_hv)
    ic(grid)
    print("part1", np.count_nonzero(grid > 1))

    data_diag = list(filter_diag(data))
    fill_diag(grid, data_diag)
    print("part2", np.count_nonzero(grid > 1))


if __name__ == "__main__":
    sys.exit(main())
