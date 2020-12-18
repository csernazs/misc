#!/usr/bin/env python3


from typing import Any, List

import re
from collections import defaultdict

from functools import reduce
import operator

NOP = None


def mul(numbers):
    return reduce(operator.mul, numbers)


def parse_file(path: str):
    with open(path) as infile:
        return [x.rstrip() for x in infile]


def evaluate_1(expr: List[Any]):
    expr = [x for x in expr if x is not None]
    acc = expr.pop(0)
    op = None
    for part in expr:
        if isinstance(part, int):
            if op == "+":
                acc = acc + part
            elif op == "*":
                acc = acc * part
            else:
                raise ValueError("Invalid op: {!r}".format(op))
        elif part in "*+":
            op = part

    return acc


def split_list(items: List[Any], sep: Any):
    retval = []
    group = []
    for item in items:
        if item == sep:
            retval.append(group)
            group = []
        else:
            group.append(item)
    retval.append(group)
    return retval


def evaluate_2(expr: List[Any]):
    add_groups = split_list(expr, "*")
    sum_results = []
    for group in add_groups:
        sum_results.append(sum([x for x in group if isinstance(x, int)]))

    return mul(sum_results)


def reduce_bracket(tokens, eval_fn):
    bracket_id = 0
    brackets = defaultdict(list)
    for idx, token in enumerate(tokens):
        if token == "(":
            bracket_id += 1
            brackets[bracket_id].append([idx, None])
        elif token == ")":
            brackets[bracket_id][-1][1] = idx
            bracket_id -= 1
    assert bracket_id == 0

    max_idx = max(brackets.keys())
    bracket_list = []
    for idx in range(1, max_idx + 1):
        bracket_list.append(brackets[idx])

    for bracket in reversed(bracket_list):
        for rng in bracket:
            result = eval_fn(tokens[rng[0] + 1 : rng[1]])
            old_length = len(tokens)
            tokens[rng[0] : rng[1] + 1] = [NOP] * (rng[1] - rng[0]) + [result]
            assert len(tokens) == old_length


def solve_line(line: str, eval_fn):
    tokens = tokenize(line)
    if "(" in tokens:
        reduce_bracket(tokens, eval_fn)

    return eval_fn(tokens)


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


def tokenize(line: str):
    line = line.replace(" ", "")
    tokens = re.findall(r"(\d+|\(|\)|\+|\*)", line)
    retval = []
    for t in tokens:
        if t in "()+*":
            retval.append(t)
        else:
            retval.append(int(t))
    return retval


def test_evaluate_1():
    assert evaluate_1([111, "+", 222]) == 111 + 222
    assert evaluate_1([6, "*", 7, "*", 9]) == 6 * 7 * 9
    assert evaluate_1([1, "+", 2, "+", 3]) == 1 + 2 + 3
    assert evaluate_1([1, "+", 2, "+", 3, "*", 4, "*", 5]) == (1 + 2 + 3) * 4 * 5
    assert evaluate_1([6, "*", 7, "+", 1, "+", 2, "+", 3, "*", 4, "*", 5]) == ((6 * 7) + (1 + 2 + 3)) * 4 * 5


def test_evaluate_2():
    assert evaluate_1([111, "+", 222]) == 111 + 222
    assert evaluate_1([6, "*", 7, "*", 9]) == 6 * 7 * 9
    assert evaluate_1([1, "+", 2, "+", 3]) == 1 + 2 + 3
    assert evaluate_1([1, "+", 2, "+", 3, "*", 4, "*", 5]) == (1 + 2 + 3) * 4 * 5

    assert evaluate_2([4, "*", 5, "+", 1, "+", 2, "+", 3]) == (5 + 1 + 2 + 3) * 4
    assert evaluate_2([6, "*", 7, "+", 1, "+", 2, "+", 3, "*", 4, "*", 5]) == 6 * (7 + 1 + 2 + 3) * 4 * 5


def test_list_split():
    assert split_list([6, "*", 7, "+", 1, "+", 2, "+", 3, "*", 4, "*", 5], "+") == [
        [6, "*", 7],
        [1],
        [2],
        [3, "*", 4, "*", 5],
    ]


def test_tokenize():
    assert tokenize("((2 + 4 * 9) * (6 + 9 * 876 + 6) + 6) + 212 + 432 * 2") == [
        "(",
        "(",
        2,
        "+",
        4,
        "*",
        9,
        ")",
        "*",
        "(",
        6,
        "+",
        9,
        "*",
        876,
        "+",
        6,
        ")",
        "+",
        6,
        ")",
        "+",
        212,
        "+",
        432,
        "*",
        2,
    ]


def test_solve_1():
    lines = parse_file("aoc_18.txt")
    assert solve_1(lines) == 11297104473091


def test_solve_2():
    lines = parse_file("aoc_18.txt")
    assert solve_2(lines) == 185348874183674


def main():
    lines = parse_file("aoc_18.txt")
    print("solve_1", solve_1(lines))
    print("solve_2", solve_2(lines))


if __name__ == "__main__":
    main()
