#!/usr/bin/env python3

import sys
from textwrap import dedent
from typing import Iterable, Optional

import pytest

T_PAIRS = list[tuple[tuple[int, int], tuple[int, int]]]


class RangeSet:
    def __init__(self, lower: int, higher: int):
        if lower > higher:
            raise ValueError("lower must not be greater than higher")
        self.lower = lower
        self.higher = higher

    def __contains__(self, element: int) -> bool:
        return element >= self.lower and element <= self.higher

    def issubset(self, other: "RangeSet") -> bool:
        if not isinstance(other, RangeSet):
            raise TypeError("issubset argument must be a RangeSet")

        return self.lower >= other.lower and self.higher <= other.higher

    def intersection(self, other: "RangeSet") -> Optional["RangeSet"]:
        if other.lower > self.lower:
            new_lower = other.lower
        else:
            new_lower = self.lower

        if other.higher < self.higher:
            new_higher = other.higher
        else:
            new_higher = self.higher

        if new_lower <= new_higher:
            return RangeSet(new_lower, new_higher)

        return None

    def __len__(self) -> int:
        return self.higher - self.lower + 1

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RangeSet):
            return NotImplemented

        return self.lower == other.lower and self.higher == other.higher

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} lower={self.lower} higher={self.higher}>"


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


def iter_sets(pairs_list: T_PAIRS) -> Iterable[tuple[RangeSet, RangeSet]]:
    for pairs in pairs_list:
        left_pair = pairs[0]
        right_pair = pairs[1]
        left_set = RangeSet(left_pair[0], left_pair[1])
        right_set = RangeSet(right_pair[0], right_pair[1])
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


def test_rangeset():
    rs = RangeSet(1, 10)
    assert rs.lower == 1
    assert rs.higher == 10
    assert len(rs) == 10
    assert str(rs) == "<RangeSet lower=1 higher=10>"
    assert 5 in rs
    assert 1 in rs
    assert 10 in rs
    assert 0 not in rs
    assert 11 not in rs

    assert len(RangeSet(1, 1)) == 1


def test_rangeset_issubset():
    rs = RangeSet(1, 10)
    assert rs.issubset(RangeSet(1, 9)) is False
    assert rs.issubset(RangeSet(5, 10)) is False
    assert rs.issubset(rs) is True
    assert rs.issubset(RangeSet(1, 11)) is True
    assert rs.issubset(RangeSet(0, 10)) is True


def test_rangeset_intersection():
    rs = RangeSet(1, 10)

    assert rs.intersection(RangeSet(1, 5)) == RangeSet(1, 5)
    assert rs.intersection(RangeSet(4, 5)) == RangeSet(4, 5)
    assert rs.intersection(rs) == rs
    assert rs.intersection(RangeSet(20, 25)) is None
    assert rs.intersection(RangeSet(5, 5)) == RangeSet(5, 5)
    assert rs.intersection(RangeSet(5, 20)) == RangeSet(5, 10)
    assert rs.intersection(RangeSet(-10, 5)) == RangeSet(1, 5)


if __name__ == "__main__":
    sys.exit(main())
