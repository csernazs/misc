#!/usr/bin/env python3


import sys


def part01(lines: list[str]) -> int:
    retval: int = 0

    for line in lines:
        first: int | None = None
        second: int | None = None

        for char in line:
            if char in "0123456789":
                if first is None:
                    first = int(char)
                else:
                    second = int(char)
        assert first is not None

        if second is None:
            second = first

        number: int = first * 10 + second
        retval += number

    return retval


def part02(lines: list[str]) -> int:
    retval: int = 0

    choices: dict[str, int] = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    for line in lines:
        min_first_idx: int = 2**32
        max_last_idx: int = 0
        left: int = 0
        right: int = 0

        for choice, value in choices.items():
            first_idx = line.find(choice)
            if first_idx >= 0 and first_idx < min_first_idx:
                left = value
                min_first_idx = first_idx

            last_idx = line.rfind(choice)
            if last_idx > max_last_idx:
                right = value
                max_last_idx = last_idx

        if right == 0:
            right = left

        number = left * 10 + right

        retval += number

    return retval


def test_part01():
    lines = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]
    assert part01(lines) == 142


def test_part02():
    lines = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]
    assert part02(lines) == 281
    lines = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]
    assert part02(lines) == 142


def main():
    with open("aoc_01.txt") as infile:
        lines = [x.strip() for x in infile]

    print(part01(lines))
    print(part02(lines))


if __name__ == "__main__":
    sys.exit(main())
