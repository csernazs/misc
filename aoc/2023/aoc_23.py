#!/usr/bin/env python3

import sys
from collections import deque
from dataclasses import dataclass
from functools import cached_property
from typing import Callable, Iterable

import pytest

PATH = 1
FOREST = 2
LEFT = 3
RIGHT = 4
UP = 5
DOWN = 6


@dataclass
class Tile:
    type: int
    max_distance: int = 0


GRID_INT = list[list[int]]
GRID = list[list[Tile]]
PAIR = tuple[int, int]


def parse_lines(lines: Iterable[str]) -> GRID_INT:
    rows: GRID_INT = []

    char_map = {
        ".": PATH,
        "#": FOREST,
        ">": RIGHT,
        "<": LEFT,
        "v": DOWN,
        "^": UP,
    }

    for line in lines:
        row: list[int] = []
        for char in line:
            row.append(char_map[char])
        rows.append(row)
    return rows


"""

#.###
#...#
#.#.#
#...#
#.###

#1###
#234#
#3#5#
#476#
#5###


"""


def condition_with_slopes(type: int, dir: PAIR) -> bool:
    return (
        type == PATH
        or (type == UP and dir == (-1, 0))
        or (type == DOWN and dir == (1, 0))
        or (type == LEFT and dir == (0, -1))
        or (type == RIGHT and dir == (0, 1))
    )


def condition_without_slopes(type: int, dir: PAIR) -> bool:
    return type in (PATH, UP, DOWN, LEFT, RIGHT)


@dataclass(frozen=True)
class QueueItem:
    route: list[PAIR]
    route_set: set[PAIR]


def print_grid(grid: GRID):
    for row in grid:
        print("".join([f"{cell.max_distance:4}" for cell in row]))


def walk(
    grid: GRID, start: PAIR, target: PAIR, *, condition: Callable[[int, PAIR], bool]
) -> list[list[PAIR]]:
    queue: deque[QueueItem] = deque(
        [
            QueueItem(
                route=[start],
                route_set={
                    start,
                },
            )
        ]
    )
    directions: list[PAIR] = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    routes: list[list[PAIR]] = []

    iter_cnt = 0
    while queue:
        iter_cnt += 1

        qi = queue.popleft()
        pos = qi.route[-1]

        if iter_cnt % 10000 == 0:
            print(len(queue), len(routes), len(qi.route))

        if pos == target:
            for idx, route_pos in enumerate(qi.route):
                if grid[route_pos[0]][route_pos[1]].max_distance < idx + 1:
                    grid[route_pos[0]][route_pos[1]].max_distance = idx + 1
            print("new route", len(qi.route))
            routes.append(qi.route.copy())
            # print_grid(grid)

            continue

        current = grid[pos[0]][pos[1]]
        if current.max_distance > len(qi.route):
            continue

        new_pos_list: list[PAIR] = []

        for dir in directions:
            new_pos: PAIR = (pos[0] + dir[0], pos[1] + dir[1])
            if (
                new_pos[0] < 0
                or new_pos[1] < 0
                or new_pos[0] > len(grid) - 1
                or new_pos[1] > len(grid[new_pos[0]]) - 1
            ):
                continue

            if new_pos in qi.route_set:
                continue

            new_tile = grid[new_pos[0]][new_pos[1]]

            if condition(new_tile.type, dir):
                # if current.max_distance - new_tile.max_distance > 0 or new_tile.max_distance == 0:
                #     new_tile.max_distance = current.max_distance + 1

                new_pos_list.append(new_pos)

        if len(new_pos_list) == 1:
            queue.appendleft(
                QueueItem(
                    qi.route + [new_pos_list[0]],
                    qi.route_set.union(
                        {
                            new_pos_list[0],
                        }
                    ),
                )
            )
        elif len(new_pos_list) > 1:
            for new_pos in new_pos_list:
                queue.append(
                    QueueItem(
                        qi.route + [new_pos],
                        qi.route_set.union(
                            {
                                new_pos,
                            }
                        ),
                    )
                )

    return routes


