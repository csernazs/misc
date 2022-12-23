#!/usr/bin/env python3
from functools import cache
import sys
from typing import Optional

import pytest

EDICT = dict[str, int | tuple[str, str, str]]


def parse(lines: list[str]) -> EDICT:
    retval: EDICT = {}
    for line in lines:
        left, right = line.split(": ")
        try:
            right_int = int(right)
            retval[left] = right_int
        except ValueError:
            right_fields = right.split()
            retval[left] = (right_fields[0], right_fields[1], right_fields[2])

    return retval


def do_op(left: int, op: str, right: int) -> int:
    if op == "+":
        result = left + right
    elif op == "*":
        result = left * right
    elif op == "/":
        result = left // right
    elif op == "-":
        result = left - right
    elif op == "=":
        result = int(left == right)
    else:
        raise ValueError(op)
    return result


class Symbol:
    def __init__(self):
        self.value: Optional[int] = None
        self.op = ""

    def __add__(self, other: int):
        if self.value is None:
            self.value = other
            self.op = "+"
        else:
            self.value += other
        return self

    def __radd__(self, other: int):
        if self.value is None:
            self.value = other
            self.op = "+"
        else:
            self.value += other
        return self

    def __sub__(self, other: int):
        if self.value is None:
            self.value = other
            self.op = "-"
        else:
            self.value -= other
        return self

    def __rsub__(self, other: int):
        if self.value is None:
            self.value = other
            self.op = "-"
        else:
            self.value -= other
        return self

    def __mul__(self, other: int):
        if self.value is None:
            self.value = other
            self.op = "*"
        else:
            self.value *= other
        return self

    def __rmul__(self, other: int):
        if self.value is None:
            self.value = other
            self.op = "*"
        else:
            self.value *= other
        return self

    def __floordiv__(self, other: int):
        if self.value is None:
            self.value = other
            self.op = "/"
        else:
            self.value //= other
        return self

    def __eq__(self, other):
        assert self.value is not None
        return True


def get_value(name: str, exprs: EDICT) -> int:
    value = exprs[name]

    if isinstance(value, tuple):
        left, op, right = value
        left_value = get_value(left, exprs)
        right_value = get_value(right, exprs)
        return do_op(left_value, op, right_value)
    else:
        return value


def part01(exprs: EDICT):
    return get_value("root", exprs)


def part02(exprs: EDICT):
    exprs = exprs.copy()
    root = exprs["root"]
    assert isinstance(exprs["humn"], int)
    assert isinstance(root, tuple)

    dvpt = get_value("dvpt", exprs)
    print("dvpt", dvpt)

    ljgn = get_value("ljgn", exprs)
    print("ljgn", ljgn)

    # result = ljgn * (humn - dvpt)

    # result / ljgn = humn - dvpt

    # ptdq: humn - dvpt
    # lgvd: ljgn * ptdq

    # lgvd = ljgn * (humn - dvpt)

    result = 150
    humn = result // ljgn + dvpt

    print("humn", humn)

    exprs["humn"] = humn

    print("pppw", get_value("pppw", exprs))

    print("sjmn", get_value("sjmn", exprs))

    return humn


def main():
    with open("aoc_21.txt") as infile:
        lines = [x.strip() for x in infile]

    parsed = parse(lines)
    print(part01(parsed))
    print(part02(parsed))


@pytest.fixture
def sample() -> EDICT:
    return {
        "root": ("pppw", "+", "sjmn"),
        "dbpl": 5,
        "cczh": ("sllz", "+", "lgvd"),
        "zczc": 2,
        "ptdq": ("humn", "-", "dvpt"),
        "dvpt": 3,
        "lfqf": 4,
        "humn": 5,
        "ljgn": 2,
        "sjmn": ("drzm", "*", "dbpl"),
        "sllz": 4,
        "pppw": ("cczh", "/", "lfqf"),
        "lgvd": ("ljgn", "*", "ptdq"),
        "drzm": ("hmdt", "-", "zczc"),
        "hmdt": 32,
    }


def test_parse():
    lines = [
        "root: pppw + sjmn",
        "dbpl: 5",
        "cczh: sllz + lgvd",
        "zczc: 2",
        "ptdq: humn - dvpt",
        "dvpt: 3",
        "lfqf: 4",
        "humn: 5",
        "ljgn: 2",
        "sjmn: drzm * dbpl",
        "sllz: 4",
        "pppw: cczh / lfqf",
        "lgvd: ljgn * ptdq",
        "drzm: hmdt - zczc",
        "hmdt: 32",
    ]
    assert parse(lines) == {
        "root": ("pppw", "+", "sjmn"),
        "dbpl": 5,
        "cczh": ("sllz", "+", "lgvd"),
        "zczc": 2,
        "ptdq": ("humn", "-", "dvpt"),
        "dvpt": 3,
        "lfqf": 4,
        "humn": 5,
        "ljgn": 2,
        "sjmn": ("drzm", "*", "dbpl"),
        "sllz": 4,
        "pppw": ("cczh", "/", "lfqf"),
        "lgvd": ("ljgn", "*", "ptdq"),
        "drzm": ("hmdt", "-", "zczc"),
        "hmdt": 32,
    }


def test_part01(sample: EDICT):
    assert part01(sample) == 152


def test_part02(sample: EDICT):
    assert part02(sample) == 301


if __name__ == "__main__":
    sys.exit(main())
