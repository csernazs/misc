#!/usr/bin/env python3
# pylint: disable=all

import sys
from pprint import pprint
from typing import List, Optional

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


def solve(module_funs: List[int], module_pointers: List[Optional[int]]):



def main():
    no_cases = read_int(infile)

    for case_idx in range(no_cases):
        no_modules = read_int(infile)
        module_funs = read_ints(infile)
        assert len(module_funs) == no_modules

        module_pointers = read_ints(infile)
        assert len(module_pointers) == no_modules

        new_pointers = []
        for pointer in module_pointers:
            if pointer == 0:
                new_pointers.append(None)
            else:
                new_pointers.append(pointer-1)

        solution = solve(module_funs, new_pointers)
        outfile.write("Case #%d: %s\n" % (case_idx + 1, solution))


if __name__ == "__main__":
    main()
