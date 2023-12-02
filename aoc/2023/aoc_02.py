#!/usr/bin/env python3

import re
import sys
from dataclasses import dataclass

import pytest


@dataclass
class Pull:
    red: int = 0
    green: int = 0
    blue: int = 0

    def any(self) -> bool:
        return self.red > 0 or self.green > 0 or self.blue > 0

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue


@dataclass
class Game:
    pulls: list[Pull]


def parse_line(line: str):
    pulls: list[Pull] = []

    pull = Pull()

    for token in re.split(r"([,;])\s*", line.split(": ", 1)[1]):
        if token == ";":
            pulls.append(pull)
            pull = Pull()
        elif token == ",":
            continue
        else:
            amount_s, color = token.split(" ")
            amount = int(amount_s)
            if color == "blue":
                pull.blue = amount
            elif color == "green":
                pull.green = amount
            elif color == "red":
                pull.red = amount
            else:
                raise ValueError(color)

    if pull.any():
        pulls.append(pull)

    return Game(pulls=pulls)


def parse_lines(lines: list[str]) -> list[Game]:
    retval: list[Game] = []
    for line in lines:
        retval.append(parse_line(line))
    return retval


def part_01(games: list[Game]) -> int:
    # 12 red cubes, 13 green cubes, and 14 blue cubes
    bag = Pull(12, 13, 14)

    valid_games: list[int] = []

    for idx, game in enumerate(games):
        for pull in game.pulls:
            if pull.red > bag.red or pull.green > bag.green or pull.blue > bag.blue:
                break
        else:
            valid_games.append(idx + 1)

    return sum(valid_games)


def part_02(games: list[Game]) -> int:
    powers: list[int] = []

    for game in games:
        bag = Pull()
        for pull in game.pulls:
            if pull.red > bag.red:
                bag.red = pull.red

            if pull.green > bag.green:
                bag.green = pull.green

            if pull.blue > bag.blue:
                bag.blue = pull.blue
        powers.append(bag.power)

    return sum(powers)


def main():
    with open("aoc_02.txt") as infile:
        lines = [x.strip() for x in infile]

    games = parse_lines(lines)
    print(part_01(games))
    print(part_02(games))


@pytest.fixture()
def input_task() -> list[Game]:
    return [
        Game([Pull(4, 0, 3), Pull(1, 2, 6), Pull(0, 2, 0)]),
        Game([Pull(0, 2, 1), Pull(1, 3, 4), Pull(0, 1, 1)]),
        Game([Pull(20, 8, 6), Pull(4, 13, 5), Pull(1, 5, 0)]),
        Game([Pull(3, 1, 6), Pull(6, 3, 0), Pull(14, 3, 15)]),
        Game([Pull(6, 3, 1), Pull(1, 2, 2)]),
    ]


def test_parse(input_task: list[Game]):
    lines = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]

    assert parse_lines(lines) == input_task


def test_part01(input_task: list[Game]):
    assert part_01(input_task) == 8


def test_part02(input_task: list[Game]):
    assert part_02(input_task) == 2286


if __name__ == "__main__":
    sys.exit(main())
