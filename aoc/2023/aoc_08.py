#!/usr/bin/env python3
import math
import sys
from dataclasses import dataclass
from itertools import cycle

import pytest


@dataclass
class Node:
    name: str
    left: str
    right: str


@dataclass
class Task:
    instructions: list[str]
    nodes: dict[str, Node]


def parse_lines(lines: list[str]) -> Task:
    instructions = list(lines[0])

    nodes: dict[str, Node] = {}
    for line in lines[2:]:
        fields = line.split()
        node = Node(name=fields[0], left=fields[2].strip(",("), right=fields[3].strip(",)"))
        nodes[node.name] = node

    return Task(instructions, nodes)


def part_01(task: Task) -> int:
    nodes = task.nodes
    current = nodes["AAA"]
    cnt = 0
    for instruction in cycle(task.instructions):
        if instruction == "L":
            current = nodes[current.left]
        elif instruction == "R":
            current = nodes[current.right]
        else:
            raise ValueError(instruction)

        cnt += 1
        if current.name == "ZZZ":
            return cnt

    return cnt


def part_02(task: Task) -> int:
    nodes = task.nodes

    current_nodes: list[Node] = []
    for node in nodes.values():
        if node.name.endswith("A"):
            current_nodes.append(node)

    repeats: list[int] = []

    for current_node in current_nodes:
        match_idx = 0
        for idx, instruction in enumerate(cycle(task.instructions)):
            if instruction == "L":
                current_node = nodes[current_node.left]
            elif instruction == "R":
                current_node = nodes[current_node.right]
            else:
                raise ValueError(instruction)

            if current_node.name.endswith("Z"):
                if match_idx > 0:
                    repeats.append(idx - match_idx)
                    break
                match_idx = idx

    return math.lcm(*repeats)


def main():
    with open("aoc_08.txt") as infile:
        lines = [line.strip() for line in infile]

    task = parse_lines(lines)
    print(part_01(task))
    print(part_02(task))


@pytest.fixture()
def task() -> Task:
    return Task(
        instructions=list("LLR"),
        nodes={
            "AAA": Node("AAA", "BBB", "BBB"),
            "BBB": Node("BBB", "AAA", "ZZZ"),
            "ZZZ": Node("ZZZ", "ZZZ", "ZZZ"),
        },
    )


def test_parse(task: Task):
    lines = [
        "LLR",
        "",
        "AAA = (BBB, BBB)",
        "BBB = (AAA, ZZZ)",
        "ZZZ = (ZZZ, ZZZ)",
    ]
    assert parse_lines(lines) == task


def test_part01(task: Task):
    assert part_01(task) == 6


if __name__ == "__main__":
    sys.exit(main())