@dataclass
class Crossing:
    pos: PAIR
    directions: list[PAIR]
    routes: list[list[PAIR]]

    @cached_property
    def routes_set(self) -> list[set[PAIR]]:
        return [set(route) for route in self.routes]


CROSSING_DICT = dict[PAIR, Crossing]


def iter_neigh(grid: GRID_INT, pos: PAIR) -> Iterable[PAIR]:
    directions: list[PAIR] = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    for dir in directions:
        new_pos: PAIR = (pos[0] + dir[0], pos[1] + dir[1])
        if (
            new_pos[0] < 0
            or new_pos[1] < 0
            or new_pos[0] > len(grid) - 1
            or new_pos[1] > len(grid[new_pos[0]]) - 1
        ):
            continue

        if grid[new_pos[0]][new_pos[1]] != FOREST:
            yield new_pos


def get_route(
    grid: GRID_INT, crossings: CROSSING_DICT, *, start_pos: PAIR, start_direction: PAIR
) -> list[PAIR]:
    old_pos = start_pos

    pos = (start_pos[0] + start_direction[0], start_pos[1] + start_direction[1])
    route: list[PAIR] = [pos]

    while pos not in crossings:
        neigh = list(iter_neigh(grid, pos))
        try:
            neigh.remove(old_pos)
        except ValueError:
            pass

        if len(neigh) > 1:
            raise ValueError(f"{pos} is a crossing? neigh={neigh!r}")

        elif len(neigh) == 0:  # dead end or target?
            return route

        elif len(neigh) == 1:
            old_pos = pos
            pos = neigh[0]
            route.append(pos)

    return route


def get_cells_exists(
    grid: GRID_INT, condition: Callable[[list[PAIR]], bool]
) -> list[tuple[PAIR, list[PAIR]]]:
    directions: list[PAIR] = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]
    retval: list[tuple[PAIR, list[PAIR]]] = []

    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == FOREST:
                continue

            valid_dirs: list[PAIR] = []

            for dir in directions:
                new_pos: PAIR = (row_idx + dir[0], col_idx + dir[1])
                if (
                    new_pos[0] < 0
                    or new_pos[1] < 0
                    or new_pos[0] > len(grid) - 1
                    or new_pos[1] > len(grid[new_pos[0]]) - 1
                ):
                    continue

                if grid[new_pos[0]][new_pos[1]] != FOREST:
                    valid_dirs.append(dir)

            if condition(valid_dirs):
                retval.append(((row_idx, col_idx), valid_dirs))

    return retval


def get_crossings(grid: GRID_INT) -> CROSSING_DICT:
    pos_list = get_cells_exists(grid, lambda neigh: len(neigh) > 2)
    crossings: dict[PAIR, Crossing] = {}
    for pos, directions in pos_list:
        crossings[pos] = Crossing(pos=pos, directions=directions, routes=[])

    for crossing in crossings.values():
        for direction in crossing.directions:
            route = get_route(grid, crossings, start_pos=(crossing.pos), start_direction=direction)
            crossing.routes.append(route)

        crossing.routes.sort(key=len, reverse=True)

    return crossings


def part_01(grid_int: GRID_INT) -> int:
    grid = [[Tile(type) for type in row] for row in grid_int]
    pos: PAIR = (0, 1)
    grid[pos[0]][pos[1]].max_distance = 1

    routes = walk(grid, (0, 1), (len(grid) - 1, len(grid[-1]) - 2), condition=condition_with_slopes)
    return len(max(routes, key=len)) - 1


def part_02_old(grid_int: GRID_INT) -> int:
    grid = [[Tile(type) for type in row] for row in grid_int]
    pos: PAIR = (0, 1)
    grid[pos[0]][pos[1]].max_distance = 1

    routes = walk(grid, (0, 1), (len(grid) - 1, len(grid[-1]) - 2), condition=condition_without_slopes)
    return len(max(routes, key=len)) - 1


