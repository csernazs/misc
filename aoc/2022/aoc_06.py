#!/usr/bin/env python3

import sys
import pytest


def find_uniqe_substr(input_str: str, length: int):
    for idx in range(len(input_str) - length):
        substr = input_str[idx : idx + length]
        if len(set(substr)) == length:
            return idx + length


def part01(input_str: str):
    return find_uniqe_substr(input_str, 4)


def part02(input_str: str):
    return find_uniqe_substr(input_str, 14)


def main():
    input_str = open("aoc_06.txt").read().strip()
    print(part01(input_str))
    print(part02(input_str))


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
    ],
)
def test_part01(input_str: str, expected: int):
    assert part01(input_str) == expected


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
    ],
)
def test_part02(input_str: str, expected: int):
    assert part02(input_str) == expected


if __name__ == "__main__":
    sys.exit(main())
