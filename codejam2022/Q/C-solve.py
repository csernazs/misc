#!/usr/bin/env python3
# pylint: disable=all

import sys
from pprint import pprint
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


def longest_run(dices, start=1):
    current = start
    for dice in dices:
        if dice >= current:
            current += 1
        else:
            continue

    return current - start


def solve(dices: List[int]):
    dices_sorted = sorted(dices)
    retval = longest_run(dices_sorted, 1)
    return retval


def main():
    no_cases = read_int(infile)

    for case_idx in range(no_cases):
        no_dices = read_int(infile)
        dices = read_ints(infile)
        assert len(dices) == no_dices

        solution = solve(dices)
        outfile.write("Case #%d: %s\n" % (case_idx + 1, solution))


if __name__ == "__main__":
    main()
