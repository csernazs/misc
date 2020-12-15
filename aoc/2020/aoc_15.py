#!/usr/bin/env python3

from collections import defaultdict


def solve(data, max_turn):
    numbers = defaultdict(list)
    last = None
    for turn, number in enumerate(data):
        numbers[number].append(turn)
        last = number

    for turn in range(len(data), max_turn):
        # if turn % 1000000 == 0:
        #     print(max_turn - turn, last)
        last_turns = numbers[last]
        if len(last_turns) >= 2:
            next = last_turns[-1] - last_turns[-2]
        else:
            next = 0
        numbers[next].append(turn)
        last = next

    return last


def main():
    data = (13, 0, 10, 12, 1, 5, 8)
    print("solve_1", solve(data, max_turn=2020))
    print("solve_2", solve(data, max_turn=30000000))


if __name__ == "__main__":
    main()
