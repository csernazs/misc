#!/usr/bin/env python3

import math
import sys
from typing import Optional

import pytest
from collections import deque


class Valve:
    def __init__(self, name: str, children: list["Valve"], flow_rate: Optional[int]):
        self.name = name
        self._flow_rate = flow_rate
        self.children = children

    @property
    def flow_rate(self) -> int:
        assert self._flow_rate is not None
        return self._flow_rate

    @flow_rate.setter
    def flow_rate(self, value: int):
        self._flow_rate = value

    @property
    def child_names(self):
        return list([x.name for x in self.children])

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} flow_rate={self.flow_rate} children={self.child_names}>"


def parse(lines: list[str]) -> dict[str, Valve]:

    valves: dict[str, Valve] = {}

    for line in lines:
        fields = line.split()
        name = fields[1]
        rate = int(fields[4].split("=")[1].rstrip(";"))
        child_names = [x.rstrip(",") for x in fields[9:]]

        ## print(name, rate, child_names)
        for child_name in child_names:
            if not child_name in valves:
                valves[child_name] = Valve(child_name, [], None)

        child_nodes = [valves[c] for c in child_names]
        if name not in valves:
            valves[name] = Valve(name, child_nodes, rate)
        else:
            valves[name].children = child_nodes
            valves[name].flow_rate = rate

    return valves


def compute_distances(start: Valve) -> dict[str, int]:
    distances: dict[str, int] = {start.name: 0}

    queue = deque([start])

    while queue:
        valve = queue.popleft()
        distance = distances[valve.name]
        new_distance = distance + 1
        for children in valve.children:
            if new_distance < distances.get(children.name, math.inf):
                distances[children.name] = new_distance
                queue.append(children)

    return distances


class Solver:
    def __init__(self, valves: dict[str, Valve]):
        self.valves = valves
        self.valves_with_flow_rate = [x for x in valves.values() if x.flow_rate > 0]

        self.distances: dict[str, dict[str, int]] = {}
        for valve in self.valves_with_flow_rate:
            self.distances[valve.name] = compute_distances(valve)

    def solve_part01(self, cv: Valve) -> int:
        self.distances[cv.name] = compute_distances(cv)
        return self.solve_part01_rec(cv, open_valves=set(), remaining_time=30, total_gain=0)

    def solve_part01_rec(self, cv: Valve, open_valves: set[str], remaining_time: int, total_gain: int) -> int:
        ## print("current", cv.name)
        possible_distances = self.distances[cv.name]
        possible_valves = [
            (self.valves[vname], distance)
            for vname, distance in possible_distances.items()
            if vname != cv.name and self.valves[vname].flow_rate > 0 and vname not in open_valves
        ]

        ## print("possible_valves", possible_valves)
        if not possible_valves:
            return total_gain

        gains = []
        for valve, distance in possible_valves:
            new_open_valves = open_valves.union(
                {
                    valve.name,
                }
            )
            new_remaining_time = remaining_time - distance - 1
            if new_remaining_time < 0:
                continue

            gain = self.solve_part01_rec(
                valve,
                new_open_valves,
                new_remaining_time,
                total_gain=total_gain + valve.flow_rate * (new_remaining_time),
            )
            gains.append(gain)

        if not gains:
            return total_gain
        return max(gains)


def part01(valves: dict[str, Valve]):
    solver = Solver(valves)
    return solver.solve_part01(valves["AA"])


def main():
    with open("aoc_16.txt") as infile:
        lines = [x.strip() for x in infile]

    valves = parse(lines)
    print(part01(valves))


@pytest.fixture
def sample() -> dict[str, Valve]:
    lines = [
        "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
        "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
        "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
        "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
        "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
        "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
        "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
        "Valve HH has flow rate=22; tunnel leads to valve GG",
        "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
        "Valve JJ has flow rate=21; tunnel leads to valve II",
    ]

    return parse(lines)


def test_parse():
    lines = [
        "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
        "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
        "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
        "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
        "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
        "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
        "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
        "Valve HH has flow rate=22; tunnel leads to valve GG",
        "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
        "Valve JJ has flow rate=21; tunnel leads to valve II",
    ]

    valves = parse(lines)
    for name, valve in valves.items():
        assert valve.flow_rate is not None
        assert valve.name == name

    assert valves["AA"].child_names == ["DD", "II", "BB"]
    assert valves["AA"].flow_rate == 0

    reprs = []
    for valve in valves.values():
        reprs.append(repr(valve))

    assert reprs == [
        "<Valve name=DD flow_rate=20 children=['CC', 'AA', 'EE']>",
        "<Valve name=II flow_rate=0 children=['AA', 'JJ']>",
        "<Valve name=BB flow_rate=13 children=['CC', 'AA']>",
        "<Valve name=AA flow_rate=0 children=['DD', 'II', 'BB']>",
        "<Valve name=CC flow_rate=2 children=['DD', 'BB']>",
        "<Valve name=EE flow_rate=3 children=['FF', 'DD']>",
        "<Valve name=FF flow_rate=0 children=['EE', 'GG']>",
        "<Valve name=GG flow_rate=0 children=['FF', 'HH']>",
        "<Valve name=HH flow_rate=22 children=['GG']>",
        "<Valve name=JJ flow_rate=21 children=['II']>",
    ]


def test_compute_distances(sample: dict[str, Valve]):
    assert compute_distances(sample["AA"]) == {
        "AA": 0,
        "DD": 1,
        "II": 1,
        "BB": 1,
        "CC": 2,
        "EE": 2,
        "JJ": 2,
        "FF": 3,
        "GG": 4,
        "HH": 5,
    }


def test_part01(sample: dict[str, Valve]):
    assert part01(sample) == 1651


if __name__ == "__main__":
    sys.exit(main())
