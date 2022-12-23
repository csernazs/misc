#!/usr/bin/env python3

from dataclasses import dataclass
from pprint import pprint
import re
import sys
from typing import Optional
import numpy as np
from numpy.typing import NDArray

P = tuple[int, int]


def try_int(x: str) -> str | int:
    try:
        return int(x)
    except ValueError:
        return x


@dataclass(frozen=True)
class Task:
    grid: NDArray
    instructions: list[int | str]


DOT = 1
EMPTY = 0
WALL = 2

RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (0, 1)
UP = (0, -1)

def part01(task: Task):
    grid = task.grid

    pos: Optional[P] = None
    dir: P = RIGHT
    for idx, cell in grid[0]:
        if cell == EMPTY:
            pos = (0, idx)
            break

    assert pos is not None

    for instr in task.instructions:
        if isinstance(instr, int):
            for cnt in range(instr):
                new_pos: P = (pos[0] + dir[0], pos[1] + dir[1])
                if grid[new_pos] == WALL:
                    break
                if grid[new_pos] == EMPTY:



def parse(lines: list[str]) -> Task:
    width = len(max(lines[:-2], key=len))
    height = len(lines) - 2

    rows = []
    for line in lines[:-2]:
        row = []
        for char in line:
            if char == " ":
                cell = 0
            elif char == ".":
                cell = 1
            elif char == "#":
                cell = 2
            else:
                raise ValueError(char)

            row.append(cell)

        assert len(row) <= width
        if len(row) < width:
            row.extend([0] * (width - len(row)))

        rows.append(row)

    array = np.array(rows)

    instructions = [try_int(x) for x in re.findall("\d+|L|R", lines[-1])]

    return Task(array, instructions)


def main():
    pass


def test_parse():
    lines = [
        "        ...#",
        "        .#..",
        "        #...",
        "        ....",
        "...#.......#",
        "........#...",
        "..#....#....",
        "..........#.",
        "        ...#....",
        "        .....#..",
        "        .#......",
        "        ......#.",
        "",
        "10R5L5R10L4R5L5",
    ]

    expected = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 1],
        ]
    )

    parsed = parse(lines)

    assert (parsed.grid == expected).all()
    assert parsed.instructions == [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5]


if __name__ == "__main__":
    sys.exit(main())
