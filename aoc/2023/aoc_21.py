#!/usr/bin/env python3


import sys
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Container

import numpy as np
import pytest
from numpy.typing import NDArray

PLOT = 1
ROCK = 2
START = 3

PAIR = tuple[int, int]
GRID = NDArray[np.int64]


def iter_neigh(array: NDArray[np.int64], pos: PAIR) -> Iterator[tuple[PAIR, int]]:
    if pos[0] > 0:
        new_pos = (pos[0] - 1, pos[1])
        yield (new_pos, array[new_pos])

    if pos[0] < array.shape[0]:
        new_pos = (pos[0] + 1, pos[1])
        yield (new_pos, array[new_pos])

    if pos[1] > 0:
        new_pos = (pos[0], pos[1] - 1)
        yield (new_pos, array[new_pos])

    if pos[1] < array.shape[1]:
        new_pos = (pos[0], pos[1] + 1)
        yield (new_pos, array[new_pos])


def parse_to_grid(
    lines: list[str], value_map: dict[str, int], default: int | None = None
) -> NDArray[np.int64]:
    rows: list[list[int]] = []

    for line in lines:
        row: list[int] = []
        for char in line:
            if default is not None:
                row.append(value_map.get(char, default))
            else:
                if (value := value_map.get(char)) is not None:
                    row.append(value)
                else:
                    raise ValueError(char)
        rows.append(row)

    retval: NDArray[np.int64] = np.array(rows, dtype=np.int64)
    return retval


@dataclass(frozen=True)
class WorkItem:
    pos: PAIR
    step: int


def print_grid(grid: GRID, points: Container[PAIR]):
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if (row_idx, col_idx) in points:
                sys.stdout.write("O")
            elif value == PLOT:
                sys.stdout.write(".")
            elif value == ROCK:
                sys.stdout.write("#")
            elif value == START:
                sys.stdout.write("S")
        sys.stdout.write("\n")


def part_01(grid: GRID, step_max: int) -> int:
    a = np.where(grid == START)
    start_pos: PAIR = (a[0][0], a[1][0])

    queue: deque[WorkItem] = deque([WorkItem(pos=start_pos, step=0)])
    seen: set[PAIR] = set()
    last_iteration: set[PAIR] = set()

    min_steps: dict[PAIR, int] = {}

    while queue:
        item = queue.popleft()
        print(item.step)

        if item.pos not in min_steps:
            min_steps[item.pos] = item.step

        if item.step >= step_max:
            last_iteration.add(item.pos)
            continue

        for neigh_pos, neigh_value in iter_neigh(grid, item.pos):
            if neigh_value == ROCK:
                continue
            if neigh_pos in seen:
                continue
            seen.add(neigh_pos)
            queue.append(WorkItem(neigh_pos, item.step + 1))

    cnt = 0
    show: set[PAIR] = set()

    for pos, step in min_steps.items():
        if (step_max - step) % 2 == 0:
            cnt += 1
            show.add(pos)

    print_grid(grid, show)
    return cnt


def parse_lines(lines: list[str]) -> NDArray[np.int64]:
    retval = parse_to_grid(lines, {".": PLOT, "#": ROCK, "S": START})
    return retval


def main():
    with open("aoc_21.txt") as infile:
        lines = [line.strip() for line in infile]

    grid = parse_lines(lines)
    print(part_01(grid, step_max=64))


def test_parse(grid: GRID):
    lines = [
        "...........",
        ".....###.#.",
        ".###.##..#.",
        "..#.#...#..",
        "....#.#....",
        ".##..S####.",
        ".##..#...#.",
        ".......##..",
        ".##.#.####.",
        ".##..##.##.",
        "...........",
    ]
    assert (parse_lines(lines) == grid).all()


@pytest.fixture(name="grid")
def fixture_grid() -> NDArray[np.int64]:
    return np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1],
            [1, 2, 2, 2, 1, 2, 2, 1, 1, 2, 1],
            [1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1],
            [1, 2, 2, 1, 1, 3, 2, 2, 2, 2, 1],
            [1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1],
            [1, 2, 2, 1, 2, 1, 2, 2, 2, 2, 1],
            [1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    )


def test_part01(grid: GRID):
    assert part_01(grid, 6) == 16


if __name__ == "__main__":
    sys.exit(main())
