#!/usr/bin/env python3
# pylint: disable=all

from collections import deque
import itertools
from typing import List
import sys

try:
    infile = open(sys.argv[1], "r")
except IndexError:
    infile = sys.stdin

try:
    outfile = open(sys.argv[2], "w")
except IndexError:
    outfile = sys.stdout


def read_int(f):
    return int(f.readline())


def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))


def read_lines(f, no_lines):
    retval = []
    for i in range(no_lines):
        retval.append(f.readline().rstrip())
    return retval


def find_starts(words: List[str], start: str):
    retval = []
    for word in words:
        if word.startswith(start):
            retval.append(word)
    return retval


def find_ends(words: List[str], end: str):
    retval = []
    for word in words:
        if word.endswith(end):
            retval.append(word)
    return retval


def is_valid_word(word: str):
    state = {}
    for idx, char in enumerate(word):
        if char not in state:
            state[char] = idx
        else:
            if state[char] != idx - 1:
                return False
            state[char] = idx

    return True

def solve_tower(tower: deque, words: List[str]):
    ## print(f"{tower=}")
    ## print(f"{words=}")
    candidates = find_starts(words, tower[-1][-1])
    ## print(f"starts {candidates=}")
    for candidate in candidates:
        new_tower = tower.copy()
        new_tower.append(candidate)
        new_words = words.copy()
        new_words.remove(candidate)
        if not new_words:
            return new_tower

        return solve_tower(new_tower, new_words)

    candidates = find_ends(words, tower[0][0])
    ## print(f"ends {candidates=}")
    for candidate in candidates:
        new_tower = tower.copy()
        new_tower.appendleft(candidate)
        new_words = words.copy()
        new_words.remove(candidate)
        if not new_words:
            return new_tower
        return solve_tower(new_tower, new_words)

    ## print(f"remaining {words=}")
    for candidate in words:
        new_tower = tower.copy()
        new_tower.append(candidate)
        new_words = words.copy()
        new_words.remove(candidate)
        if not new_words:
            return new_tower
        return solve_tower(new_tower, new_words)


def solve(words: List[str]) -> str:
    for word in words:
        if not is_valid_word(word):
            return "IMPOSSIBLE"

    tower = deque([words.pop(0)])

    retval = solve_tower(tower, words)
    retval_s = "".join(retval)
    if is_valid_word(retval_s):
        return retval_s
    else:
        return "IMPOSSIBLE"

def solve2(words: List[str]) -> str:
    for word in words:
        if not is_valid_word(word):
            return "IMPOSSIBLE"

    for perm in itertools.permutations(words):
        candidate = "".join(perm)
        if is_valid_word(candidate):
            return candidate

    return "IMPOSSIBLE"

def main():
    no_cases = read_int(infile)

    for case_idx in range(no_cases):
        no_words = read_int(infile)
        word_list = infile.readline().strip().split()
        assert len(word_list) == no_words
        solution = solve2(word_list)
        outfile.write("Case #%d: %s\n" % (case_idx + 1, solution))

if __name__ == "__main__":
    main()
