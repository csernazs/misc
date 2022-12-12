#!/usr/bin/env python3

import math
import operator
import re
import sys
from typing import Optional

import pytest


def try_int(val: str) -> int | str:
    try:
        return int(val)
    except ValueError:
        return val


class Operation:
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
    }

    def __init__(self, op_a: str, op: str, op_b: str):
        self.op_a = try_int(op_a)
        self.op_b = try_int(op_b)
        self.op = self.operators[op]

    @classmethod
    def parse(cls, text: str):
        # new = old * 13
        if m := re.match(r"(\w+) = (\w+) (.) (\w+)$", text):
            left, op_a, op, op_b = m.groups()
            assert left == "new"

        return cls(op_a, op, op_b)

    def evaluate(self, old: int) -> int:
        if self.op_a == "old":
            left = old
        elif isinstance(self.op_a, int):
            left = self.op_a

        if self.op_b == "old":
            right = old
        elif isinstance(self.op_b, int):
            right = self.op_b

        return self.op(left, right)

    def __call__(self, old: int) -> int:
        return self.evaluate(old)


class Monkey:
    def __init__(
        self,
        items: list[int],
        operation: Operation,
        divisible_by: int,
        true_case: int,
        false_case: int,
    ):
        self.items = items
        self.operation = operation
        self.divisible_by = divisible_by
        self.true_case = true_case
        self.false_case = false_case
        self.inspected_items = 0

    @classmethod
    def parse(cls, lines: list[str]):
        # "  Starting items: 79, 98",
        # "  Operation: new = old * 19",
        # "  Test: divisible by 23",
        # "    If true: throw to monkey 2",
        # "    If false: throw to monkey 3",

        items: Optional[list[int]] = None
        operation: Optional[Operation] = None
        divisible_by: Optional[int] = None
        true_case: Optional[int] = None
        false_case: Optional[int] = None

        for line in lines:
            line = line.strip()

            if line.startswith("Starting items:"):
                items = [int(x.strip(",")) for x in line.split()[2:]]
            elif line.startswith("Operation:"):
                operation = Operation.parse(line.split(maxsplit=1)[-1])
            elif line.startswith("Test: divisible by"):
                divisible_by = int(line.split()[-1])
            elif line.startswith("If true: throw to monkey"):
                true_case = int(line.split()[-1])
            elif line.startswith("If false: throw to monkey"):
                false_case = int(line.split()[-1])

        if (
            items is None
            or operation is None
            or divisible_by is None
            or true_case is None
            or false_case is None
        ):
            raise ValueError()

        return cls(items, operation, divisible_by, true_case, false_case)

    def copy(self) -> "Monkey":
        return Monkey(self.items.copy(), self.operation, self.divisible_by, self.true_case, self.false_case)


def parse(lines: list[str]) -> list[Monkey]:
    monkey_idx = 0
    monkey_lines: list[str] = []

    retval: list[Monkey] = []

    for line in lines:
        if line.startswith("Monkey "):
            monkey_id = int(line.split()[-1].strip(":"))
            assert monkey_id == monkey_idx
            monkey_idx += 1
            if monkey_lines:
                retval.append(Monkey.parse(monkey_lines))
                monkey_lines.clear()
        else:
            monkey_lines.append(line)

    if monkey_lines:
        retval.append(Monkey.parse(monkey_lines))

    return retval


def play_round(monkey_list: list[Monkey], divide_by: int):

    lcm = math.lcm(*[x.divisible_by for x in monkey_list])

    for idx, monkey in enumerate(monkey_list):
        for item in monkey.items:
            worry = monkey.operation(item)
            bored = worry // divide_by
            if bored % monkey.divisible_by == 0:
                monkey_list[monkey.true_case].items.append(bored)
            else:
                monkey_list[monkey.false_case].items.append(bored)
            monkey.inspected_items += 1
        monkey.items.clear()

    for monkey in monkey_list:
        monkey.items = [x % lcm for x in monkey.items]


def part01(monkey_list: list[Monkey]) -> int:
    for _ in range(20):
        play_round(monkey_list, 3)

    monkey_list.sort(key=lambda m: m.inspected_items, reverse=True)
    return monkey_list[0].inspected_items * monkey_list[1].inspected_items


