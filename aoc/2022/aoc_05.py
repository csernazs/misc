#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from pprint import pprint

import pytest


@dataclass
class Move:
    source: int
    target: int
    amount: int


@dataclass
class Task:
    racks: list[list[str]]
    moves: list[Move]


def parse(lines: list[str]):
    for line in lines:
        if line.startswith(" 1 "):
            no_racks = int(line.split()[-1])
            break
    else:
        raise ValueError("Unable to determine the number of racks")

    racks: list[list[str]] = [[] for _ in range(no_racks)]
    for line in lines:
        if line.startswith(" 1 "):
            break

        for rack_idx in range(no_racks):
            try:
                container = line[1 + (rack_idx * 4)]
            except IndexError:
                break
            if container != " ":
                racks[rack_idx].append(container)

    moves = []
    for line in lines:
        if line.startswith("move "):
            fields = line.split()
            amount = int(fields[1])
            source = int(fields[3]) - 1
            target = int(fields[5]) - 1
            moves.append(Move(source, target, amount))

    return Task(racks=racks, moves=moves)


def run(task: Task, reverse: bool) -> list[str]:
    racks = [x.copy() for x in task.racks]
    for move in task.moves:
        if reverse:
            racks[move.target] = list(reversed(racks[move.source][: move.amount])) + racks[move.target]
        else:
            racks[move.target] = racks[move.source][: move.amount] + racks[move.target]

        racks[move.source][: move.amount] = []

    retval = [rack[0] for rack in racks]
    return retval


def part01(task: Task) -> str:
    return "".join(run(task, reverse=True))


def part02(task: Task) -> str:
    return "".join(run(task, reverse=False))


def main():
    with open("aoc_05.txt") as infile:
        lines = [x.rstrip() for x in infile]

    task = parse(lines)
    print(part01(task))
    print(part02(task))


@pytest.fixture
def task():
    return Task(
        racks=[["N", "Z"], ["D", "C", "M"], ["P"]],
        moves=[
            Move(source=1, target=0, amount=1),
            Move(source=0, target=2, amount=3),
            Move(source=1, target=0, amount=2),
            Move(source=0, target=1, amount=1),
        ],
    )


def test_parse(task: Task):
    lines = [
        "    [D]",
        "[N] [C]",
        "[Z] [M] [P]",
        " 1   2   3",
        "",
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]

    assert parse(lines) == task


def test_part01(task: Task):
    assert part01(task) == "CMZ"


def test_part02(task: Task):
    assert part02(task) == "MCD"


if __name__ == "__main__":
    sys.exit(main())
