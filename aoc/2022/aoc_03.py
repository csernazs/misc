#!/usr/bin/env python3

import sys
from string import ascii_letters as letters
from typing import Iterable, Optional, Sequence


def find_common_in_groups(groups: Sequence[Iterable]) -> set:
    assert len(groups) > 1

    groups_set = [set(x) for x in groups]

    common: Optional[set] = None
    for group in groups_set:
        if common is None:
            common = group
        else:
            common = common.intersection(group)

    assert common is not None

    return common


def get_common_item(backpack: str):
    left = backpack[: len(backpack) // 2]
    right = backpack[len(backpack) // 2 :]
    assert len(left) == len(right) and len(left) + len(right) == len(backpack)

    common = find_common_in_groups([set(left), set(right)])
    assert len(common) == 1
    return common.pop()


def get_priority(item: str) -> int:
    assert len(item) == 1
    return letters.index(item) + 1


def part01(backpacks: list[str]):
    retval = 0
    for backpack in backpacks:
        common_item = get_common_item(backpack)
        retval += get_priority(common_item)

    return retval


def part02(elves: list[str]):
    retval = 0
    groups = [elves[idx : idx + 3] for idx in range(0, len(elves), 3)]
    for group in groups:
        common = find_common_in_groups(group)
        assert len(common) == 1
        retval += get_priority(common.pop())
    return retval


def main():
    with open("aoc_03.txt") as infile:
        lines = [x.strip() for x in infile]

    print(part01(lines))
    print(part02(lines))


def test_aoc03_part01():
    sample = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    assert part01(sample) == 157


def test_aoc03_part02():
    sample = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    assert part02(sample) == 70


if __name__ == "__main__":
    sys.exit(main())
