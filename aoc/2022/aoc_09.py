#!/usr/bin/env python3

import sys
from typing import List, Tuple

import pytest

T_STEPS = List[Tuple[str, int]]


def parse(lines: List[str]) -> T_STEPS:
    retval = []
    for line in lines:
        dir, length_s = line.split()
        length = int(length_s)
        retval.append((dir, length))
    return retval


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, dir: str):
        if dir == "U":
            self.y += 1
        elif dir == "D":
            self.y -= 1
        elif dir == "R":
            self.x += 1
        elif dir == "L":
            self.x -= 1
        else:
            raise ValueError(dir)

    def adjust_for_head(self, head: "Position") -> bool:
        diff_x = head.x - self.x
        diff_y = head.y - self.y

        transitions = {
            (-2, 0): (-1, 0),
            (2, 0): (1, 0),
            (0, -2): (0, -1),
            (0, 2): (0, 1),
            (-2, 1): (-1, 1),
            (2, 1): (1, 1),
            (1, -2): (1, -1),
            (1, 2): (1, 1),
            (-2, -1): (-1, -1),
            (2, -1): (1, -1),
            (-1, -2): (-1, -1),
            (-1, 2): (-1, 1),
            (-2, -2): (-1, -1),
            (2, 2): (1, 1),
            (2, -2): (1, -1),
            (-2, 2): (-1, 1),
        }

        if (diff_x, diff_y) in transitions:
            step_x, step_y = transitions[(diff_x, diff_y)]
            self.x += step_x
            self.y += step_y
            return True

        return False

    def __repr__(self) -> str:
        return f"<x={self.x} y={self.y}>"

    @property
    def as_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


def show(head: Position, tail: Position):
    for y in range(10):
        for x in range(10):
            if head.x == x and head.y == y:
                sys.stdout.write("H")
            elif tail.x == x and tail.y == y:
                sys.stdout.write("T")
            else:
                sys.stdout.write(".")
        sys.stdout.write("\n")


def part01aaa(steps: T_STEPS) -> int:
    head = Position(0, 0)
    tail = Position(0, 0)
    seen_positions: set[Tuple[int, int]] = set()

    seen_positions.add(tail.as_tuple)

    for dir, length in steps:
        for _ in range(length):
            head.move(dir)
            tail.adjust_for_head(head)
            seen_positions.add(tail.as_tuple)

    return len(seen_positions)


def solve(steps: T_STEPS, rope_length: int) -> int:
    knots: List[Position] = [Position(0, 0) for _ in range(rope_length)]
    seen_positions: set[Tuple[int, int]] = set()

    for dir, length in steps:
        for _ in range(length):
            knots[0].move(dir)
            for idx, pos in enumerate(knots[1:]):
                pos.adjust_for_head(knots[idx])
            if len(knots) == rope_length:
                seen_positions.add(knots[-1].as_tuple)

    return len(seen_positions)


def part01(steps: T_STEPS) -> int:
    return solve(steps, 2)


def part02(steps: T_STEPS) -> int:
    return solve(steps, 10)


def main():
    with open("aoc_09.txt") as infile:
        lines = [x.strip() for x in infile]
    steps = parse(lines)
    print(part01(steps))
    print(part02(steps))


@pytest.fixture
def example1():
    return [
        ("R", 4),
        ("U", 4),
        ("L", 3),
        ("D", 1),
        ("R", 4),
        ("D", 1),
        ("L", 5),
        ("R", 2),
    ]


@pytest.fixture
def example2():
    return [
        ("R", 5),
        ("U", 8),
        ("L", 8),
        ("D", 3),
        ("R", 17),
        ("D", 10),
        ("L", 25),
        ("U", 20),
    ]


def test_parse(example1: T_STEPS):
    lines = [
        "R 4",
        "U 4",
        "L 3",
        "D 1",
        "R 4",
        "D 1",
        "L 5",
        "R 2",
    ]

    assert parse(lines) == example1


def test_part01(example1: T_STEPS):
    assert part01(example1) == 13


def test_part02_example1(example1: T_STEPS):
    assert part02(example1) == 1


def test_part02_example2(example2: T_STEPS):
    assert part02(example2) == 36


if __name__ == "__main__":
    sys.exit(main())
