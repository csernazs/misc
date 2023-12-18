#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from math import ceil, sqrt

try:
    import pytest
except ImportError:
    pytest = None


@dataclass
class Race:
    time: int
    distance: int


def parse_lines_1(lines: list[str]) -> list[Race]:
    times = lines[0].split()[1:]
    distances = lines[1].split()[1:]
    retval: list[Race] = []
    for time, distance in zip(times, distances):
        retval.append(Race(int(time), int(distance)))
    return retval


def parse_lines_2(lines: list[str]) -> Race:
    times = lines[0].split()[1:]
    distances = lines[1].split()[1:]

    return Race(int("".join(times)), int("".join(distances)))


def solve_race(race: Race) -> int:
    # (race.time - speed) * speed = race.distance

    # a = -1
    # b = race.time
    # c = -race.distance

    min_speed = ((0 - race.time) + sqrt(race.time**2 - 4 * race.distance)) / (-2)
    max_speed = ((0 - race.time) - sqrt(race.time**2 - 4 * race.distance)) / (-2)
    retval = ceil(max_speed - 0.01) - ceil(min_speed + 0.01)
    return int(retval)


def part_01(races: list[Race]) -> int:
    retval: int = 1

    for race in races:
        cnt = solve_race(race)
        retval = retval * cnt

    return retval


def part_02(race: Race) -> int:
    return solve_race(race)


def main():
    with open("aoc_06.txt") as infile:
        lines = [x.strip() for x in infile]

    races = parse_lines_1(lines)
    print(part_01(races))
    print(part_02(parse_lines_2(lines)))


if pytest is not None:

    @pytest.fixture()
    def races() -> list[Race]:
        return [
            Race(time=7, distance=9),
            Race(time=15, distance=40),
            Race(time=30, distance=200),
        ]

    def test_parse(races: list[Race]):
        lines = [
            "Time:      7  15   30",
            "Distance:  9  40  200",
        ]
        assert parse_lines_1(lines) == races

    def test_part01(races: list[Race]):
        assert part_01(races) == 288

    def test_part02():
        assert part_02(Race(time=71530, distance=940200)) == 71503


if __name__ == "__main__":
    sys.exit(main())
