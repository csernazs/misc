#!/usr/bin/env python3

import sys
from icecream import ic

opening = "([{<"
pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def parse_line(line):
    stack = []
    for char in line:
        if char in opening:
            stack.append(char)
            ic(stack)
        else:
            last = stack.pop()
            if char != pairs[last]:
                return False

    if not stack:
        return True
    return False


def solve_1(lines):
    for line in lines:
        if not parse_line(line):
            print("invalid", line)
        else:
            print("valid", line)


def main():
    with open("aoc_10.txt") as infile:
        lines = [x.strip() for x in infile]
    solve_1(lines)


if __name__ == "__main__":
    sys.exit(main())
