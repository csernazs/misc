#!/usr/bin/env python3
from dataclasses import dataclass
import sys
import re
from typing import Optional, Tuple, List

import pytest

P = Tuple[int, int]


def dist(p1: P, p2: P) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


@dataclass
class Sensor:
    pos: P
    beacon: P

    def __post_init__(self):
        self.range = dist(self.pos, self.beacon)

    def in_range(self, pos: P) -> bool:
        d = dist(pos, self.pos)
        return d <= self.range

    def get_range_at_y(self, y: int) -> Optional[P]:
        length = self.range - abs(self.pos[1] - y)
        if length >= 0:
            return (self.pos[0] - length, self.pos[0] + length)
        return None


def merge_ranges(ranges: list[P]):
    ### print("merge_ranges called with", ranges)
    ranges = ranges.copy()

    ranges.sort(key=lambda x: x[1] - x[0], reverse=True)

    new_ranges: list = []

    ### print("ranges", ranges)
    for idx, r in enumerate(ranges):
        if new_ranges == []:
            new_ranges.append(list(r))
            continue
        ### print(new_ranges)
        for new_range in new_ranges:
            if r[0] >= new_range[0] and r[1] <= new_range[1]:
                break
            elif r[0] < new_range[0] and r[1] > new_range[1]:
                new_range[0] = r[0]
                new_range[1] = r[1]
                break
            elif r[0] >= new_range[0] and r[0] <= new_range[1] + 1 and r[1] > new_range[1]:
                new_range[1] = r[1]
                break
            elif r[1] >= new_range[0] - 1 and r[1] <= new_range[1] - 1 and r[0] < new_range[0]:
                new_range[0] = r[0]
                break
            else:
                new_ranges.append(list(r))

    retval = [tuple(x) for x in new_ranges]
    ### print("merge_ranges returns with", retval)
    return retval


def merge_ranges_to_minimum(ranges: list[P]):
    while True:
        new_ranges = merge_ranges(ranges)
        if new_ranges == ranges:
            return new_ranges

        ranges = new_ranges.copy()


def parse_line(line: str) -> Sensor:
    m = re.match(r"Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)", line)
    if m:
        fields = [int(x) for x in m.groups()]
        return Sensor(pos=(fields[0], fields[1]), beacon=(fields[2], fields[3]))
    else:
        raise ValueError(line)


def parse(lines: List[str]) -> List[Sensor]:
    retval: List[Sensor] = []
    for line in lines:
        retval.append(parse_line(line))
    return retval


def part01(sensors: List[Sensor], y: int):
    ranges = []
    for sensor in sensors:
        r = sensor.get_range_at_y(y)
        if r is not None:
            ranges.append(r)

    print(ranges)
    minimal_ranges = merge_ranges_to_minimum(ranges)
    print(minimal_ranges)
    cnt = 0
    for r in minimal_ranges:
        cnt += r[1] - r[0] + 1

    print("partial cnt", cnt)
    seen = set()
    for sensor in sensors:
        if sensor.pos[1] == y:
            for r in minimal_ranges:
                if sensor.pos[0] >= r[0] and sensor.pos[0] <= r[1] and sensor.pos not in seen:
                    print("pos", sensor.pos)
                    seen.add(sensor.pos)
                    cnt -= 1

        if sensor.beacon[1] == y:
            for r in minimal_ranges:
                if sensor.beacon[0] >= r[0] and sensor.beacon[0] <= r[1] and sensor.beacon not in seen:
                    print("beacon", sensor.beacon)
                    seen.add(sensor.beacon)
                    cnt -= 1
    print("final cnt", cnt)
    return cnt


def part02(sensors: List[Sensor], size: int):
    for y in range(size):
        if y % 10000 == 0:
            print(y)
        ranges = []
        for sensor in sensors:
            r = sensor.get_range_at_y(y)
            if r is not None:
                ranges.append(r)

        ranges = merge_ranges_to_minimum(ranges)
        if len(ranges) > 1:
            print(y, ranges)


