#!/usr/bin/env python3

import re
import sys
from dataclasses import dataclass
from functools import cache, cached_property

import pytest


@dataclass
class Card:
    idx: int
    winning: set[int]
    own: set[int]

    @cached_property
    def score(self) -> int:
        retval = 0
        result = len(self.own.intersection(self.winning))
        if result > 0:
            retval = 2 ** (result - 1)
        return retval

    @cached_property
    def score2(self) -> int:
        result = len(self.own.intersection(self.winning))
        return result


@dataclass(frozen=True)
class CardScore:
    idx: int
    score: int


@cache
def get_recursive_score(cards: tuple[CardScore, ...], card: CardScore) -> int:
    if card.score > 0:
        retval = card.score
        for card in cards[card.idx + 1 : card.idx + 1 + card.score]:
            retval += get_recursive_score(cards, card)
        return retval
    else:
        return 0


def parse_lines(lines: list[str]) -> list[Card]:
    retval: list[Card] = []
    for idx, line in enumerate(lines):
        if m := re.match(r"Card +\d+: ([\d\s]+)\|([\d\s]+)", line):
            winning = set(map(int, m.group(1).strip().split()))
            own = set(map(int, m.group(2).strip().split()))
            retval.append(Card(idx=idx, winning=winning, own=own))
        else:
            raise ValueError(line)
    return retval


def part_01(cards: list[Card]) -> int:
    retval = 0
    for card in cards:
        retval += card.score
    return retval


def part_02(cards: list[Card]) -> int:
    cards_score = tuple([CardScore(idx, card.score2) for idx, card in enumerate(cards)])
    retval = 0

    for card in cards_score:
        result = get_recursive_score(cards_score, card)
        retval += result

    return retval + len(cards)


def main():
    with open("aoc_04.txt") as infile:
        lines = [line.strip() for line in infile]

    cards = parse_lines(lines)
    print(part_01(cards))
    print(part_02(cards))


@pytest.fixture()
def cards() -> list[Card]:
    return [
        Card(idx=0, winning={41, 48, 17, 83, 86}, own={6, 9, 48, 17, 83, 53, 86, 31}),
        Card(idx=1, winning={32, 13, 16, 20, 61}, own={32, 68, 17, 82, 19, 24, 61, 30}),
        Card(idx=2, winning={1, 44, 53, 21, 59}, own={1, 69, 72, 14, 16, 82, 21, 63}),
        Card(idx=3, winning={69, 73, 41, 84, 92}, own={5, 76, 51, 84, 83, 54, 58, 59}),
        Card(idx=4, winning={32, 83, 87, 26, 28}, own={36, 70, 12, 82, 22, 88, 93, 30}),
        Card(idx=5, winning={72, 13, 18, 56, 31}, own={35, 67, 36, 74, 10, 11, 77, 23}),
    ]


def test_parse(cards: list[Card]):
    lines = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]

    assert parse_lines(lines) == cards


def test_part01(cards: list[Card]):
    assert part_01(cards) == 13


def test_part02(cards: list[Card]):
    assert part_02(cards) == 30


if __name__ == "__main__":
    sys.exit(main())
