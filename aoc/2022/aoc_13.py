#!/usr/bin/env python3


from dataclasses import dataclass
from functools import cmp_to_key
import json
import sys

import pytest


@dataclass
class Pair:
    left: list[list | int]
    right: list[list | int]


def parse(lines: list[str]):
    left = None
    right = None
    retval: list[Pair] = []

    for line in lines:
        if not line:
            continue

        if left is None:
            left = json.loads(line)
        elif right is None:
            right = json.loads(line)
            retval.append(Pair(left, right))
            left = None
            right = None

    if left is not None and right is not None:
        retval.append(Pair(left, right))

    return retval


def all_int(l: list):
    for x in l:
        if not isinstance(x, int):
            return False
    return True


def cmp(left, right):
    if left < right:
        return -1
    elif left > right:
        return 1

    return 0


def is_int(x):
    return isinstance(x, int)


def is_list(x):
    return isinstance(x, list)


def compare(left, right):
    if is_int(left) and is_int(right):
        return cmp(left, right)
    elif is_list(left) and is_list(right):
        if all_int(left) and all_int(right):
            return cmp(left, right)

        for left_item, right_item in zip(left, right):
            if (retval := compare(left_item, right_item)) != 0:
                return retval

        return cmp(len(left), len(right))
    elif is_int(left) and is_list(right):
        return compare([left], right)
    elif is_list(left) and is_int(right):
        return compare(left, [right])
    else:
        raise ValueError(f"{left!r}  {right!r}")


def part01(pairs: list[Pair]):
    retval = 0
    for idx, pair in enumerate(pairs):
        if compare(pair.left, pair.right) == -1:
            retval += idx + 1
    return retval


def part02(pairs: list[Pair]):
    items: list[list | int] = []
    for pair in pairs:
        items.append(pair.left)
        items.append(pair.right)

    div1 = [[2]]
    div2 = [[6]]

    items.append(div1)
    items.append(div2)

    items.sort(key=cmp_to_key(compare))

    return (items.index(div1) + 1) * (items.index(div2) + 1)


def main():
    with open("aoc_13.txt") as infile:
        lines = [x.strip() for x in infile]

    pairs = parse(lines)
    print(part01(pairs))
    print(part02(pairs))


@pytest.fixture
def sample() -> list[Pair]:
    return [
        Pair(left=[1, 1, 3, 1, 1], right=[1, 1, 5, 1, 1]),
        Pair(left=[[1], [2, 3, 4]], right=[[1], 4]),
        Pair(left=[9], right=[[8, 7, 6]]),
        Pair(left=[[4, 4], 4, 4], right=[[4, 4], 4, 4, 4]),
        Pair(left=[7, 7, 7, 7], right=[7, 7, 7]),
        Pair(left=[], right=[3]),
        Pair(left=[[[]]], right=[[]]),
        Pair(left=[1, [2, [3, [4, [5, 6, 7]]]], 8, 9], right=[1, [2, [3, [4, [5, 6, 0]]]], 8, 9]),
    ]


def test_parse(sample: list[Pair]):
    lines = [
        "[1,1,3,1,1]",
        "[1,1,5,1,1]",
        "",
        "[[1],[2,3,4]]",
        "[[1],4]",
        "",
        "[9]",
        "[[8,7,6]]",
        "",
        "[[4,4],4,4]",
        "[[4,4],4,4,4]",
        "",
        "[7,7,7,7]",
        "[7,7,7]",
        "",
        "[]",
        "[3]",
        "",
        "[[[]]]",
        "[[]]",
        "",
        "[1,[2,[3,[4,[5,6,7]]]],8,9]",
        "[1,[2,[3,[4,[5,6,0]]]],8,9]",
    ]

    parsed = parse(lines)

    assert parsed == sample


def test_compare(sample: list[Pair]):
    assert compare(sample[0].left, sample[0].right) == -1
    assert compare(sample[1].left, sample[1].right) == -1
    assert compare(sample[2].left, sample[2].right) == 1
    assert compare(sample[3].left, sample[3].right) == -1
    assert compare(sample[4].left, sample[4].right) == 1
    assert compare(sample[5].left, sample[5].right) == -1
    assert compare(sample[6].left, sample[6].right) == 1
    assert compare(sample[7].left, sample[7].right) == 1

    assert compare(sample[0].left, sample[0].left) == 0
    assert compare(sample[1].left, sample[1].left) == 0
    assert compare(sample[2].left, sample[2].left) == 0
    assert compare(sample[3].left, sample[3].left) == 0
    assert compare(sample[4].left, sample[4].left) == 0
    assert compare(sample[5].left, sample[5].left) == 0
    assert compare(sample[6].left, sample[6].left) == 0
    assert compare(sample[7].left, sample[7].left) == 0

    assert compare(sample[0].right, sample[0].right) == 0
    assert compare(sample[1].right, sample[1].right) == 0
    assert compare(sample[2].right, sample[2].right) == 0
    assert compare(sample[3].right, sample[3].right) == 0
    assert compare(sample[4].right, sample[4].right) == 0
    assert compare(sample[5].right, sample[5].right) == 0
    assert compare(sample[6].right, sample[6].right) == 0
    assert compare(sample[7].right, sample[7].right) == 0


def test_part01(sample: list[Pair]):
    assert part01(sample) == 13


def test_part02(sample: list[Pair]):
    assert part02(sample) == 140


if __name__ == "__main__":
    sys.exit(main())
