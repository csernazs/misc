#!/usr/bin/env python3

import re
import sys
from dataclasses import dataclass
from typing import Iterable

import pytest

POS = tuple[int, int]


@dataclass(frozen=True)
class Number:
    value: int
    pos: POS

    def iter_neigh(self) -> Iterable[POS]:
        length = len(str(self.value))

        yield ((self.pos[0], self.pos[1] - 1))
        yield ((self.pos[0], self.pos[1] + length))

        for offset in range(-1, length + 1):
            yield ((self.pos[0] - 1, self.pos[1] + offset))
            yield ((self.pos[0] + 1, self.pos[1] + offset))


@dataclass
class Task:
    numbers: list[Number]
    symbols: dict[POS, str]


def iter_neigh_symbols(number: Number, symbols: dict[POS, str]) -> Iterable[tuple[int, int, str]]:
    for pos in number.iter_neigh():
        if pos in symbols:
            yield (pos[0], pos[1], symbols[pos])


def parse_lines(lines: list[str]) -> Task:
    numbers: list[Number] = []
    symbols: dict[POS, str] = {}

    for row_idx, line in enumerate(lines):
        for match in re.finditer(r"\d+", line):
            n = Number(value=int(match.group(0)), pos=(row_idx, match.start()))
            numbers.append(n)

        for col_idx, char in enumerate(line):
            if char not in "0123456789.":
                symbols[(row_idx, col_idx)] = char

    return Task(numbers=numbers, symbols=symbols)


def part_01(task: Task) -> int:
    retval: int = 0
    for number in task.numbers:
        for pos in number.iter_neigh():
            if pos in task.symbols:
                retval += number.value
                break
    return retval


def part_02(task: Task) -> int:
    symbol_numbers: dict[POS, set[Number]] = {}

    for number in task.numbers:
        for row, col, symbol in iter_neigh_symbols(number, task.symbols):
            if symbol == "*":
                symbol_pos = (row, col)
                if symbol_pos in symbol_numbers:
                    symbol_numbers[symbol_pos].add(number)
                else:
                    symbol_numbers[symbol_pos] = set([number])
    retval = 0

    for symbol_pos, numbers in symbol_numbers.items():
        if len(numbers) == 2:
            retval += numbers.pop().value * numbers.pop().value

    return retval


def main():
    with open("aoc_03.txt") as infile:
        lines = [x.strip() for x in infile]

    task = parse_lines(lines)
    print(part_01(task))
    print(part_02(task))


@pytest.fixture()
def task() -> Task:
    return Task(
        numbers=[
            Number(value=467, pos=(0, 0)),
            Number(value=114, pos=(0, 5)),
            Number(value=35, pos=(2, 2)),
            Number(value=633, pos=(2, 6)),
            Number(value=617, pos=(4, 0)),
            Number(value=58, pos=(5, 7)),
            Number(value=592, pos=(6, 2)),
            Number(value=755, pos=(7, 6)),
            Number(value=664, pos=(9, 1)),
            Number(value=598, pos=(9, 5)),
        ],
        symbols={(1, 3): "*", (3, 6): "#", (4, 3): "*", (5, 5): "+", (8, 3): "$", (8, 5): "*"},
    )


def test_parse(task: Task):
    lines = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]

    assert parse_lines(lines) == task


def test_iter_neigh():
    number = Number(value=456, pos=(3, 10))
    assert set(number.iter_neigh()) == {
        (2, 9),
        (2, 10),
        (2, 11),
        (2, 12),
        (2, 13),
        (3, 13),
        (3, 9),
        (4, 9),
        (4, 10),
        (4, 11),
        (4, 12),
        (4, 13),
    }


def test_part01(task: Task):
    assert part_01(task) == 4361


def test_part02(task: Task):
    assert part_02(task) == 467835


if __name__ == "__main__":
    sys.exit(main())
