#!/usr/bin/env python3

import operator
from functools import reduce


def mul(numbers):
    return reduce(operator.mul, numbers)


def parse_file(path: str):
    with open(path) as infile:
        return list(map(int, infile))


def solve_1(numbers):
    numbers = sorted(numbers)
    count1 = 0
    count3 = 0
    old_n = 0
    numbers.append(numbers[-1] + 3)
    diffs = {}
    for n in numbers:
        diffs[n] = n - old_n
        if n - old_n == 1:
            count1 += 1
        if n - old_n == 3:
            count3 += 1
        old_n = n

    return count1 * count3


def solve_2(numbers):
    numbers = sorted(numbers)
    ranks = {0: 1}
    for n in numbers:
        rank = 0
        for t in (n - 1, n - 2, n - 3):
            if t in ranks:
                rank += ranks[t]
        ranks[n] = rank

    # print("ranks:")
    # for n, rank in sorted(ranks.items()):
    #     print(n, rank)

    return ranks[numbers[-1]]


def main():
    numbers = parse_file("aoc_10.txt")
    sol_1 = solve_1(numbers)
    print("solve_1", sol_1)

    sol_2 = solve_2(numbers)
    print("solve_2", sol_2)


if __name__ == "__main__":
    main()
