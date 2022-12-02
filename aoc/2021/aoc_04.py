#!/usr/bin/env python3

import sys
from typing import List, Optional
import numpy as np
from icecream import ic


class Board:
    def __init__(self, rows: List[List[int]] = []):
        self.data = np.array(rows)
        if self.data.shape[0] != self.data.shape[1]:
            raise ValueError(self.data)
        self.size = self.data.shape[0]

        self.row_draw = [set() for _ in range(self.size)]
        self.col_draw = [set() for _ in range(self.size)]
        self.drawn = set()
        self.is_winning = False

    def __repr__(self):
        return repr(self.data)

    def draw_number(self, number: int):
        if number not in self.drawn:
            for idx, row in enumerate(self.data):
                if number in row:
                    self.row_draw[idx].add(number)
                    self.drawn.add(number)

            for idx, col in enumerate(self.data.transpose()):
                if number in col:
                    self.col_draw[idx].add(number)
                    self.drawn.add(number)

            for drawn in self.row_draw:
                if len(drawn) == self.size:
                    self.is_winning = True
                    return

            for drawn in self.col_draw:
                if len(drawn) == self.size:
                    self.is_winning = True
                    return

    def get_sum_of_not_drawn(self) -> int:
        total = 0
        for row in self.data:
            for number in row:
                if number not in self.drawn:
                    total += number
        return total


def parse(lines: List[str]):
    numbers = [int(x) for x in lines[0].split(",")]

    boards: List[Board] = []
    rows = []
    for line in lines[2:]:
        if line == "":
            boards.append(Board(rows))
            rows = []
        else:
            rows.append([int(x) for x in line.split()])

    if rows:
        boards.append(Board(rows))

    return (numbers, boards)


def main():
    with open("aoc_04.txt") as infile:
        numbers, boards = parse([x.strip() for x in infile])

    last_board_winning: Optional[Board] = None
    last_number_winning: Optional[int] = None

    boards_won = []

    for number in numbers:
        for board in boards:
            if board not in boards_won:
                board.draw_number(number)
                if board.is_winning:
                    boards_won.append(board)
                    if last_board_winning is None:
                        print("first winning")
                        ic(board)
                        print(board.get_sum_of_not_drawn() * number)

                    last_number_winning = number
                    last_board_winning = board

    if last_board_winning is not None and last_number_winning is not None:
        print("last winning")
        ic(last_board_winning)
        ic(last_board_winning.get_sum_of_not_drawn())
        ic(last_number_winning)
        print(last_board_winning.get_sum_of_not_drawn() * last_number_winning)


if __name__ == "__main__":
    sys.exit(main())
