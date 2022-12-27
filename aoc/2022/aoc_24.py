#!/usr/bin/env python3

import sys
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Optional

import pytest

P = tuple[int, int]


@dataclass(frozen=True)
class Cell:
    dir: P

    def move(self, pos: P) -> P:
        return (pos[0] + self.dir[0], pos[1] + self.dir[1])

    def move_wrap_around(self, orig_pos: P, width: int, height: int) -> P:
        new_pos = list(self.move(orig_pos))
        if new_pos[0] < 0:
            new_pos[0] = height - 1
        elif new_pos[0] > height - 1:
            new_pos[0] = 0
        if new_pos[1] < 0:
            new_pos[1] = width - 1
        elif new_pos[1] > width - 1:
            new_pos[1] = 0

        return (new_pos[0], new_pos[1])


CELLS = dict[P, list[Cell]]

UP = Cell((-1, 0))
DOWN = Cell((1, 0))
LEFT = Cell((0, -1))
RIGHT = Cell((0, 1))


@dataclass
class Grid:
    cells: CELLS
    width: int
    height: int


class Play:
    def __init__(self, grid: Grid):
        self.cells = grid.cells
        self.width = grid.width
        self.height = grid.height

    def move_cells(self) -> CELLS:
        new_cells: CELLS = defaultdict(list)

        for pos, cells in self.cells.items():
            for cell in cells:
                new_pos = cell.move_wrap_around(pos, self.width, self.height)
                new_cells[new_pos].append(cell)
        return new_cells

    def iter_routes(self, route_length: int) -> list[list[P]]:
        routes: list[list[P]] = []
        todo: list[list[P]] = []

        routes.append([(0, 0)])
        todo.append([(0, 0)])

        # breakpoint()
        while len(routes[-1]) < route_length:
            new_todo: list[list[P]] = []
            for route in todo:
                last_pos = route[-1]
                for next_pos in self.get_neighbours(last_pos):
                    print(route + [next_pos])
                    routes.append(route + [next_pos])
                    new_todo.append(route + [next_pos])

                routes.append(route + [last_pos])
                new_todo.append(route + [last_pos])

            todo = new_todo

        retval: list[list[P]] = []
        for route in routes:
            if route[-1] == (self.height - 1, self.width - 1):
                retval.append(route)
        return retval

    def get_neighbours(self, current: P) -> list[P]:
        retval: list[P] = []

        if current[0] < self.height - 1:
            retval.append((current[0] + 1, current[1]))

        if current[1] < self.width - 1:
            retval.append((current[0], current[1] + 1))

        if current[1] > 0:
            retval.append((current[0], current[1] - 1))

        if current[0] > 0:
            retval.append((current[0] - 1, current[1]))

        return retval

    def solve(self, player: P, steps: int = 0, seen: Optional[list[P]] = None) -> Optional[int]:
        ### print("solve", player, steps, seen)

        if seen is None:
            seen = []

        if steps > 50:
            return None

        if player == (self.height - 1, self.width - 1):
            ### print("solution", seen)
            # breakpoint()
            return steps

        if player == (-1, 0):
            move_pos_list = [(0, 0)]
        else:
            move_pos_list = self.get_neighbours(player)

        new_cells = self.move_cells()

        steps_list: list[int] = []
        for new_player in move_pos_list:
            if len(new_cells[new_player]) == 0:  # and new_player not in seen:
                # move
                play = Play(grid=Grid(cells=new_cells, width=self.width, height=self.height))
                result = play.solve(
                    new_player,
                    steps + 1,
                    seen + [new_player],
                )
                if result is not None:
                    ### print(f"adding {result} to steps_list")
                    steps_list.append(result)

        # wait
        if player == (-1, 0) or len(new_cells[player]) == 0:
            play = Play(grid=Grid(cells=new_cells, width=self.width, height=self.height))
            result = play.solve(player, steps + 1, seen)
            if result is not None:
                steps_list.append(result)

        if not steps_list:
            ### print(f"no steps list for {player} seen={seen}")
            return None
        else:
            ### print("steps_list", steps_list)
            return min(steps_list)


def parse(lines: list[str]) -> Grid:
    dir_map = {
        "v": DOWN,
        "^": UP,
        "<": LEFT,
        ">": RIGHT,
    }

    cells: CELLS = {}

    width = 0
    for line_idx, line in enumerate(lines):
        if line_idx == 0:
            width = len(line) - 2
            assert line.startswith("#.#")
            continue
        if line.startswith("##"):
            break
        for cell_idx, c in enumerate(line[1:-1]):
            if c != ".":
                cells[(line_idx - 1, cell_idx)] = [dir_map[c]]

    assert width > 0
    height = len(lines) - 2
    assert height > 0
    return Grid(cells=cells, width=width, height=height)


def part01(grid: Grid):
    play = Play(grid)
    result = play.solve((-1, 0))
    if result is not None:
        return result + 1


def main():
    with open("aoc_24.txt") as infile:
        lines = [x.strip() for x in infile]

    grid = parse(lines)
    print(part01(grid))


@pytest.fixture
def sample() -> Grid:
    lines = [
        "#.######",
        "#>>.<^<#",
        "#.<..<<#",
        "#>v.><>#",
        "#<^v^^>#",
        "######.#",
    ]
    grid = parse(lines)
    return grid


def test_part01(sample: Grid):
    assert part01(sample) == 18


def test_iter_routes(sample: Grid):
    play = Play(sample)
    pprint(play.iter_routes(10))


if __name__ == "__main__":
    sys.exit(main())
