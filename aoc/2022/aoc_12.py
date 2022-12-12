#!/usr/bin/env python3

import sys
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pytest
from numpy.typing import NDArray

POS = tuple[int, int]


@dataclass(eq=True)
class Field:
    map: NDArray
    end: POS
    start: POS

    def get_neighbours(self, current: POS) -> list[POS]:
        candidates = []

        if current[0] > 0:
            candidates.append((current[0] - 1, current[1]))

        if current[0] < self.map.shape[0] - 1:
            candidates.append((current[0] + 1, current[1]))

        if current[1] > 0:
            candidates.append((current[0], current[1] - 1))

        if current[1] < self.map.shape[1] - 1:
            candidates.append((current[0], current[1] + 1))

        return candidates


def parse(lines: list[str]):
    ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"
    letter_to_int = {k: v for v, k in enumerate(ascii_lowercase)}
    letter_to_int["S"] = letter_to_int["a"]
    letter_to_int["E"] = letter_to_int["z"]

    points: list[int] = []
    height = len(lines)

    for rowidx, line in enumerate(lines):
        width = len(line)

        for colidx, c in enumerate(line):
            if c == "S":
                start = (rowidx, colidx)
            elif c == "E":
                end = (rowidx, colidx)
            points.append(letter_to_int[c])

    array = np.array(points).reshape(height, width)
    return Field(array, end, start)


@dataclass(frozen=True)
class Item:
    pos: POS
    distance: int


class Solver(ABC):
    def __init__(self, field: Field):
        self.field = field

    @abstractmethod
    def is_final(self, current: POS) -> bool:
        pass

    @abstractmethod
    def is_candidate(self, current: POS, candidate: POS) -> bool:
        pass

    def solve(
        self,
        current: POS,
        distance: int = 0,
    ) -> Optional[int]:

        queue: deque[Item] = deque()

        visited = np.ones(self.field.map.shape, dtype=np.int32) * 1000000

        queue.append(Item(current, 0))

        while queue:
            item = queue.popleft()
            current, distance = (item.pos, item.distance)

            if distance >= visited[current]:
                continue

            if self.is_final(current):
                return distance

            visited[current] = distance

            candidates = self.field.get_neighbours(current)
            for candidate_pos in candidates:
                if visited[candidate_pos] > distance + 1 and self.is_candidate(current, candidate_pos):
                    queue.append(Item(candidate_pos, distance + 1))

        return None


class Part01Solver(Solver):
    def is_final(self, current: POS) -> bool:
        return current == self.field.end

    def is_candidate(self, current: POS, candidate: POS) -> bool:
        return self.field.map[candidate] - self.field.map[current] <= 1


class Part02Solver(Solver):
    def is_final(self, current: POS) -> bool:
        return self.field.map[current] == 0

    def is_candidate(self, current: POS, candidate: POS) -> bool:
        return self.field.map[current] - self.field.map[candidate] <= 1


def part01(field: Field) -> Optional[int]:
    solver = Part01Solver(field)
    return solver.solve(field.start)


def part02(field: Field) -> Optional[int]:
    solver = Part02Solver(field)
    return solver.solve(field.end)


def main():
    with open("aoc_12.txt") as infile:
        lines = [x.strip() for x in infile]

    field = parse(lines)
    print(part01(field))
    print(part02(field))


@pytest.fixture
def field() -> Field:
    lines = [
        "Sabqponm",
        "abcryxxl",
        "accszExk",
        "acctuvwj",
        "abdefghi",
    ]
    return parse(lines)


def test_parse():
    lines = [
        "Sabqponm",
        "abcryxxl",
        "accszExk",
        "acctuvwj",
        "abdefghi",
    ]
    field = parse(lines)
    expected = np.array(
        [
            [0, 0, 1, 16, 15, 14, 13, 12],
            [0, 1, 2, 17, 24, 23, 23, 11],
            [0, 2, 2, 18, 25, 25, 23, 10],
            [0, 2, 2, 19, 20, 21, 22, 9],
            [0, 1, 3, 4, 5, 6, 7, 8],
        ]
    )
    assert (field.map == expected).all()
    assert field.end == (2, 5)
    assert field.start == (0, 0)


def test_part01(field: Field):
    assert part01(field) == 31


def test_part02(field: Field):
    assert part02(field) == 29


if __name__ == "__main__":
    sys.exit(main())
