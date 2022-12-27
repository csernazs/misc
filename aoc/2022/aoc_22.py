#!/usr/bin/env python3

from pathlib import Path
import re
import sys
from dataclasses import dataclass
from pprint import pprint
from typing import Optional

import numpy as np
import PIL.Image
import PIL.ImageDraw
import pytest
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


EMPTY = 1
DOT = 2
WALL = 3
PLAYER = 4

RIGHT = (0, 1)
LEFT = (0, -1)
DOWN = (1, 0)
UP = (-1, 0)


class ImageWriter:
    def __init__(self, target_dir: Path, resize_factor: int = 1):
        self.target_dir = target_dir
        self.frame_no = 0
        self.resize_factor = resize_factor
        self.color_map: dict[int, tuple[int, int, int]] = {
            EMPTY: (127, 127, 127),
            DOT: (0, 0, 0),
            WALL: (255, 0, 0),
            PLAYER: (255, 255, 255),
        }

    def get_raw_color_map(self, color_size: int = 3) -> list[int]:
        palette = [0] * (255 * color_size)
        for color_id, color_tuple in self.color_map.items():
            for offset in range(color_size):
                palette[color_id * 3 + offset] = color_tuple[offset]

        return palette

    def save(self, grid: NDArray, player: P):
        if not self.target_dir.is_dir():
            return

        im = PIL.Image.new(mode="RGB", size=(grid.shape[1], grid.shape[0]))

        for rowidx, row in enumerate(grid):
            for colidx, cell in enumerate(row):
                if player == (rowidx, colidx):
                    color = self.color_map[PLAYER]
                else:
                    color = self.color_map[cell]
                im.putpixel((colidx, rowidx), color)

        with self.target_dir.joinpath(f"img_{self.frame_no:05}.png").open("wb") as outfile:
            im.resize(
                (im.size[0] * self.resize_factor, im.size[1] * self.resize_factor),
                resample=PIL.Image.Resampling.NEAREST,
            ).save(outfile, "PNG")

        self.frame_no += 1


def parse(lines: list[str]) -> Task:
    width = len(max(lines[:-2], key=len))

    rows = []
    for line in lines[:-2]:
        row = []
        for char in line:
            if char == " ":
                cell = EMPTY
            elif char == ".":
                cell = DOT
            elif char == "#":
                cell = WALL
            else:
                raise ValueError(char)

            row.append(cell)

        assert len(row) <= width
        if len(row) < width:
            row.extend([EMPTY] * (width - len(row)))

        rows.append(row)

    array = np.array(rows)

    instructions = [try_int(x) for x in re.findall(r"\d+|L|R", lines[-1])]

    return Task(array, instructions)


def find_next_pos(grid: NDArray, pos: P, dir: P) -> P:
    new_pos_mut: list[int] = [pos[0] + dir[0], pos[1] + dir[1]]
    shape = grid.shape

    if new_pos_mut[0] < 0:
        new_pos_mut[0] = shape[0] - 1
    elif new_pos_mut[0] > shape[0] - 1:
        new_pos_mut[0] = 0

    if new_pos_mut[1] < 0:
        new_pos_mut[1] = shape[1] - 1
    elif new_pos_mut[1] > shape[1] - 1:
        new_pos_mut[1] = 0

    new_pos: P = (new_pos_mut[0], new_pos_mut[1])

    if grid[new_pos] == WALL:
        return pos

    return new_pos


def find_next_valid_pos(grid: NDArray, pos: P, dir: P) -> P:
    orig_pos = pos
    while True:
        new_pos = find_next_pos(grid, pos, dir)
        if new_pos == pos:
            if grid[pos] == EMPTY:
                return orig_pos
            else:
                return pos

        if grid[new_pos] == EMPTY:
            pos = new_pos
            continue

        if grid[new_pos] == DOT:
            return new_pos


def rotate_right(dir: P) -> P:
    map: dict[P, P] = {
        RIGHT: DOWN,
        DOWN: LEFT,
        LEFT: UP,
        UP: RIGHT,
    }
    return map[dir]


def rotate_left(dir: P) -> P:
    map: dict[P, P] = {
        RIGHT: UP,
        UP: LEFT,
        LEFT: DOWN,
        DOWN: RIGHT,
    }
    return map[dir]


def print_grid(grid: NDArray, pos: P):
    print("=" * grid.shape[1])
    for rowidx, row in enumerate(grid):
        for colidx, cell in enumerate(row):
            if pos == (rowidx, colidx):
                sys.stdout.write("@")
            elif cell == WALL:
                sys.stdout.write("#")
            elif cell == EMPTY:
                sys.stdout.write(" ")
            elif cell == DOT:
                sys.stdout.write(".")
            else:
                raise ValueError(cell)

        sys.stdout.write("\n")
    print("=" * grid.shape[1])


