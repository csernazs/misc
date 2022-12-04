#!/usr/bin/env python3

import sys
from textwrap import dedent
from typing import Iterable

import pytest

T_PAIRS = list[tuple[tuple[int, int], tuple[int, int]]]


def parse(lines: list[str]) -> T_PAIRS:
    retval: T_PAIRS = []

    for line in lines:
        left, right = line.split(",")
        left_pair = tuple([int(x) for x in left.split("-")])
        right_pair = tuple([int(x) for x in right.split("-")])
        assert len(left_pair) == 2
        assert len(right_pair) == 2
        retval.append(((left_pair[0], left_pair[1]), (right_pair[0], right_pair[1])))

    return retval


def iter_sets(pairs_list: T_PAIRS) -> Iterable[tuple[set, set]]:
    for pairs in pairs_list:
        left_pair = pairs[0]
        right_pair = pairs[1]
        left_set = set(range(left_pair[0], left_pair[1] + 1))
        right_set = set(range(right_pair[0], right_pair[1] + 1))
        yield (left_set, right_set)


def part01(pairs_list: T_PAIRS) -> int:
    cnt = 0
    for left_set, right_set in iter_sets(pairs_list):
        if left_set.issubset(right_set) or right_set.issubset(left_set):
            cnt += 1
    return cnt


def part02(pairs_list: T_PAIRS) -> int:
    cnt = 0
    for left_set, right_set in iter_sets(pairs_list):
        if left_set.intersection(right_set):
            cnt += 1
    return cnt


def main():
    with open("aoc_04.txt") as infile:
        lines = [x.strip() for x in infile]

    pairs = parse(lines)

    print(part01(pairs))
    print(part02(pairs))


@pytest.fixture
def sample():
    return [
        ((2, 4), (6, 8)),
        ((2, 3), (4, 5)),
        ((5, 7), (7, 9)),
        ((2, 8), (3, 7)),
        ((6, 6), (4, 6)),
        ((2, 6), (4, 8)),
    ]


def test_parse(sample: T_PAIRS):
    lines = [
        "2-4,6-8",
        "2-3,4-5",
        "5-7,7-9",
        "2-8,3-7",
        "6-6,4-6",
        "2-6,4-8",
    ]
    assert parse(lines) == sample


def test_aoc04_part01(sample: T_PAIRS):
    assert part01(sample) == 2


def test_aoc04_part02(sample: T_PAIRS):
    assert part02(sample) == 4


if __name__ == "__main__":
    sys.exit(main())
