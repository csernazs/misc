#!/usr/bin/env python3

from collections import deque
import sys

import pytest

CUBE = tuple[int, int, int]
CUBELIST = list[CUBE]


def get_sides_for_cube(cubes_set: set[CUBE], cube: CUBE) -> int:
    # sides = 6
    # close_cubes = [
    #     (cube[0] + 1, cube[1], cube[2]),
    #     (cube[0] - 1, cube[1], cube[2]),
    #     (cube[0], cube[1] + 1, cube[2]),
    #     (cube[0], cube[1] - 1, cube[2]),
    #     (cube[0], cube[1], cube[2] + 1),
    #     (cube[0], cube[1], cube[2] - 1),
    # ]
    # for close_cube in close_cubes:
    #     if close_cube in cubes_set:
    #         sides = sides - 1

    return 6 - len(get_nearby_cubes(cubes_set, cube)[0])


def get_nearby_cubes(cubes_set: set[CUBE], cube: CUBE) -> tuple[CUBELIST, CUBELIST]:
    nearby: CUBELIST = []
    empty: CUBELIST = []
    close_cubes = [
        (cube[0] + 1, cube[1], cube[2]),
        (cube[0] - 1, cube[1], cube[2]),
        (cube[0], cube[1] + 1, cube[2]),
        (cube[0], cube[1] - 1, cube[2]),
        (cube[0], cube[1], cube[2] + 1),
        (cube[0], cube[1], cube[2] - 1),
    ]
    for close_cube in close_cubes:
        if close_cube in cubes_set:
            nearby.append(close_cube)
        else:
            empty.append(close_cube)

    return (nearby, empty)


def part01(cubes: CUBELIST) -> int:
    cubes_set = set(cubes)

    sides = 0
    for cube in cubes:
        sides += get_sides_for_cube(cubes_set, cube)
    return sides


def part02(cubes: CUBELIST) -> int:
    cubes_set = set(cubes)
    min_x = min(cubes, key=lambda x: x[0])[0] - 1
    min_y = min(cubes, key=lambda x: x[1])[1] - 1
    min_z = min(cubes, key=lambda x: x[2])[2] - 1

    max_x = max(cubes, key=lambda x: x[0])[0] + 1
    max_y = max(cubes, key=lambda x: x[1])[1] + 1
    max_z = max(cubes, key=lambda x: x[2])[2] + 1

    queue = deque([(min_x, min_y, min_z)])

    retval = 0

    seen: set[CUBE] = set()

    while queue:
        pos = queue.popleft()
        if pos in seen:
            continue

        seen.add(pos)

        nearby_cubes, empty_places = get_nearby_cubes(cubes_set, pos)
        retval += len(nearby_cubes)
        for empty in empty_places:
            if (
                empty in seen
                or empty[0] < min_x
                or empty[1] < min_y
                or empty[2] < min_z
                or empty[0] > max_x
                or empty[1] > max_y
                or empty[2] > max_z
            ):
                continue

            queue.append(empty)

    return retval


def parse(lines: list[str]) -> CUBELIST:
    retval = []
    for line in lines:
        fields = line.split(",")
        assert len(fields) == 3
        retval.append((int(fields[0]), int(fields[1]), int(fields[2])))

    return retval


def main():
    with open("aoc_18.txt") as infile:
        lines = [x.strip() for x in infile]

    cubes = parse(lines)
    print(part01(cubes))
    print(part02(cubes))


@pytest.fixture
def sample() -> CUBELIST:
    return [
        (2, 2, 2),
        (1, 2, 2),
        (3, 2, 2),
        (2, 1, 2),
        (2, 3, 2),
        (2, 2, 1),
        (2, 2, 3),
        (2, 2, 4),
        (2, 2, 6),
        (1, 2, 5),
        (3, 2, 5),
        (2, 1, 5),
        (2, 3, 5),
    ]


def test_parse(sample: CUBELIST):
    lines = [
        "2,2,2",
        "1,2,2",
        "3,2,2",
        "2,1,2",
        "2,3,2",
        "2,2,1",
        "2,2,3",
        "2,2,4",
        "2,2,6",
        "1,2,5",
        "3,2,5",
        "2,1,5",
        "2,3,5",
    ]

    assert parse(lines) == sample


def test_part01(sample: CUBELIST):
    assert part01(sample) == 64


def test_part02(sample: CUBELIST):
    assert part02(sample) == 58


if __name__ == "__main__":
    sys.exit(main())
