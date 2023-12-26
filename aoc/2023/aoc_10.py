#!/usr/bin/env python3

import sys
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Container

import pytest

PAIR = tuple[int, int]

D_UP = (-1, 0)
D_DOWN = (1, 0)
D_RIGHT = (0, 1)
D_LEFT = (0, -1)


class Segment(ABC):
    def __init__(self, char: str):
        self.char = char

    @abstractmethod
    def transform(self, direction: PAIR) -> PAIR | None:
        pass

    def __eq__(self, other):
        if not isinstance(other, Segment):
            return NotImplemented

        return self.char == other.char


class UpDown(Segment):
    def transform(self, direction: PAIR) -> PAIR | None:
        if direction == D_DOWN or direction == D_UP:
            return direction


class LeftRight(Segment):
    def transform(self, direction: PAIR) -> PAIR | None:
        if direction == D_RIGHT or direction == D_LEFT:
            return direction


# L
class DownRight(Segment):
    def transform(self, direction: PAIR) -> PAIR | None:
        if direction == D_DOWN:
            return D_RIGHT

        if direction == D_LEFT:
            return D_UP


# F
class UpRight(Segment):
    def transform(self, direction: PAIR) -> PAIR | None:
        if direction == D_UP:
            return D_RIGHT
        if direction == D_LEFT:
            return D_DOWN


# 7
class UpLeft(Segment):
    def transform(self, direction: PAIR) -> PAIR | None:
        if direction == D_UP:
            return D_LEFT
        if direction == D_RIGHT:
            return D_DOWN


# J
class DownLeft(Segment):
    def transform(self, direction: PAIR) -> PAIR | None:
        if direction == D_DOWN:
            return D_LEFT
        if direction == D_RIGHT:
            return D_UP


class Empty(Segment):
    def transform(self, direction: PAIR) -> PAIR | None:
        return None


@dataclass
class Task:
    rows: list[list[Segment]]
    animal: PAIR


CHARMAP: dict[str, Segment] = {
    "|": UpDown("|"),
    "-": LeftRight("-"),
    "L": DownRight("L"),
    "F": UpRight("F"),
    "7": UpLeft("7"),
    "J": DownLeft("J"),
    "S": Empty("S"),
    ".": Empty("."),
}


def parse_lines(lines: list[str]) -> Task:
    rows: list[list[Segment]] = []
    animal_pos: PAIR | None = None

    for row_idx, line in enumerate(lines):
        row: list[Segment] = []
        for col_idx, char in enumerate(line):
            if char == "S":
                animal_pos = (row_idx, col_idx)
            row.append(CHARMAP[char])
        rows.append(row)

    assert animal_pos is not None
    return Task(rows, animal_pos)


def get_route(task: Task) -> list[PAIR]:
    matrix = task.rows
    pos = task.animal

    direction: PAIR = (0, 0)
    if matrix[pos[0]][pos[1] + 1].char in "7-J":
        pos = (pos[0], pos[1] + 1)
        direction = (0, 1)

    elif matrix[pos[0]][pos[1] - 1].char in "L-F":
        pos = (pos[0], pos[1] + 1)
        direction = (0, -1)

    elif matrix[pos[0] - 1][pos[1]].char in "|F7":
        pos = (pos[0] - 1, pos[1])
        direction = (-1, 0)

    elif matrix[pos[0] + 1][pos[1]].char in "|JL":
        pos = (pos[0] + 1, pos[1])
        direction = (1, 0)

    else:
        raise ValueError(f"Unable to start: {pos}")

    route: list[PAIR] = [pos]
    while pos != task.animal:
        new_dir = matrix[pos[0]][pos[1]].transform(direction)
        assert new_dir is not None
        new_pos = (pos[0] + new_dir[0], pos[1] + new_dir[1])
        route.append(new_pos)
        pos = new_pos
        direction = new_dir

    print(route)
    return route