g_routes: list[list[PAIR]] = []


def walk_crossings(
    grid: GRID_INT, crossings: CROSSING_DICT, end_pos: PAIR, route: list[PAIR], level: int
) -> list[PAIR]:
    current = route[-1]
    if current == end_pos:
        return route

    route_set = set(route)
    crossing = crossings[current]

    routes: list[list[PAIR]] = []

    for outward, outward_set in zip(crossing.routes, crossing.routes_set):
        if outward[-1] in crossings and not route_set.intersection(outward_set):
            routes.append(walk_crossings(grid, crossings, end_pos, route + outward, level + 1))

    if len(routes) == 1:
        return routes[0]
    if len(routes) == 0:
        return []

    if level < 10:
        print(level, len(max(routes, key=len)))

    return max(routes, key=len)


def part_02_recursive(grid: GRID_INT) -> int:
    crossings = get_crossings(grid)

    start_route = get_route(grid, crossings, start_pos=(0, 1), start_direction=(1, 0))
    print(start_route)
    assert start_route[-1] in crossings

    end_route = get_route(
        grid, crossings, start_pos=(len(grid) - 1, len(grid[0]) - 2), start_direction=(-1, 0)
    )
    assert end_route[-1] in crossings
    end_crossing_pos = end_route[-1]

    longest = walk_crossings(grid, crossings, end_pos=end_crossing_pos, route=start_route, level=0)
    print(start_route)
    print(longest)
    print(end_route)
    return len(longest) + len(end_route)


def part_02(grid: GRID_INT) -> int:
    crossings = get_crossings(grid)

    start_route = get_route(grid, crossings, start_pos=(0, 1), start_direction=(1, 0))
    print(start_route)
    assert start_route[-1] in crossings

    end_route = get_route(
        grid, crossings, start_pos=(len(grid) - 1, len(grid[0]) - 2), start_direction=(-1, 0)
    )
    assert end_route[-1] in crossings
    end_crossing_pos = end_route[-1]

    start_crossing = crossings[start_route[-1]]
    end_crossing = crossings[end_crossing_pos]

    remaining_crossings = [
        c for c in crossings.values() if c.pos != start_crossing.pos and c.pos != end_crossing.pos
    ]
    print(len(remaining_crossings))

    return 999


def main():
    with open("aoc_23.txt") as infile:
        lines = [line.strip() for line in infile]
    grid = parse_lines(lines)

    # print(part_01(grid))
    print(part_02_recursive(grid))


@pytest.fixture(name="grid")
def f_grid() -> GRID_INT:
    return [
        [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2],
        [2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 4, 1, 4, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2],
        [2, 2, 2, 6, 2, 2, 2, 2, 2, 1, 2, 6, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2],
        [2, 2, 2, 1, 4, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2],
        [2, 2, 2, 6, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2],
        [2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2],
        [2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2],
        [2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2],
        [2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 2],
        [2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 4, 1, 2],
        [2, 1, 2, 1, 2, 6, 2, 2, 2, 2, 2, 2, 2, 6, 2, 2, 2, 1, 2, 2, 2, 6, 2],
        [2, 1, 1, 1, 2, 1, 4, 1, 2, 1, 1, 1, 4, 1, 4, 1, 2, 1, 2, 2, 2, 1, 2],
        [2, 2, 2, 2, 2, 6, 2, 1, 2, 1, 2, 2, 2, 6, 2, 1, 2, 1, 2, 2, 2, 1, 2],
        [2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2],
        [2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2],
        [2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2],
        [2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 6, 2, 2, 2, 2, 2, 6, 2, 2, 2],
        [2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 4, 1, 4, 1, 2, 1, 4, 1, 2, 2, 2],
        [2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 6, 2, 2, 2],
        [2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2],
    ]


