#!/usr/bin/env python3

import operator
from functools import reduce


def mul(numbers):
    return reduce(operator.mul, numbers)


def parse_file(path: str):
    retval = []
    with open(path) as infile:
        for line in infile:
            retval.append(line.rstrip())

    return retval


class Area:
    def __init__(self, data):
        self.data = data
        self.width = len(self.data[0])
        self.height = len(self.data)

    def get(self, row, column):
        column = column % self.width
        return self.data[row][column]

    @classmethod
    def parse(cls, path):
        return cls(parse_file(path))

    def solve_pattern(self, right, down):
        colidx = 0
        rowidx = 0
        cnt = 0

        while rowidx < self.height:
            if self.get(rowidx, colidx) == "#":
                cnt += 1
            rowidx += down
            colidx += right

        return cnt


def task_1(area: Area):
    print(area.solve_pattern(right=3, down=1))


def task_2(area: Area):

    # Right 1, down 1.
    # Right 3, down 1. (This is the slope you already checked.)
    # Right 5, down 1.
    # Right 7, down 1.
    # Right 1, down 2.

    numbers = (
        area.solve_pattern(right=1, down=1),
        area.solve_pattern(right=3, down=1),
        area.solve_pattern(right=5, down=1),
        area.solve_pattern(right=7, down=1),
        area.solve_pattern(right=1, down=2),
    )
    print(mul(numbers))


def main():
    area = Area.parse("aoc_03.txt")
    task_1(area)
    task_2(area)


if __name__ == "__main__":
    main()
