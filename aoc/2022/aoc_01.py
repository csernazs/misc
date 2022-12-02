#!/usr/bin/env python3

from collections import defaultdict
import sys

from icecream import ic


# def part01(groups: list[list[int]]):
#     elves = defaultdict(int)
#     for group in groups:
#         for idx, item in enumerate(group):
#             elves[idx] += item

#     max_elf = max(elves.items(), key=lambda kv: kv[1])
#     print(max_elf)


def part01(groups: list[list[int]]):
    elves = []
    for group in groups:
        elves.append(sum(group))

    print(max(elves))


def part02(groups: list[list[int]]):
    elves = []
    for group in groups:
        elves.append(sum(group))

    elves.sort(reverse=True)
    print(sum(elves[:3]))


def main():
    groups: list[list[int]] = []
    group = []
    with open("aoc_01.txt") as infile:
        for line in infile:
            line = line.strip()
            if line:
                group.append(int(line))
            else:
                groups.append(group)
                group = []

    if group:
        groups.append(group)

    part01(groups)
    part02(groups)


if __name__ == "__main__":
    sys.exit(main())
