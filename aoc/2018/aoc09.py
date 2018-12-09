#!/usr/bin/python3

from __future__ import print_function
from collections import deque


def print_circle(circle):
    idx = circle.index(0)
    circle.rotate(0 - idx)
    print("circle", " ".join(map(str, circle)))
    circle.rotate(idx)


def solve_a(no_players, marbles):
    circle = deque([0])
    player = 0
    score = [0 for _ in range(no_players)]

    for marble in range(1, marbles + 1):
        if marble % 100000 == 0:
            print("marble", marble)
        # print("current_marble", circle[0])
        # print("current_player", player)
        if marble % 23 == 0:
            #            import pdb; pdb.set_trace()
            score[player] += marble
            circle.rotate(7)
            additional = circle.popleft()
            score[player] += additional
            # print("mod23", marble, additional)
            # circle.rotate(0)
        else:
            circle.rotate(-2)
            circle.insert(0, marble)

        # print_circle(circle)

        player = player + 1
        if player >= no_players:
            player = 0

    # print(score)
    # print(max(score))

    return max(score)


def main():
    no_players = 10
    no_marbles = 1618

    #    no_players = 9
    #    no_marbles = 25

    no_players, no_marbles = 30, 5807
    no_players, no_marbles = 458, 71307

    no_marbles = no_marbles * 100
    print("solution", solve_a(no_players, no_marbles))


if __name__ == "__main__":
    main()
