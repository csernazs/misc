#!/usr/bin/env python3

import sys
from collections import Counter
from dataclasses import dataclass
from typing import Any, TypeVar

import pytest

CARD_VALUES_1 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

JOKER = 1

CARD_VALUES_2 = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": JOKER,
}


@dataclass
class Hand1:
    cards: tuple[int, int, int, int, int]

    def get_type(self) -> int:
        counter = Counter(self.cards)
        most_common = counter.most_common()
        if len(most_common) == 1:
            return 7  # five of a kind
        if len(most_common) == 2 and most_common[0][1] == 4:
            return 6  # four of a kind
        if len(most_common) == 2 and most_common[0][1] == 3 and most_common[1][1] == 2:
            return 5  # full house
        if len(most_common) == 3 and most_common[0][1] == 3:
            return 4  # three of a kind
        if len(most_common) == 3 and most_common[0][1] == 2 and most_common[1][1] == 2:
            return 3  # two pair
        if len(most_common) == 4 and most_common[0][1] == 2:
            return 2  # one pair
        if len(most_common) == 5:
            return 1  # high card
        raise ValueError(counter)

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Hand1):
            return NotImplemented
        self_type = self.get_type()
        other_type = other.get_type()
        if self_type > other_type:
            return True
        elif self_type < other_type:
            return False
        else:
            return self.cards > other.cards

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Hand1):
            return NotImplemented
        self_type = self.get_type()
        other_type = other.get_type()
        if self_type < other_type:
            return True
        elif self_type > other_type:
            return False
        else:
            return self.cards < other.cards

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Hand1):
            return NotImplemented
        return self.cards == other.cards


@dataclass
class Hand2:
    cards: tuple[int, int, int, int, int]

    def get_type(self) -> int:
        counter = Counter(self.cards)
        j = counter[JOKER]

        most_common = counter.most_common()
        if len(most_common) == 1:
            return 7  # five of a kind

        if len(most_common) == 2 and most_common[0][1] == 4:
            if j == 1 or j == 4:
                return 7  # five of a kind with joker
            else:
                return 6  # four of a kind

        if len(most_common) == 2 and most_common[0][1] == 3 and most_common[1][1] == 2:
            if j == 3 or j == 2:
                return 7  # five of a kind with joker
            else:
                return 5  # full house

        if len(most_common) == 3 and most_common[0][1] == 3:
            if j == 1 or j == 3:
                return 6  # four of a kind with joker
            return 4  # three of a kind
        if len(most_common) == 3 and most_common[0][1] == 2 and most_common[1][1] == 2:
            if j == 1:
                return 5  # full house with joker
            if j == 2:
                return 6  # four of a kind with joker
            return 3  # two pair
        if len(most_common) == 4 and most_common[0][1] == 2:
            if j == 1 or j == 2:
                return 4  # three of a kind with joker
            else:
                return 2  # one pair
        if len(most_common) == 5:
            if j == 1:
                return 2  # one pair with joker
            return 1  # high card
        raise ValueError(counter)

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Hand2):
            return NotImplemented
        self_type = self.get_type()
        other_type = other.get_type()
        if self_type > other_type:
            return True
        elif self_type < other_type:
            return False
        else:
            return self.cards > other.cards

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Hand2):
            return NotImplemented
        self_type = self.get_type()
        other_type = other.get_type()
        if self_type < other_type:
            return True
        elif self_type > other_type:
            return False
        else:
            return self.cards < other.cards

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Hand2):
            return NotImplemented
        return self.cards == other.cards


T = TypeVar("T", Hand1, Hand2)


def parse_lines(lines: list[str], card_values: dict[str, int], target: type[T]) -> list[tuple[T, int]]:
    retval: list[tuple[T, int]] = []

    for line in lines:
        cards_s, bid_s = line.split(" ")
        assert len(cards_s) == 5
        bid = int(bid_s)
        cards = [card_values[card] for card in cards_s]
        retval.append((target((cards[0], cards[1], cards[2], cards[3], cards[4])), bid))
    return retval


def solve(bids: list[tuple[Hand1, int]] | list[tuple[Hand2, int]]):
    sorted_bids = sorted(bids, key=lambda x: x[0])
    retval = 0

    for idx, (hand, bid_value) in enumerate(sorted_bids):
        # print(hand, bid_value)
        retval += (idx + 1) * bid_value
    return retval


