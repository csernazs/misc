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


def solve(word):
    retval = []
    cnt = 0
    for idx, char in enumerate(word):
        # print(char, cnt, retval)
        if idx == 0:
            retval.append(char)
        elif char == retval[-1]:
            retval.append(char)
            cnt += 1
        elif char > retval[-1]:
            retval.append(retval[-1] * (cnt + 1))
            retval.append(char)
            cnt = 0
        else:
            retval.append(char)
            cnt = 0

    return "".join(retval)


def main():
    no_cases = read_int(infile)

    for case_idx in range(no_cases):
        word = infile.readline().strip()
        solution = solve(word)
        outfile.write("Case #%d: %s\n" % (case_idx + 1, solution))


if __name__ == "__main__":
    main()
