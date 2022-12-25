#!/usr/bin/env python3

import sys

import pytest


def snafu2int(snafu: str) -> int:
    assert len(snafu) > 0

    symbol_to_int: dict[str, int] = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2,
    }

    parts: list[int] = [symbol_to_int[x] for x in snafu]

    retval = 0

    for idx, part in enumerate(reversed(parts)):
        retval += (5**idx) * part

    return retval


def to_base5(x: int) -> list[int]:
    assert x >= 0
    parts: list[int] = []
    if x == 0:
        return [0]

    while x > 0:
        x, mod = divmod(x, 5)
        parts.append(mod)

    parts.reverse()
    return parts


def int2snafu_list(x: int) -> list[int]:
    base5 = to_base5(x)
    base5.reverse()
    new_digits = []

    addition = 0
    for digit in base5:
        d = digit + addition
        if d > 2:
            d = d - 5
            addition = 1
            new_digits.append(d)
        else:
            addition = 0
            new_digits.append(d)

    if addition > 0:
        new_digits.append(addition)

    new_digits.reverse()
    return new_digits


def int2snafu(x: int) -> str:
    to_str = {
        -2: "=",
        -1: "-",
        0: "0",
        1: "1",
        2: "2",
    }

    retval = ""
    for d in int2snafu_list(x):
        retval += to_str[d]

    return retval


def part01(lines: list[str]) -> str:
    s = 0
    for line in lines:
        s += snafu2int(line)

    return int2snafu(s)


def main():
    with open("aoc_25.txt") as infile:
        lines = [x.strip() for x in infile]

    print(part01(lines))


snafu_examples = (
    ("0", 0),
    ("1", 1),
    ("2", 2),
    ("1=", 3),
    ("1-", 4),
    ("10", 5),
    ("11", 6),
    ("12", 7),
    ("2=", 8),
    ("2-", 9),
    ("20", 10),
    ("21", 11),
    ("22", 12),
    ("1==", 13),
    ("1=-", 14),
    ("1=0", 15),
    ("1=1", 16),
    ("1=2", 17),
    ("1-=", 18),
    ("1--", 19),
    ("1-0", 20),
    ("1-1", 21),
    ("1-2", 22),
    ("1=-0-2", 1747),
    ("12111", 906),
    ("2=0=", 198),
    ("2=01", 201),
    ("111", 31),
    ("20012", 1257),
    ("112", 32),
    ("1=-1=", 353),
    ("1-12", 107),
    ("122", 37),
    ("1=11-2", 2022),
    ("1-0---0", 12345),
    ("1121-1110-1=0", 314159265),
)


@pytest.mark.parametrize("snafu,integer", snafu_examples)
def test_snafu2int(snafu, integer):
    assert snafu2int(snafu) == integer


@pytest.mark.parametrize("snafu,integer", snafu_examples)
def test_int2snafu(snafu, integer):
    assert int2snafu(integer) == snafu


if __name__ == "__main__":
    sys.exit(main())