@pytest.fixture()
def bids_1() -> list[tuple[Hand1, int]]:
    return [
        (Hand1(cards=(3, 2, 10, 3, 13)), 765),
        (Hand1(cards=(10, 5, 5, 11, 5)), 684),
        (Hand1(cards=(13, 13, 6, 7, 7)), 28),
        (Hand1(cards=(13, 10, 11, 11, 10)), 220),
        (Hand1(cards=(12, 12, 12, 11, 14)), 483),
    ]


@pytest.fixture()
def bids_2() -> list[tuple[Hand2, int]]:
    return [
        (Hand2(cards=(3, 2, 10, 3, 12)), 765),
        (Hand2(cards=(10, 5, 5, 1, 5)), 684),
        (Hand2(cards=(12, 12, 6, 7, 7)), 28),
        (Hand2(cards=(12, 10, 1, 1, 10)), 220),
        (Hand2(cards=(11, 11, 11, 1, 13)), 483),
    ]


def test_parse(bids_1: list[tuple[Hand1, int]], bids_2: list[tuple[Hand2, int]]):
    lines = [
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
    ]
    assert parse_lines(lines, CARD_VALUES_1, Hand1) == bids_1
    assert parse_lines(lines, CARD_VALUES_2, Hand2) == bids_2


def test_get_type_1():
    assert Hand1((2, 2, 2, 2, 2)).get_type() == 7
    assert Hand1((2, 2, 2, 2, 3)).get_type() == 6
    assert Hand1((3, 2, 2, 2, 2)).get_type() == 6

    assert Hand1((3, 3, 2, 2, 2)).get_type() == 5
    assert Hand1((2, 2, 2, 3, 3)).get_type() == 5

    assert Hand1((3, 4, 2, 2, 2)).get_type() == 4
    assert Hand1((2, 2, 2, 4, 3)).get_type() == 4

    assert Hand1((3, 4, 3, 4, 2)).get_type() == 3
    assert Hand1((4, 3, 4, 3, 5)).get_type() == 3

    assert Hand1((4, 4, 3, 5, 6)).get_type() == 2
    assert Hand1((2, 3, 4, 5, 5)).get_type() == 2

    assert Hand1((2, 3, 4, 5, 6)).get_type() == 1
    assert Hand1((7, 8, 9, 10, 11)).get_type() == 1


def test_get_type_2():
    assert Hand2(cards=(3, 2, 10, 3, 12)).get_type() == 2
    assert Hand2(cards=(12, 12, 6, 7, 7)).get_type() == 3
    assert Hand2(cards=(12, 10, 1, 1, 10)).get_type() == 6
    assert Hand2(cards=(10, 5, 5, 1, 5)).get_type() == 6
    assert Hand2(cards=(11, 11, 11, 1, 13)).get_type() == 6


def test_comparison_1():
    assert Hand1((2, 3, 4, 5, 6)) < Hand1((7, 8, 9, 10, 11))
    assert Hand1((7, 8, 9, 10, 11)) > Hand1((2, 3, 4, 5, 6))
    assert Hand1((12, 12, 12, 11, 14)) > Hand1((13, 10, 11, 11, 10))

    assert not Hand1((2, 3, 4, 5, 6)) > Hand1((7, 8, 9, 10, 11))
    assert not Hand1((7, 8, 9, 10, 11)) < Hand1((2, 3, 4, 5, 6))
    assert not Hand1((12, 12, 12, 11, 14)) < Hand1((13, 10, 11, 11, 10))


def test_part01(bids_1: list[tuple[Hand1, int]]):
    assert solve(bids_1) == 6440


def test_part02(bids_2: list[tuple[Hand1, int]]):
    assert solve(bids_2) == 5905


def main():
    with open("aoc_07.txt") as infile:
        lines = [line.strip() for line in infile]

    bids = parse_lines(lines, CARD_VALUES_1, Hand1)
    print(solve(bids))

    bids = parse_lines(lines, CARD_VALUES_2, Hand2)
    print(solve(bids))


if __name__ == "__main__":
    sys.exit(main())