def part02(monkey_list: list[Monkey]) -> int:
    for _ in range(10000):
        play_round(monkey_list, 1)

    monkey_list.sort(key=lambda m: m.inspected_items, reverse=True)
    return monkey_list[0].inspected_items * monkey_list[1].inspected_items


def main():
    with open("aoc_11.txt") as infile:
        lines = [x.rstrip() for x in infile]

    monkeys = parse(lines)

    print(part01([monkey.copy() for monkey in monkeys]))
    print(part02([monkey.copy() for monkey in monkeys]))


def test_operation():
    assert Operation.parse("new = old * 13")(122) == 122 * 13
    assert Operation.parse("new = 99 * 13")(122) == 99 * 13
    assert Operation.parse("new = 99 + 13")(122) == 99 + 13
    assert Operation.parse("new = 99 + old")(122) == 99 + 122
    assert Operation.parse("new = old + old")(122) == 122 + 122
    assert Operation.parse("new = old + old").evaluate(122) == 122 + 122


@pytest.fixture(scope="session")
def monkey_parsed() -> list[Monkey]:
    lines = [
        "Monkey 0:",
        "  Starting items: 79, 98",
        "  Operation: new = old * 19",
        "  Test: divisible by 23",
        "    If true: throw to monkey 2",
        "    If false: throw to monkey 3",
        "",
        "Monkey 1:",
        "  Starting items: 54, 65, 75, 74",
        "  Operation: new = old + 6",
        "  Test: divisible by 19",
        "    If true: throw to monkey 2",
        "    If false: throw to monkey 0",
        "",
        "Monkey 2:",
        "  Starting items: 79, 60, 97",
        "  Operation: new = old * old",
        "  Test: divisible by 13",
        "    If true: throw to monkey 1",
        "    If false: throw to monkey 3",
        "",
        "Monkey 3:",
        "  Starting items: 74",
        "  Operation: new = old + 3",
        "  Test: divisible by 17",
        "    If true: throw to monkey 0",
        "    If false: throw to monkey 1",
    ]

    return parse(lines)


@pytest.fixture
def monkey_list(monkey_parsed: list[Monkey]):
    return [monkey.copy() for monkey in monkey_parsed]


def test_parse():
    lines = [
        "Monkey 0:",
        "  Starting items: 79, 98",
        "  Operation: new = old * 19",
        "  Test: divisible by 23",
        "    If true: throw to monkey 2",
        "    If false: throw to monkey 3",
        "",
        "Monkey 1:",
        "  Starting items: 54, 65, 75, 74",
        "  Operation: new = old + 6",
        "  Test: divisible by 19",
        "    If true: throw to monkey 2",
        "    If false: throw to monkey 0",
        "",
        "Monkey 2:",
        "  Starting items: 79, 60, 97",
        "  Operation: new = old * old",
        "  Test: divisible by 13",
        "    If true: throw to monkey 1",
        "    If false: throw to monkey 3",
        "",
        "Monkey 3:",
        "  Starting items: 74",
        "  Operation: new = old + 3",
        "  Test: divisible by 17",
        "    If true: throw to monkey 0",
        "    If false: throw to monkey 1",
    ]

    monkeys = parse(lines)
    assert len(monkeys) == 4
    assert monkeys[0].items == [79, 98]
    assert monkeys[-1].items == [74]


def test_monkey_parse():
    lines = [
        "  Starting items: 79, 60, 97",
        "  Operation: new = old * old",
        "  Test: divisible by 13",
        "    If true: throw to monkey 1",
        "    If false: throw to monkey 3",
    ]
    m = Monkey.parse(lines)
    assert m.items == [79, 60, 97]
    assert m.operation.op_a == "old"
    assert m.operation.op_b == "old"
    assert m.operation.op is operator.mul
    assert m.true_case == 1
    assert m.false_case == 3


def test_round(monkey_list: list[Monkey]):
    play_round(monkey_list, 3)
    assert monkey_list[0].items == [20, 23, 27, 26]
    assert monkey_list[1].items == [2080, 25, 167, 207, 401, 1046]
    assert monkey_list[2].items == []
    assert monkey_list[3].items == []


def test_part01(monkey_list: list[Monkey]):
    assert part01(monkey_list) == 10605


def test_part02(monkey_list: list[Monkey]):
    assert part02(monkey_list) == 2713310158


if __name__ == "__main__":
    sys.exit(main())