def part01(task: Task):
    grid = task.grid

    imgwriter = ImageWriter(Path("/tmp/images"), resize_factor=5)

    pos: Optional[P] = None
    dir: P = RIGHT
    for idx, cell in enumerate(grid[0]):
        if cell == DOT:
            pos = (0, idx)
            break

    assert pos is not None

    for instr in task.instructions:
        assert grid[pos] == DOT
        print("processing", instr)
        if isinstance(instr, int):
            for cnt in range(instr):
                print("cnt", cnt)
                new_pos = find_next_valid_pos(grid, pos, dir)
                assert grid[new_pos] == DOT
                if new_pos == pos:
                    break
                pos = new_pos
                imgwriter.save(grid, pos)

        elif isinstance(instr, str):
            if instr == "R":
                dir = rotate_right(dir)
            elif instr == "L":
                dir = rotate_left(dir)
            else:
                raise ValueError(f"No such instr: {instr!r}")
        else:
            raise TypeError(instr)

    facing_map = {RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3}
    solution = ((pos[0] + 1) * 1000) + ((pos[1] + 1) * 4) + facing_map[dir]
    return solution


def main():
    with open("aoc_22.txt") as infile:
        lines = [x.rstrip() for x in infile]

    task = parse(lines)
    print(part01(task))


@pytest.fixture
def sample() -> Task:
    grid = np.array(
        [
            [
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                DOT,
                DOT,
                DOT,
                WALL,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
            ],
            [
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                DOT,
                WALL,
                DOT,
                DOT,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
            ],
            [
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                WALL,
                DOT,
                DOT,
                DOT,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
            ],
            [
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                DOT,
                DOT,
                DOT,
                DOT,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
            ],
            [
                DOT,
                DOT,
                DOT,
                WALL,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                WALL,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
            ],
            [
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                WALL,
                DOT,
                DOT,
                DOT,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
            ],
            [
                DOT,
                DOT,
                WALL,
                DOT,
                DOT,
                DOT,
                DOT,
                WALL,
                DOT,
                DOT,
                DOT,
                DOT,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
            ],
            [
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                WALL,
                DOT,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
            ],
            [
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                DOT,
                DOT,
                DOT,
                WALL,
                DOT,
                DOT,
                DOT,
                DOT,
            ],
            [
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                WALL,
                DOT,
                DOT,
            ],
            [
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                DOT,
                WALL,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
            ],
            [
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                EMPTY,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                DOT,
                WALL,
                DOT,
            ],
        ]
    )
    instr: list[str | int] = [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5]

    return Task(grid, instr)


def test_parse(sample: Task):
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

    parsed = parse(lines)

    assert (parsed.grid == sample.grid).all()
    assert parsed.instructions == sample.instructions


def test_part01(sample: Task):
    assert part01(sample) == 6032


def test_find_next_valid_pos():
    array = np.array([EMPTY, EMPTY, DOT, DOT, WALL, DOT]).reshape(1, 6)
    new_pos = find_next_valid_pos(array, pos=(0, 2), dir=RIGHT)
    assert new_pos == (0, 3)

    array = np.array([DOT, WALL, DOT, DOT, WALL, DOT]).reshape(1, 6)
    new_pos = find_next_valid_pos(array, pos=(0, 5), dir=RIGHT)
    assert new_pos == (0, 0)

    array = np.array([WALL, WALL, DOT, DOT, DOT, DOT]).reshape(1, 6)
    new_pos = find_next_valid_pos(array, pos=(0, 5), dir=RIGHT)
    assert new_pos == (0, 5)

    new_pos = find_next_valid_pos(array, pos=(0, 4), dir=RIGHT)
    assert new_pos == (0, 5)

    new_pos = find_next_valid_pos(array, pos=(0, 3), dir=RIGHT)
    assert new_pos == (0, 4)

    new_pos = find_next_valid_pos(array, pos=(0, 2), dir=RIGHT)
    assert new_pos == (0, 3)

    array = np.array([WALL, WALL, DOT, DOT, DOT, DOT, EMPTY, EMPTY]).reshape(1, 8)
    new_pos = find_next_valid_pos(array, pos=(0, 5), dir=RIGHT)
    assert new_pos == (0, 5)

    new_pos = find_next_valid_pos(array, pos=(0, 4), dir=RIGHT)
    assert new_pos == (0, 5)

    array = np.array([EMPTY, EMPTY, DOT, DOT, WALL, DOT]).reshape(6, 1)
    new_pos = find_next_valid_pos(array, pos=(2, 0), dir=DOWN)
    assert new_pos == (3, 0)

    array = np.array([DOT, WALL, DOT, DOT, WALL, DOT]).reshape(6, 1)
    new_pos = find_next_valid_pos(array, pos=(5, 0), dir=DOWN)
    assert new_pos == (0, 0)

    array = np.array([WALL, WALL, DOT, DOT, DOT, DOT]).reshape(6, 1)
    new_pos = find_next_valid_pos(array, pos=(5, 0), dir=DOWN)
    assert new_pos == (5, 0)

    new_pos = find_next_valid_pos(array, pos=(4, 0), dir=DOWN)
    assert new_pos == (5, 0)

    new_pos = find_next_valid_pos(array, pos=(3, 0), dir=DOWN)
    assert new_pos == (4, 0)

    new_pos = find_next_valid_pos(array, pos=(2, 0), dir=DOWN)
    assert new_pos == (3, 0)


if __name__ == "__main__":
    sys.exit(main())
