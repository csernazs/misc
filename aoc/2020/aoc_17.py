#!/usr/bin/env python3

from itertools import product
from typing import Set, Tuple
from functools import lru_cache

Cells = Set[Tuple[int, int, int]]


@lru_cache(maxsize=128)
def nearby_offsets(dimensions):
    retval = []
    zeros = (0,) * dimensions
    for diffs in product([-1, 0, 1], repeat=dimensions):
        if diffs != zeros:
            retval.append(diffs)

    return tuple(retval)


@lru_cache(maxsize=4096)
def nearby_coordinates(pos):
    retval = set()
    diffs = nearby_offsets(len(pos))
    for diff in diffs:
        new_pos = []
        for p, d in zip(pos, diff):
            new_pos.append(p + d)
        retval.add(tuple(new_pos))
    return retval


def count_nearby(cells: Cells, pos):
    nearby = cells.intersection(nearby_coordinates(pos))
    return len(nearby)


def parse_file(path: str):
    cells = set()
    with open(path) as infile:
        for y, line in enumerate(infile):
            for x, char in enumerate(line.rstrip()):
                if char == "#":
                    cells.add((x, y))
    return cells


def get_dimensions(cells: Cells):
    mins = []
    maxs = []
    for cell in cells:
        if not mins:
            mins = list(cell)
            maxs = list(cell)
            continue

        for idx, p in enumerate(cell):
            if p < mins[idx]:
                mins[idx] = p
            elif p > maxs[idx]:
                maxs[idx] = p

    retval = [(a, b) for a, b in zip(mins, maxs)]
    return retval


def iterate(cells: Cells):
    cells_copy = cells.copy()

    d = get_dimensions(cells_copy)
    for pos in product(*[range(a[0] - 1, a[1] + 2) for a in d]):
        nearby_count = count_nearby(cells_copy, pos)
        if pos in cells_copy and (nearby_count < 2 or nearby_count > 3):
            cells.remove(pos)
        elif pos not in cells_copy and nearby_count == 3:
            cells.add(pos)


def solve_1(cells: Cells):
    new_cells = set()
    for cell in cells:
        new_cells.add(cell + (0,))
    cells = new_cells

    for cnt in range(6):
        iterate(cells)

    return len(cells)


def solve_2(cells: Cells):
    new_cells = set()
    for cell in cells:
        new_cells.add(cell + (0, 0))
    cells = new_cells

    for cnt in range(6):
        iterate(cells)

    return len(cells)


def main():
    cells = parse_file("aoc_17.txt")
    print("solve_1", solve_1(cells))
    print("solve_2", solve_2(cells))


if __name__ == "__main__":
    main()
