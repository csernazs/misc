#!/usr/bin/env python3


from typing import List, no_type_check_decorator

import re
from enum import Enum, auto
from collections import defaultdict

from functools import reduce
import operator


def mul(numbers):
    return reduce(operator.mul, numbers)


def parse_file(path: str):
    with open(path) as infile:
        return [x.rstrip() for x in infile]


def evaluate_1(expr: str):
    retval = 0
    operands = [int(x) for x in re.split(r"[\+\*]", expr)]
    ops = re.findall(r"[\*\+]", expr)
    acc = operands.pop(0)
    for op, operand in zip(ops, operands):
        if op == "*":
            acc = acc * operand
        elif op == "+":
            acc = acc + operand

    return acc


def evaluate_2(expr: str):
    add_groups = expr.split("*")
    sum_results = []
    for group in add_groups:
        sum_results.append(sum(map(int, group.split("+"))))

    return mul(sum_results)


def reduce_bracket(line, eval_fn):
    line = list(line.replace(" ", ""))
    bracket_id = 0
    brackets = defaultdict(list)
    for idx, char in enumerate(line):
        if char == "(":
            bracket_id += 1
            brackets[bracket_id].append([idx, None])
        elif char == ")":
            brackets[bracket_id][-1][1] = idx
            bracket_id -= 1
    assert bracket_id == 0

    max_idx = max(brackets.keys())
    bracket_list = []
    for idx in range(1, max_idx + 1):
        bracket_list.append(brackets[idx])

    rng = bracket_list[-1][0]
    expr = "".join(line[rng[0] + 1 : rng[1]])
    result = eval_fn(expr)
    line[rng[0] : rng[1] + 1] = [str(result)]
    return "".join(line)


def solve_line(line: str, eval_fn):
    while "(" in line:
        line = reduce_bracket(line, eval_fn)
        # print(">>>", line)

    return eval_fn(line)


def solve_1(lines: List[str]):
    retval = 0
    for line in lines:
        retval += solve_line(line, evaluate_1)
    return retval


def solve_2(lines: List[str]):
    retval = 0
    for line in lines:
        retval += solve_line(line, evaluate_2)
    return retval


def test():
    assert evaluate_1("111+222") == 111 + 222
    assert evaluate_1("6*7*9") == 6 * 7 * 9
    assert evaluate_1("1+2+3") == 1 + 2 + 3
    assert evaluate_1("1+2+3*4*5") == (1 + 2 + 3) * 4 * 5
    assert evaluate_1("6*7+1+2+3*4*5") == ((6 * 7) + (1 + 2 + 3)) * 4 * 5

    assert evaluate_2("111+222") == 111 + 222
    assert evaluate_2("6*7*9") == 6 * 7 * 9
    assert evaluate_2("1+2+3") == 1 + 2 + 3
    assert evaluate_2("1+2+3*4*5") == (1 + 2 + 3) * 4 * 5
    assert evaluate_2("4*5+1+2+3") == (5 + 1 + 2 + 3) * 4
    assert evaluate_2("6*7+1+2+3*4*5") == 6 * (7 + 1 + 2 + 3) * 4 * 5


def main():
    lines = parse_file("aoc_18.txt")
    print("solve_1", solve_1(lines))
    print("solve_2", solve_2(lines))


if __name__ == "__main__":
    main()
