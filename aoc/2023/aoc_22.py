#!/usr/bin/env python3

import sys
from dataclasses import dataclass, field
from typing import Iterable

import pytest

POS = tuple[int, int, int]

STATE = dict[POS, "Brick"]


@dataclass
class Brick:
    cubes: list[POS]
    top: list[POS] = field(init=False)
    bottom: list[POS] = field(init=False)

    def __post_init__(self):
        self.top = self.get_top()
        self.bottom = self.get_bottom()

    def get_top(self) -> list[POS]:
        top_cubes: list[POS] = [self.cubes[0]]
        for cube in self.cubes[1:]:
            if cube[2] > top_cubes[0][2]:
                top_cubes = [cube]
            elif cube[2] == top_cubes[0][2]:
                top_cubes.append(cube)

        return top_cubes

    def get_bottom(self) -> list[POS]:
        bottom_cubes: list[POS] = [self.cubes[0]]
        for cube in self.cubes[1:]:
            if cube[2] < bottom_cubes[0][2]:
                bottom_cubes = [cube]
            elif cube[2] == bottom_cubes[0][2]:
                bottom_cubes.append(cube)

        return bottom_cubes

    def refresh(self):
        self.bottom = self.get_bottom()
        self.top = self.get_top()

    @property
    def bottom_z(self) -> int:
        return self.bottom[0][2]

    def move_down(self):
        self.cubes = [(x, y, z - 1) for x, y, z in self.cubes]
        self.refresh()

    def can_move_down(self, state: STATE, exclude: "Brick|None" = None) -> bool:
        if self.bottom_z == 1:
            return False

        for x, y, z in self.bottom:
            new_pos: POS = (x, y, z - 1)
            brick: Brick | None = state.get(new_pos)
            if brick is not None and brick != exclude:
                return False
        return True

    def can_be_removed(self, state: STATE) -> bool:
        for x, y, z in self.top:
            new_pos: POS = (x, y, z + 1)
            top_brick: Brick | None = state.get(new_pos)
            if top_brick is not None:
                if top_brick.can_move_down(state, exclude=self):
                    return False
        return True

    def supports(self, state: STATE) -> list["Brick"]:
        retval: list[Brick] = []
        for x, y, z in self.top:
            new_pos: POS = (x, y, z + 1)
            top_brick: Brick | None = state.get(new_pos)
            if top_brick is not None:
                if top_brick.can_move_down(state, exclude=self):
                    retval.append(top_brick)
        return retval


def get_all(bricks: list[Brick]) -> dict[POS, Brick]:
    retval: dict[POS, Brick] = {}
    for brick in bricks:
        for cube in brick.cubes:
            retval[cube] = brick

    return retval


def move_all_down(bricks: list[Brick]) -> list[Brick]:
    retval: list[Brick] = []
    state: dict[POS, Brick] = get_all(bricks)
    for brick in bricks:
        if brick.can_move_down(state):
            brick.move_down()
            retval.append(brick)
    return retval


def iter_pos(left: POS, right: POS):
    assert right[0] >= left[0] and right[1] >= left[1] and right[2] >= left[2]
    for x in range(left[0], right[0] + 1):
        for y in range(left[1], right[1] + 1):
            for z in range(left[2], right[2] + 1):
                yield (x, y, z)


def parse_lines(lines: Iterable[str]) -> list[Brick]:
    bricks: list[Brick] = []
    for line in lines:
        left, right = line.split("~")
        left_pos = tuple([int(x) for x in left.split(",")])
        right_pos = tuple([int(x) for x in right.split(",")])
        assert len(left_pos) == 3
        assert len(right_pos) == 3
        cubes = list(iter_pos(left_pos, right_pos))
        bricks.append(Brick(cubes))

    bricks.sort(key=lambda x: x.bottom_z)
    return bricks


def part_01(bricks: list[Brick]) -> int:
    state = get_all(bricks)
    cnt = 0
    for brick in bricks:
        if brick.can_be_removed(state):
            cnt += 1
    return cnt


def remove_brick(state: dict[POS, Brick], brick: Brick) -> bool:
    for cube in brick.cubes:
        try:
            del state[cube]
        except KeyError:
            return False
    return True


def would_fallen(brick: Brick, state: dict[POS, Brick]) -> int:
    supported_bricks = brick.supports(state)
    if not remove_brick(state, brick):
        return 0

    cnt = 1

    for supported in supported_bricks:
        if supported.can_move_down(state):
            cnt += would_fallen(supported, state)
    return cnt


def part_02(bricks: list[Brick]) -> int:
    cnt = 0
    orig_state = get_all(bricks)

    for brick in bricks:
        state = orig_state.copy()
        cnt += would_fallen(brick, state) - 1
    return cnt


def main():
    with open("aoc_22.txt") as infile:
        lines = [line.strip() for line in infile]

    bricks = parse_lines(lines)

    while move_all_down(bricks):
        pass

    print(part_01(bricks))
    print(part_02(bricks))


@pytest.fixture(name="bricks")
def fixture_bricks():
    return [
        Brick([(1, 0, 1), (1, 1, 1), (1, 2, 1)]),
        Brick([(0, 0, 2), (1, 0, 2), (2, 0, 2)]),
        Brick([(0, 2, 3), (1, 2, 3), (2, 2, 3)]),
        Brick([(0, 0, 4), (0, 1, 4), (0, 2, 4)]),
        Brick([(2, 0, 5), (2, 1, 5), (2, 2, 5)]),
        Brick([(0, 1, 6), (1, 1, 6), (2, 1, 6)]),
        Brick([(1, 1, 8), (1, 1, 9)]),
    ]


def test_parse(bricks: list[Brick]):
    lines = [
        "1,0,1~1,2,1",
        "0,0,2~2,0,2",
        "0,2,3~2,2,3",
        "0,0,4~0,2,4",
        "2,0,5~2,2,5",
        "0,1,6~2,1,6",
        "1,1,8~1,1,9",
    ]
    assert parse_lines(lines) == bricks


def test_part_01(bricks: list[Brick]):
    while True:
        moved_bricks = move_all_down(bricks)
        if len(moved_bricks) == 0:
            break

    assert part_01(bricks) == 5


def test_part_02(bricks: list[Brick]):
    while True:
        moved_bricks = move_all_down(bricks)
        if len(moved_bricks) == 0:
            break

    assert part_02(bricks) == 7


if __name__ == "__main__":
    sys.exit(main())