def main():
    with open("aoc_15.txt") as infile:
        lines = [x.strip() for x in infile]

    parsed = parse(lines)
    print(part01(parsed, 2000000))
    print(part02(parsed, 4000000))


@pytest.fixture
def sample() -> List[Sensor]:
    return [
        Sensor(pos=(2, 18), beacon=(-2, 15)),
        Sensor(pos=(9, 16), beacon=(10, 16)),
        Sensor(pos=(13, 2), beacon=(15, 3)),
        Sensor(pos=(12, 14), beacon=(10, 16)),
        Sensor(pos=(10, 20), beacon=(10, 16)),
        Sensor(pos=(14, 17), beacon=(10, 16)),
        Sensor(pos=(8, 7), beacon=(2, 10)),
        Sensor(pos=(2, 0), beacon=(2, 10)),
        Sensor(pos=(0, 11), beacon=(2, 10)),
        Sensor(pos=(20, 14), beacon=(25, 17)),
        Sensor(pos=(17, 20), beacon=(21, 22)),
        Sensor(pos=(16, 7), beacon=(15, 3)),
        Sensor(pos=(14, 3), beacon=(15, 3)),
        Sensor(pos=(20, 1), beacon=(15, 3)),
    ]


def test_parse(sample: List[Sensor]):
    lines = [
        "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
        "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
        "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
        "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
        "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
        "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
        "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
        "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
        "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
        "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
        "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
        "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
        "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
        "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
    ]
    assert parse(lines) == sample


def test_part01(sample: List[Sensor]):
    assert part01(sample, 10) == 26


@pytest.mark.skip
def test_part02(sample: List[Sensor]):
    assert part02(sample, 20) == 56000011


def test_get_range_at_y():
    sensor = Sensor(pos=(8, 7), beacon=(2, 10))
    assert sensor.get_range_at_y(7) == (-1, 17)
    assert sensor.get_range_at_y(6) == (0, 16)
    assert sensor.get_range_at_y(5) == (1, 15)
    assert sensor.get_range_at_y(4) == (2, 14)
    assert sensor.get_range_at_y(3) == (3, 13)
    assert sensor.get_range_at_y(2) == (4, 12)
    assert sensor.get_range_at_y(1) == (5, 11)

    assert sensor.get_range_at_y(8) == (0, 16)
    assert sensor.get_range_at_y(9) == (1, 15)
    assert sensor.get_range_at_y(10) == (2, 14)
    assert sensor.get_range_at_y(11) == (3, 13)
    assert sensor.get_range_at_y(12) == (4, 12)
    assert sensor.get_range_at_y(13) == (5, 11)

    assert sensor.get_range_at_y(14) == (6, 10)
    assert sensor.get_range_at_y(15) == (7, 9)
    assert sensor.get_range_at_y(16) == (8, 8)
    assert sensor.get_range_at_y(17) is None
    assert sensor.get_range_at_y(18) is None
    assert sensor.get_range_at_y(19) is None


def test_merge_ranges():
    assert merge_ranges([(10, 20), (30, 40)]) == [(10, 20), (30, 40)]
    assert merge_ranges([(10, 20), (20, 30)]) == [(10, 30)]
    assert merge_ranges([(10, 20), (15, 30)]) == [(10, 30)]
    assert merge_ranges([(10, 20), (5, 15)]) == [(5, 20)]
    assert merge_ranges([(10, 20), (5, 25)]) == [(5, 25)]

    assert merge_ranges([(15, 15), (2, 14), (1, 1), (10, 14), (11, 19), (6, 10)]) == [(1, 19)]

    assert merge_ranges([(1, 1), (2, 10)]) == [(1, 10)]
    assert merge_ranges([(11, 11), (2, 10)]) == [(2, 11)]


if __name__ == "__main__":
    sys.exit(main())
