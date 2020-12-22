#!/usr/bin/env python3

from typing import *


def parse_file(path: str):
    retval = [[], []]
    player = 0
    with open(path) as infile:
        for line in infile:
            if line.startswith("Player"):
                continue

            if line == "\n":
                player += 1
            else:
                retval[player].append(int(line))

    assert len(retval[0]) == len(retval[1])
    return tuple(retval)


def play(decks: Tuple[List[int], List[int]]):
    while len(decks[0]) > 0 and len(decks[1]) > 0:
        # print(decks[0])
        # print(decks[1])
        if decks[0][0] > decks[1][0]:
            winner = 0
            loser = 1
        elif decks[1][0] > decks[0][0]:
            winner = 1
            loser = 0
        else:
            raise ValueError()

        decks[winner].append(decks[winner].pop(0))
        decks[winner].append(decks[loser].pop(0))

    if len(decks[0]) == 0:
        winner = decks[1]
    elif len(decks[1]) == 0:
        winner = decks[0]
    else:
        raise ValueError()

    return winner


rounds = 0
games = 0


def play_game(decks: Tuple[List[int], List[int]], game: int = 0):
    global rounds, games
    games += 1
    # print("new game with {} and {}".format(*decks))
    seen = [set(), set()]

    # print("play_round", decks[0], decks[1])
    while len(decks[0]) > 0 and len(decks[1]) > 0:
        rounds += 1
        if tuple(decks[0]) in seen[0] and tuple(decks[1]) in seen[1]:
            # print(game, "we seen this, player 1 wins")
            # if we seen this round, player 1 is the winner...
            return (0, decks)
        seen[0].add(tuple(decks[0]))
        seen[1].add(tuple(decks[1]))

        decks = (decks[0].copy(), decks[1].copy())

        if not decks[0]:
            return (1, decks)

        if not decks[1]:
            return (0, decks)

        top_0 = decks[0].pop(0)
        top_1 = decks[1].pop(0)

        players_top = [top_0, top_1]
        # print(game, "player 1 draws", top_0)
        # print(game, "player 2 draws", top_1)

        if len(decks[0]) >= top_0 and len(decks[1]) >= top_1:
            winner_id, _ = play_game((decks[0][:top_0], decks[1][:top_1],), game + 1)
            if winner_id == 1:
                loser_id = 0
            else:
                loser_id = 1
            # print(game, "subgame winner is", winner_id + 1)
        else:
            if top_0 > top_1:
                winner_id = 0
                loser_id = 1
            elif top_1 > top_0:
                winner_id = 1
                loser_id = 0
            else:
                raise ValueError()

        # print(game, "winner is player {}".format(winner_id + 1))

        decks[winner_id].append(players_top[winner_id])
        decks[winner_id].append(players_top[loser_id])

        # print(game, "winner's deck is", decks[winner_id])
        # print(game, "loser's deck is", decks[loser_id])

    return (winner_id, decks)


def calculate_score(deck):
    retval = 0
    for idx, value in enumerate(reversed(deck)):
        retval += (idx + 1) * value

    return retval


def solve_1(decks: Tuple[List[int], List[int]]):
    winner = play(decks)
    # print("winner", winner)
    score = calculate_score(winner)
    return score


def solve_2(decks: Tuple[List[int], List[int]]):
    winner_id, decks = play_game(decks)
    # print(decks[winner_id])
    return calculate_score(decks[winner_id])


def main():
    decks = parse_file("aoc_22.txt")

    print("solve_1", solve_1((decks[0].copy(), decks[1].copy())))
    print("solve_2", solve_2((decks[0].copy(), decks[1].copy())))
    print(rounds)
    print(games)


if __name__ == "__main__":
    main()
