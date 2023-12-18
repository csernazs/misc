#!/usr/bin/env python3

import re
import sys
from dataclasses import dataclass

import pytest


@dataclass
class Range:
    source_start: int
    destination_start: int
    length: int

    def get_destination(self, source_key: int) -> int | None:
        offset = source_key - self.source_start
        if offset >= 0 and offset < self.length:
            return self.destination_start + offset

        return None

    def reverse(self) -> "Range":
        return Range(
            source_start=self.destination_start, destination_start=self.source_start, length=self.length
        )


@dataclass
class Map:
    ranges: list[Range]

    def __post_init__(self):
        self.ranges.sort(key=lambda rng: rng.source_start)

    def reverse(self) -> "Map":
        new_ranges: list[Range] = []
        for rng in self.ranges:
            new_ranges.append(rng.reverse())

        return Map(ranges=new_ranges)

    def __contains__(self, source_key: int) -> bool:
        for rng in self.ranges:
            if rng.get_destination(source_key) is not None:
                return True
        return False

    def __getitem__(self, source_key: int):
        for rng in self.ranges:
            if (dst := rng.get_destination(source_key)) is not None:
                return dst
        return source_key


@dataclass
class Almanac:
    seeds: list[int]
    maps: dict[tuple[str, str], Map]


def parse_lines(lines: list[str]) -> Almanac:
    seeds = [int(x) for x in lines[0].split()[1:]]

    maps: dict[tuple[str, str], Map] = {}

    map_from: str | None = None
    map_to: str | None = None

    current_ranges: list[Range] = []
    for line in lines[2:]:
        if line == "":
            continue

        if m := re.match("([a-z]+)-to-([a-z]+) map:", line):
            if map_from and map_to:
                maps[(map_from, map_to)] = Map(ranges=current_ranges)
            map_from, map_to = m.groups()
            current_ranges = []
        else:
            dest, source, length = [int(x) for x in line.split()]
            rng = Range(source_start=source, destination_start=dest, length=length)
            current_ranges.append(rng)

    if map_from and map_to and not (map_from, map_to) in maps:
        maps[(map_from, map_to)] = Map(current_ranges)

    return Almanac(seeds=seeds, maps=maps)


MAPS = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
MAP_PAIRS: list[tuple[str, str]] = [(MAPS[i], MAPS[i + 1]) for i in range(len(MAPS) - 1)]


def get_location(almanac: Almanac, seed: int) -> int:
    source = seed
    for map_key in MAP_PAIRS:
        current_map: Map = almanac.maps[map_key]
        source = current_map[source]
    return source


def part_01(almanac: Almanac) -> int:
    location_seed: list[tuple[int, int]] = []

    lowest_location: int = 2**32
    for seed in almanac.seeds:
        location = get_location(almanac, seed)
        location_seed.append((location, seed))
        if location < lowest_location:
            lowest_location = location

    return lowest_location


def part_02(almanac: Almanac) -> int:
    seed_ranges = [(almanac.seeds[idx], almanac.seeds[idx + 1]) for idx in range(0, len(almanac.seeds), 2)]
    seed_map = Map(ranges=[Range(start, start, length) for start, length in seed_ranges])

    maps: list[Map] = []
    for map_key in reversed(MAP_PAIRS):
        maps.append(almanac.maps[map_key].reverse())

    location = 0
    while True:
        source = location
        for map in maps:
            source = map[source]

        if source in seed_map:
            return location
        location += 1


def main():
    with open("aoc_05.txt") as infile:
        lines = [line.strip() for line in infile]

    almanac = parse_lines(lines)
    print(part_01(almanac))
    print(part_02(almanac))


@pytest.fixture()
def almanac() -> Almanac:
    return Almanac(
        seeds=[79, 14, 55, 13],
        maps={
            ("seed", "soil"): Map(
                ranges=[
                    Range(source_start=98, destination_start=50, length=2),
                    Range(source_start=50, destination_start=52, length=48),
                ]
            ),
            ("soil", "fertilizer"): Map(
                ranges=[
                    Range(source_start=15, destination_start=0, length=37),
                    Range(source_start=52, destination_start=37, length=2),
                    Range(source_start=0, destination_start=39, length=15),
                ]
            ),
            ("fertilizer", "water"): Map(
                ranges=[
                    Range(source_start=53, destination_start=49, length=8),
                    Range(source_start=11, destination_start=0, length=42),
                    Range(source_start=0, destination_start=42, length=7),
                    Range(source_start=7, destination_start=57, length=4),
                ]
            ),
            ("water", "light"): Map(
                ranges=[
                    Range(source_start=18, destination_start=88, length=7),
                    Range(source_start=25, destination_start=18, length=70),
                ]
            ),
            ("light", "temperature"): Map(
                ranges=[
                    Range(source_start=77, destination_start=45, length=23),
                    Range(source_start=45, destination_start=81, length=19),
                    Range(source_start=64, destination_start=68, length=13),
                ]
            ),
            ("temperature", "humidity"): Map(
                ranges=[
                    Range(source_start=69, destination_start=0, length=1),
                    Range(source_start=0, destination_start=1, length=69),
                ]
            ),
            ("humidity", "location"): Map(
                ranges=[
                    Range(source_start=56, destination_start=60, length=37),
                    Range(source_start=93, destination_start=56, length=4),
                ]
            ),
        },
    )


def test_parse(almanac: Almanac):
    lines = [
        "seeds: 79 14 55 13",
        "",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
        "soil-to-fertilizer map:",
        "0 15 37",
        "37 52 2",
        "39 0 15",
        "",
        "fertilizer-to-water map:",
        "49 53 8",
        "0 11 42",
        "42 0 7",
        "57 7 4",
        "",
        "water-to-light map:",
        "88 18 7",
        "18 25 70",
        "",
        "light-to-temperature map:",
        "45 77 23",
        "81 45 19",
        "68 64 13",
        "",
        "temperature-to-humidity map:",
        "0 69 1",
        "1 0 69",
        "",
        "humidity-to-location map:",
        "60 56 37",
        "56 93 4",
    ]

    parsed_almanac = parse_lines(lines)

    assert parsed_almanac == almanac


def test_map():
    map = Map(
        ranges=[
            Range(destination_start=50, source_start=98, length=2),
            Range(destination_start=52, source_start=50, length=48),
        ]
    )

    expected = {
        48: 48,
        49: 49,
        50: 52,
        51: 53,
        52: 54,
        53: 55,
        54: 56,
        55: 57,
        56: 58,
        57: 59,
        58: 60,
        59: 61,
        60: 62,
        61: 63,
        62: 64,
        63: 65,
        64: 66,
        65: 67,
        66: 68,
        67: 69,
        68: 70,
        69: 71,
        70: 72,
        71: 73,
        72: 74,
        73: 75,
        74: 76,
        75: 77,
        76: 78,
        77: 79,
        78: 80,
        79: 81,
        80: 82,
        81: 83,
        82: 84,
        83: 85,
        84: 86,
        85: 87,
        86: 88,
        87: 89,
        88: 90,
        89: 91,
        90: 92,
        91: 93,
        92: 94,
        93: 95,
        94: 96,
        95: 97,
        96: 98,
        97: 99,
        98: 50,
        99: 51,
    }

    for key in range(100):
        if key not in expected:
            assert map[key] == key
        else:
            assert map[key] == expected[key]


def test_part01(almanac: Almanac):
    assert part_01(almanac) == 35


def test_part02(almanac: Almanac):
    assert part_02(almanac) == 46


if __name__ == "__main__":
    sys.exit(main())
