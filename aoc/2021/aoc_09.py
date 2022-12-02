#!/usr/bin/env python3

import sys
from typing import List, Tuple
import numpy as np
from termcolor import colored
from icecream import ic


def parse(lines: List[str]) -> np.array:
    data = []
    for line in lines:
        row = [int(x) for x in line]
        data.append(row)

    return np.array(data, dtype=np.int8)

def print_grid(grid, marks):
    for row_idx in range(grid.shape[0]):
        for col_idx in range(grid.shape[1]):
            cell = str(grid[row_idx, col_idx])
            if (row_idx, col_idx) in marks:
                sys.stdout.write(colored(cell, "red"))
            else:
                sys.stdout.write(cell)
        sys.stdout.write("\n")

def get_nearby_indexes(grid: np.array, row_idx: int, col_idx: int):
    retval = []
    height = grid.shape[0]
    width = grid.shape[1]
    if row_idx > 0:
        retval.append((row_idx - 1, col_idx))
    if row_idx < height - 1:
        retval.append((row_idx + 1, col_idx))
    if col_idx > 0:
        retval.append((row_idx, col_idx - 1))
    if col_idx < width - 1:
        retval.append((row_idx, col_idx + 1))

    return retval


def get_lowpoints(grid: np.array) -> List[Tuple[int, int]]:
    retval: List[Tuple[int, int]] = []

    height = grid.shape[0]
    width = grid.shape[1]
    for row_idx in range(height):
        for col_idx in range(width):
            cell = grid[row_idx, col_idx]
            for pos in get_nearby_indexes(grid, row_idx, col_idx):
                if cell >= grid[pos]:
                    break
            else:
                retval.append((row_idx, col_idx))
    return retval


def get_basin_from(grid: np.array, row_idx: int, col_idx: int):
    queue = [(row_idx, col_idx)]
    basin = set()
    while queue:
        row_idx, col_idx = queue.pop()
        # if (row_idx, col_idx) in basin:
        #     continue

        current_value = grid[row_idx, col_idx]
        for pos in get_nearby_indexes(grid, row_idx, col_idx):
            value = grid[pos]
            if value > current_value and value < 9:
                queue.append(pos)
                basin.add(pos)

    return basin


def solve_1(grid: np.array):
    risk_level = 0
    for row_idx, col_idx in get_lowpoints(grid):
        risk_level += grid[row_idx, col_idx] + 1
    print(risk_level)


def solve_2(grid: np.array):
    basin_sizes = []
    all_basin = set()
    for row_idx, col_idx in get_lowpoints(grid):
        basin = get_basin_from(grid, row_idx, col_idx)
        basin.add((row_idx, col_idx))
        # ic((row_idx, col_idx))
        # ic(basin)
        all_basin = all_basin.union(basin)
        basin_sizes.append(len(basin))

    print_grid(grid, all_basin)

    basin_sizes.sort(reverse=True)
    ic(basin_sizes)
    print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])


def main():
    with open("aoc_09.txt") as infile:
        grid = parse([x.strip() for x in infile.readlines()])

    solve_1(grid)
    solve_2(grid)


if __name__ == "__main__":
    sys.exit(main())