def test_parse(grid: GRID_INT):
    lines = [
        "#.#####################",
        "#.......#########...###",
        "#######.#########.#.###",
        "###.....#.>.>.###.#.###",
        "###v#####.#v#.###.#.###",
        "###.>...#.#.#.....#...#",
        "###v###.#.#.#########.#",
        "###...#.#.#.......#...#",
        "#####.#.#.#######.#.###",
        "#.....#.#.#.......#...#",
        "#.#####.#.#.#########v#",
        "#.#...#...#...###...>.#",
        "#.#.#v#######v###.###v#",
        "#...#.>.#...>.>.#.###.#",
        "#####v#.#.###v#.#.###.#",
        "#.....#...#...#.#.#...#",
        "#.#########.###.#.#.###",
        "#...###...#...#...#.###",
        "###.###.#.###v#####v###",
        "#...#...#.#.>.>.#.>.###",
        "#.###.###.#.###.#.#v###",
        "#.....###...###...#...#",
        "#####################.#",
    ]
    assert parse_lines(lines) == grid


def test_part01(grid: GRID_INT):
    assert part_01(grid) == 94


def test_part02(grid: GRID_INT):
    assert part_02(grid) == 154


def test_walk():
    lines = [
        "#.###",
        "#...#",
        "#.#.#",
        "#...#",
        "#.###",
    ]

    grid: GRID = [[Tile(type) for type in row] for row in parse_lines(lines)]
    grid[0][1].max_distance = 1
    routes = walk(grid, (0, 1), (4, 1), condition=condition_without_slopes)

    # print(routes)
    assert len(max(routes, key=len)) == 9


def test_crossings():
    lines = [
        "#.#####",
        "#.....#",
        "#.#.#.#",
        "#.....#",
        "#.#####",
    ]

    grid: GRID_INT = parse_lines(lines)
    crossings: CROSSING_DICT = get_crossings(grid)
    assert crossings == {
        (1, 1): Crossing(
            pos=(1, 1),
            directions=[(-1, 0), (1, 0), (0, 1)],
            routes=[[(0, 1)], [(2, 1), (3, 1)], [(1, 2), (1, 3)]],
        ),
        (1, 3): Crossing(
            pos=(1, 3),
            directions=[(1, 0), (0, -1), (0, 1)],
            routes=[[(2, 3), (3, 3)], [(1, 2), (1, 1)], [(1, 4), (1, 5), (2, 5), (3, 5), (3, 4), (3, 3)]],
        ),
        (3, 1): Crossing(
            pos=(3, 1),
            directions=[(-1, 0), (1, 0), (0, 1)],
            routes=[[(2, 1), (1, 1)], [(4, 1)], [(3, 2), (3, 3)]],
        ),
        (3, 3): Crossing(
            pos=(3, 3),
            directions=[(-1, 0), (0, -1), (0, 1)],
            routes=[[(2, 3), (1, 3)], [(3, 2), (3, 1)], [(3, 4), (3, 5), (2, 5), (1, 5), (1, 4), (1, 3)]],
        ),
    }


def test_routes():
    lines = [
        # 123456
        "#.#####",  # 0
        "#.....#",  # 1
        "#.#.#.#",  # 2
        "#.....#",  # 3
        "#.#####",  # 4
    ]

    grid: GRID_INT = parse_lines(lines)
    crossings: CROSSING_DICT = get_crossings(grid)

    assert get_route(grid, crossings, start_pos=(0, 1), start_direction=(1, 0)) == [(1, 1)]
    assert get_route(grid, crossings, start_pos=(1, 1), start_direction=(1, 0)) == [(2, 1), (3, 1)]
    assert get_route(grid, crossings, start_pos=(1, 1), start_direction=(0, 1)) == [(1, 2), (1, 3)]
    assert get_route(grid, crossings, start_pos=(1, 3), start_direction=(0, 1)) == [
        (1, 4),
        (1, 5),
        (2, 5),
        (3, 5),
        (3, 4),
        (3, 3),
    ]


if __name__ == "__main__":
    sys.exit(main())
