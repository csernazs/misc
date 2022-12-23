#!/usr/bin/env python3

from collections import defaultdict, deque
from dataclasses import dataclass
import sys
from typing import Iterable

import pytest

P = tuple[int, int]
PSET = set[P]


@dataclass
class Rule:
    checks: list[P]
    new_pos: P

    def check(self, pos: P, elves: PSET):
        for check in self.checks:
            p = (pos[0] + check[0], pos[1] + check[1])
            if p in elves:
                return False

        return True

    def move(self, pos: P, elves: PSET):
        if self.check(pos, elves):
            return (pos[0] + self.new_pos[0], pos[1] + self.new_pos[1])
        else:
            return pos


rules = deque(
    [
        Rule(checks=[(-1, 0), (-1, 1), (-1, -1)], new_pos=(-1, 0)),
        Rule(checks=[(1, 0), (1, 1), (1, -1)], new_pos=(1, 0)),
        Rule(checks=[(0, -1), (-1, -1), (1, -1)], new_pos=(0, -1)),
        Rule(checks=[(0, 1), (-1, 1), (1, 1)], new_pos=(0, 1)),
    ]
)


def get_neighbours(pos: P) -> PSET:
    return {
        (pos[0] + 1, pos[1] + 1),
        (pos[0] + 1, pos[1] - 1),
        (pos[0] + 1, pos[1]),
        (pos[0] - 1, pos[1] + 1),
        (pos[0] - 1, pos[1] - 1),
        (pos[0] - 1, pos[1]),
        (pos[0], pos[1] + 1),
        (pos[0], pos[1] - 1),
    }


def get_neighbours_elves(pos: P, elves: PSET) -> PSET:
    return elves.intersection(get_neighbours(pos))


def get_new_pos(pos: P, elves: PSET, rules: Iterable[Rule]):
    pass


def get_shape(elves: PSET) -> tuple[P, P]:
    min_row = 0
    min_col = 0
    max_row = 0
    max_col = 0

    st = 0

    for row, col in elves:
        if st == 0:
            min_row = row
            max_row = row
            min_col = col
            max_col = col
            st = 1

        if row < min_row:
            min_row = row
        if col < min_col:
            min_col = col

        if row > max_row:
            max_row = row
        if col > max_col:
            max_col = col

    return ((min_row, min_col), (max_row, max_col))


def empty_spaces(elves: PSET):
    tl, br = get_shape(elves)
    area = (br[0] - tl[0]) * (br[1] - tl[1])
    return area - len(elves)


def parse(lines: list[str]) -> PSET:
    retval: PSET = set()

    for rowidx, line in enumerate(lines):
        for colidx, char in enumerate(line):
            if char == "#":
                retval.add((rowidx, colidx))

    return retval


def print_elves(elves: PSET):
    tl, br = get_shape(elves)
    print(tl, br)
    for rowidx in range(tl[0], br[0] + 1):
        for colidx in range(tl[1], br[1] + 1):
            if (rowidx, colidx) in elves:
                sys.stdout.write("#")
            else:
                sys.stdout.write(".")
        sys.stdout.write("\n")


def part01(elves: PSET):
    # first half

    for _ in range(10):
        elves_list = list(elves)

        print_elves(elves)

        new_positions: dict[P, list[int]] = defaultdict(list)

        for idx, elf in enumerate(elves_list):
            print("processing", elf)
            neighbours = get_neighbours_elves(elf, elves)
            if not neighbours:
                print("stays")
                new_positions[elf].append(idx)
            else:
                for rule in rules:
                    new_pos = rule.move(elf, elves)
                    if new_pos != elf:
                        print("goes to", new_pos)
                        new_positions[new_pos].append(idx)
                        break
                else:  # not terminated by break
                    print("stays")
                    new_positions[elf].append(idx)

        new_elves: PSET = set()
        for pos, elf_indexes in new_positions.items():
            if len(elf_indexes) == 1:
                new_elves.add(pos)
            elif len(elf_indexes) > 1:
                for elf_idx in elf_indexes:
                    new_elves.add(elves_list[elf_idx])

        if new_elves == elves:
            return empty_spaces(elves)
        else:
            rules.rotate(-1)
            elves = new_elves

    return empty_spaces(elves)

def main():
    pass


@pytest.fixture
def sample() -> PSET:
    return {
        (0, 4),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 6),
        (2, 0),
        (2, 4),
        (2, 6),
        (3, 1),
        (3, 5),
        (3, 6),
        (4, 0),
        (4, 2),
        (4, 3),
        (4, 4),
        (5, 0),
        (5, 1),
        (5, 3),
        (5, 5),
        (5, 6),
        (6, 1),
        (6, 4),
    }


@pytest.fixture
def small_sample() -> PSET:
    return parse(
        [
            ".....",
            "..##.",
            "..#..",
            ".....",
            "..##.",
            ".....",
        ]
    )


def test_parse(sample: PSET):
    lines = [
        "....#..",
        "..###.#",
        "#...#.#",
        ".#...##",
        "#.###..",
        "##.#.##",
        ".#..#..",
    ]
    parsed = parse(lines)
    assert parsed == sample


def test_get_neighbours():
    assert get_neighbours((0, 0)) == {
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, -1),
        (0, 1),
    }


def test_get_shape():
    assert get_shape(set()) == ((0, 0), (0, 0))
    assert get_shape(
        {
            (1, 1),
        }
    ) == ((1, 1), (1, 1))
    assert get_shape({(1, 3), (5, 10)}) == ((1, 3), (5, 10))
    assert get_shape({(1, 3), (2, 4), (5, 10)}) == ((1, 3), (5, 10))


def test_part01(sample: PSET):
    assert part01(sample) == 110


def test_part01_small(small_sample: PSET):
    part01(small_sample)


if __name__ == "__main__":
    sys.exit(main())
