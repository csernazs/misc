#!/usr/bin/python3

# pylint: disable=all

import sys

infile = sys.stdin
outfile = sys.stdout


def read_int():
    return int(infile.readline())


def read_ints(sep=" "):
    return list(map(int, infile.readline().rstrip().split(sep)))


def find_issue(list_in):
    curr = -1
    for idx, item in enumerate(list_in):
        if item >= curr:
            curr = item
        else:
            return idx - 1


def is_sorted(list_in):
    return find_issue(list_in) is None


def sort(list_in):
    done = False

    while not done:
        done = True
        for i in range(0, len(list_in) - 2):
            if list_in[i] > list_in[i + 2]:
                list_in[i], list_in[i + 2] = list_in[i + 2], list_in[i]
                done = False


def solve(values):
    if is_sorted(values):
        return "OK"

    sort(values)
    idx = find_issue(values)
    if idx is None:
        return "OK"
    else:
        return idx


def main():
    for case_idx in range(read_int()):
        no_values = read_int()
        values = read_ints()
        sol = solve(values)
        print("Case #{}: {}".format(case_idx + 1, sol))


if __name__ == '__main__':
    main()
