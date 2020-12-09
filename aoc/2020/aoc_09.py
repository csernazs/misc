#!/usr/bin/env python3

import itertools
from typing import List


def parse_file(path: str):
    with open(path) as infile:
        return list(map(int, infile))


def is_valid(number, numbers):
    for a, b in itertools.combinations(numbers, r=2):
        if a + b == number:
            return True

    return False


def solve_1(numbers, past_range=25):
    for idx in range(past_range, len(numbers)):
        number = numbers[idx]
        past = numbers[idx - past_range : idx]
        if not is_valid(number, past):
            return idx, number


def solve_2(numbers: List[int]):
    number = numbers.pop(-1)
    bottom = 0
    top = 2
    s = sum(numbers[:3])
    while True:
        print(s)
        if s == number:
            sol_range = numbers[bottom : top + 1]
            assert sum(sol_range) == number
            return min(sol_range) + max(sol_range)
        if s < number:
            top += 1
            s = s + numbers[top]
        elif s > number:
            s = s - numbers[bottom]
            bottom += 1


def main():
    numbers = parse_file("aoc_09.txt")
    invalid_idx, invalid = solve_1(numbers)
    print("solve_1", invalid)
    print("solve_2", solve_2(numbers[: invalid_idx + 1]))


if __name__ == "__main__":
    main()
