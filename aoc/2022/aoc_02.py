#!/usr/bin/env python3

import sys


def calculate_score(a, b):
    # A for Rock, B for Paper, and C for Scissors
    # X for Rock, Y for Paper, and Z for Scissors

    # 1 for Rock, 2 for Paper, and 3 for Scissors
    weights = {"X": 1, "Y": 2, "Z": 3}
    scores = {
        ("A", "X"): 3,
        ("A", "Y"): 6,
        ("A", "Z"): 0,
        ("B", "X"): 0,
        ("B", "Y"): 3,
        ("B", "Z"): 6,
        ("C", "X"): 6,
        ("C", "Y"): 0,
        ("C", "Z"): 3,
    }

    return scores[(a, b)] + weights[b]


def map_choice(a, b):
    # A for Rock, B for Paper, and C for Scissors
    # X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win

    # X for Rock, Y for Paper, and Z for Scissors

    scores = {
        ("A", "X"): "Z",
        ("A", "Y"): "X",
        ("A", "Z"): "Y",
        ("B", "X"): "X",
        ("B", "Y"): "Y",
        ("B", "Z"): "Z",
        ("C", "X"): "Y",
        ("C", "Y"): "Z",
        ("C", "Z"): "X",
    }

    return scores[(a, b)]


def part01(strategy: list[tuple[str, str]]):
    return sum([calculate_score(a, b) for a, b in strategy])


def part02(strategy: list[tuple[str, str]]):
    return sum([calculate_score(a, map_choice(a, b)) for a, b in strategy])


def main():
    strategy = []
    with open("aoc_02.txt") as infile:
        for line in infile:
            line = line.strip()
            if line:
                if len(line.split()) != 2:
                    raise ValueError(line)
                strategy.append(tuple(line.split()))

    print(part01(strategy))
    print(part02(strategy))


def test_aoc02_part01():
    strategy = [
        ("A", "Y"),
        ("B", "X"),
        ("C", "Z"),
    ]
    assert part01(strategy) == 15


def test_aoc02_part02():
    strategy = [
        ("A", "Y"),
        ("B", "X"),
        ("C", "Z"),
    ]
    assert part02(strategy) == 12


if __name__ == "__main__":
    sys.exit(main())
