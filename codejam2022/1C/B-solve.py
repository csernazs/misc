#!/usr/bin/env python3
# pylint: disable=all

from collections import deque
import itertools
from typing import List
import sys

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



def solve(numbers: List[int]):
    left = sum(numbers)
    right = sum([x**2 for x in numbers])

    if left == 0:
        if sum(numbers + [1]) ** 2 == sum([x**2 for x in numbers + [1]]):
            return "1"
        else:
            return "IMPOSSIBLE"
    sol = (right - left ** 2) / (2 * left)
    if int(sol) == sol:
        return int(sol)
    else:
        return "IMPOSSIBLE"

def main():
    no_cases = read_int(infile)

    for case_idx in range(no_cases):
        no_numbers, k = read_ints(infile)
        numbers = read_ints(infile)
        assert len(numbers) == no_numbers

        solution = solve(numbers)
        outfile.write("Case #%d: %s\n" % (case_idx + 1, solution))

if __name__ == "__main__":
    main()
