#!/usr/bin/env python3
# pylint: disable=all

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
    return map(int, f.readline().rstrip().split(sep))


def read_lines(f, no_lines):
    retval = []
    for i in range(no_lines):
        retval.append(f.readline().rstrip())
    return retval


def solve(rows, cols):
    retval = []
    for rowidx in range(rows * 2):
        if rowidx == 0:
            retval.append(".." + "+-" * (cols - 1) + "+")
        elif rowidx == 1:
            retval.append(".." + "|." * (cols - 1) + "|")
        elif rowidx % 2 == 0:
            retval.append("+-" * cols + "+")
        else:
            retval.append("|." * cols + "|")

    retval.append("+-" * cols + "+")
    return "\n".join(retval)


def main():
    no_cases = read_int(infile)

    for case_idx in range(no_cases):
        rows, cols = read_ints(infile)
        solution = solve(rows, cols)
        outfile.write("Case #%d:\n%s\n" % (case_idx + 1, solution))


if __name__ == "__main__":
    main()