def get_inside_points(task: Task, route: list[PAIR]) -> list[PAIR]:
    route_points = set(route)
    oldpos: PAIR | None = None
    direction: PAIR | None = None
    initial_direction: PAIR | None = None

    retval: list[PAIR] = []
    for pos in route:
        if oldpos is None:
            oldpos = pos
            continue

        if direction is None:
            initial_direction = (pos[0] - oldpos[0], pos[1] - oldpos[1])
            direction = initial_direction
        else:
            direction = (pos[0] - oldpos[0], pos[1] - oldpos[1])

        assert initial_direction is not None

        if initial_direction == (0, 1) or initial_direction == (-1, 0):
            if direction == (0, 1):
                candidate = (pos[0] + 1, pos[1])
            elif direction == (0, -1):
                candidate = (pos[0] - 1, pos[1])
            elif direction == (1, 0):
                candidate = (pos[0], pos[1] - 1)
            elif direction == (-1, 0):
                candidate = (pos[0], pos[1] + 1)
            else:
                raise ValueError(f"Invalid direction: {direction}")

        elif initial_direction == (0, -1) or initial_direction == (1, 0):
            if direction == (0, 1):
                candidate = (pos[0] - 1, pos[1])
            elif direction == (0, -1):
                candidate = (pos[0] + 1, pos[1])
            elif direction == (1, 0):
                candidate = (pos[0], pos[1] + 1)
            elif direction == (-1, 0):
                candidate = (pos[0], pos[1] - 1)
            else:
                raise ValueError(f"Invalid direction: {direction}")
        else:
            raise ValueError(initial_direction)

        if candidate not in route_points and candidate not in retval:
            retval.append(candidate)

        oldpos = pos

    return retval


def fill(route: Container[PAIR], start_pos: PAIR):
    queue = deque([start_pos])

    retval: set[PAIR] = set((start_pos,))

    while queue:
        pos = queue.popleft()
        candidates: list[PAIR] = []
        candidates.append((pos[0] - 1, pos[1]))
        candidates.append((pos[0] + 1, pos[1]))
        candidates.append((pos[0], pos[1] - 1))
        candidates.append((pos[0], pos[1] + 1))

        for candidate in candidates:
            if candidate not in route and candidate not in retval:
                queue.append(candidate)
                retval.add(candidate)

    return retval


def print_points(height: int, width: int, route_points: set[PAIR], inside_points: set[PAIR] | None = None):
    for row_idx in range(height):
        for col_idx in range(width):
            if (row_idx, col_idx) in route_points:
                sys.stdout.write("*")
            elif inside_points is not None and (row_idx, col_idx) in inside_points:
                sys.stdout.write("I")
            else:
                sys.stdout.write(".")
        sys.stdout.write("\n")
    print()


def part_01(route: list[PAIR]) -> int:
    return len(route) // 2


def part_02(task: Task, route: list[PAIR]) -> int:
    inside = get_inside_points(task, route)
    all_inside: set[PAIR] = set()
    route_set = set(route)
    for pos in inside:
        print(pos)
        new_inside = fill(route_set, pos)
        all_inside.update(new_inside)

    print_points(len(task.rows), len(task.rows[0]), route_set, all_inside)
    return len(all_inside)


def main():
    with open("aoc_10.txt") as infile:
        lines = [line.strip() for line in infile]

    task = parse_lines(lines)
    route = get_route(task)
    print_points(height=len(task.rows), width=len(task.rows[0]), route_points=set(route))
    print(part_01(route))
    print(part_02(task, route))


@pytest.fixture()
def task() -> Task:
    v = CHARMAP["|"]
    h = CHARMAP["-"]
    l = CHARMAP["L"]
    f = CHARMAP["F"]
    se = CHARMAP["7"]
    j = CHARMAP["J"]
    s = CHARMAP["S"]
    e = CHARMAP["."]

    return Task(
        [[e, e, f, se, e], [e, f, j, v, e], [s, j, e, l, se], [v, f, h, h, j], [l, j, e, e, e]],
        (2, 0),
    )


@pytest.fixture()
def route() -> list[PAIR]:
    return [
        (2, 1),
        (1, 1),
        (1, 2),
        (0, 2),
        (0, 3),
        (1, 3),
        (2, 3),
        (2, 4),
        (3, 4),
        (3, 3),
        (3, 2),
        (3, 1),
        (4, 1),
        (4, 0),
        (3, 0),
        (2, 0),
    ]


def test_parse(task: Task):
    lines = [
        "..F7.",
        ".FJ|.",
        "SJ.L7",
        "|F--J",
        "LJ...",
    ]
    assert parse_lines(lines) == task


def test_get_route(task: Task, route: list[PAIR]):
    assert get_route(task) == route


def test_part01(route: list[PAIR]):
    assert part_01(route) == 8


def test_get_inside_points():
    lines = [
        "...........",
        ".S-------7.",
        ".|F-----7|.",
        ".||.....||.",
        ".||.....||.",
        ".|L-7.F-J|.",
        ".|..|.|..|.",
        ".L--J.L--J.",
        "...........",
    ]
    task = parse_lines(lines)
    route = get_route(task)
    inside = get_inside_points(task, route)
    print_points(9, 11, set(route), set(inside))
    assert inside == [(6, 8), (6, 7), (6, 3), (6, 2)]


if __name__ == "__main__":
    sys.exit(main())
