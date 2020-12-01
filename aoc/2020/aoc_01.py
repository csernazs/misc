#!/usr/bin/env python3

from itertools import product
from functools import reduce
import operator


def mul(numbers):
    return reduce(operator.mul, numbers)


def main():
    numbers = []
    for line in open("aoc_01.txt"):
        numbers.append(int(line))

    for nums in product(numbers, repeat=2):
        if sum(nums) == 2020:
            print(mul(nums))
            break

    for nums in product(numbers, repeat=3):
        if sum(nums) == 2020:
            print(mul(nums))
            break


if __name__ == "__main__":
    main()
