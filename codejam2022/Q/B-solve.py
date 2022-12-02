#!/usr/bin/env python3
# pylint: disable=all

from pprint import pprint
import sys
from typing import List

try:
    infile = open(sys.argv[1], "r")
except IndexError:
    infile = sys.stdin

try:
    outfile = open(sys.argv[2], "w")
except IndexError:
    outfile = sys.stdout


def read_int(f):
    return int(f.readline())


def read_ints(f, sep=" "):
    return list(map(int, f.readline().rstrip().split(sep)))


def read_lines(f, no_lines):
    retval = []
    for i in range(no_lines):
        retval.append(f.readline().rstrip())
    return retval


def solve(printers: List[List[int]]):
    colors = [[], [], [], []]
    for printer in printers:
        for idx in range(4):
            colors[idx].append(printer[idx])

    min_colors = [min(x) for x in colors]
    # print("min_colors", min_colors, sum(min_colors))
    if sum(min_colors) < 1_000_000:
        return "IMPOSSIBLE"

    remaining = 1_000_000
    retval = []
    for color in min_colors:
        color_to_add = min(remaining, color)
        retval.append(color_to_add)
        remaining -= color_to_add

    return " ".join(map(str, retval))


def main():
    no_cases = read_int(infile)

    for case_idx in range(no_cases):
        printers = []
        for _ in range(3):
            colors = read_ints(infile)
            assert len(colors) == 4
            printers.append(colors)

        # pprint(printers)
        solution = solve(printers)
        outfile.write("Case #%d: %s\n" % (case_idx + 1, solution))


if __name__ == "__main__":
    main()
