#!/usr/bin/env python3

import sys

import pytest


def parse_lines(lines: list[str]) -> list[list[int]]:
    retval: list[list[int]] = []
    for line in lines:
        retval.append([int(x) for x in line.split()])
    return retval


def calculate_rows(ints: list[int]) -> list[list[int]]:
    rows: list[list[int]] = []
    last_row = ints
    while True:
        new_row: list[int] = []
        for pair in [last_row[idx : idx + 2] for idx in range(len(last_row) - 1)]:
            new_row.append(pair[1] - pair[0])
        rows.append(new_row)
        last_row = new_row
        if new_row == len(new_row) * [0]:
            break
    return rows


def solve_task_1(task: list[int]) -> int:
    rows = calculate_rows(task)

    rows.reverse()
    rows[0].append(0)
    for idx in range(1, len(rows)):
        rows[idx].append(rows[idx - 1][-1] + rows[idx][-1])

    return rows[-1][-1] + task[-1]


def solve_task_2(task: list[int]) -> int:
    rows = calculate_rows(task)
    rows.reverse()
    rows[0].append(0)
    for idx in range(1, len(rows)):
        rows[idx].insert(0, rows[idx][0] - rows[idx - 1][0])

    return task[0] - rows[-1][0]


def part_01(ints: list[list[int]]) -> int:
    ints = [x[:] for x in ints]
    retval = 0
    for task in ints:
        retval += solve_task_1(task)

    return retval


def part_02(ints: list[list[int]]) -> int:
    ints = [x[:] for x in ints]

    retval = 0
    for task in ints:
        retval += solve_task_2(task)
    return retval


def main():
    with open("aoc_09.txt") as infile:
        lines = [line.strip() for line in infile]

    ints = parse_lines(lines)
    print(part_01(ints))
    print(part_02(ints))


@pytest.fixture()
def ints():
    return [
        [
            0,
            3,
            6,
            9,
            12,
            15,
        ],
        [
            1,
            3,
            6,
            10,
            15,
            21,
        ],
        [10, 13, 16, 21, 30, 45],
    ]


def test_parse(ints: list[list[int]]):
    lines = [
        "0 3 6 9 12 15",
        "1 3 6 10 15 21",
        "10 13 16 21 30 45",
    ]
    assert parse_lines(lines) == ints


def test_part01(ints: list[list[int]]):
    assert part_01(ints) == 114


def test_part02(ints: list[list[int]]):
    assert part_02(ints) == 2


if __name__ == "__main__":
    sys.exit(main())
