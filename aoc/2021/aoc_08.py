#!/usr/bin/env python3

import sys
from icecream import ic
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

ic.disable()

@dataclass
class Display:
    value: List[str]
    patterns: List[Set[str]]

    def get_patterns_by_length(self, length: int) -> List[Set[str]]:
        retval = []
        for pattern in self.patterns:
            if len(pattern) == length:
                retval.append(pattern)
        return retval

    def get_pattern_by_length(self, length: int) -> Set[str]:
        patterns = self.get_patterns_by_length(length)
        assert len(patterns) == 1
        return patterns[0]


class PatternMap:
    def __init__(self, data=List[Tuple[Set[str], int]]):
        self.data = data

    def __getitem__(self, key: Set[str]):
        for k, value in self.data:
            if k == key:
                return value

    @classmethod
    def from_known(cls, known=Dict[int, Set[str]]):
        data = []
        for digit, pattern_set in known.items():
            data.append((pattern_set, digit))

        return cls(data)


def match(pattern_list=List[Set[str]], pattern=Set[str]) -> List[Set[str]]:
    retval = []
    for p in pattern_list:
        if p & pattern == pattern:
            retval.append(p)
    return retval


def match_one(patterns=List[Set[str]], pattern=Set[str]) -> Set[str]:
    matches = match(patterns, pattern)
    assert len(matches) == 1, matches
    return matches[0]


def parse(lines) -> List[Display]:
    displays: List[Display] = []
    for line in lines:
        patterns, value = line.split(" | ")
        patterns_list = [set(x) for x in patterns.split(" ")]
        value_list = [set(x) for x in value.split(" ")]
        displays.append(Display(value=value_list, patterns=patterns_list))

    return displays


def compute(disp: Display) -> PatternMap:
    known = {}
    known[1] = disp.get_pattern_by_length(2)
    known[7] = disp.get_pattern_by_length(3)
    # segment_map["a"] = (known[7] - known[1]).pop()
    # ic(segment_map)

    known[4] = disp.get_pattern_by_length(4)
    known[8] = disp.get_pattern_by_length(7)

    known[3] = match_one(disp.get_patterns_by_length(5), known[1])

    d_nine_candidates = [x for x in match(disp.patterns, known[4].union(known[7])) if x != known[8]]
    assert len(d_nine_candidates) == 1
    known[9] = d_nine_candidates[0]

    d_zero_candidates = [x for x in match(disp.get_patterns_by_length(6), known[7]) if x != known[9]]
    assert len(d_zero_candidates) == 1
    known[0] = d_zero_candidates[0]

    d_six_candidates = [x for x in disp.get_patterns_by_length(6) if x not in (known[9], known[0])]
    assert len(d_six_candidates) == 1
    known[6] = d_six_candidates[0]

    known[5] = known[6] - (known[8] - known[9])
    known[2] = [x for x in disp.patterns if x not in known.values()][0]

    return PatternMap.from_known(known)


def solve_1(displays: List[Display]):
    cnt = 0
    for disp in displays:
        cnt += len([x for x in disp.value if len(x) in (2, 4, 3, 7)])
    print(cnt)


def solve_2(displays: List[Display]):

    """
    known: 0, 1, 3, 4, 6, 7, 8, 9
    2, 5

      0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....

      5:      6:      7:      8:      9:
     aaaa    aaaa    aaaa    aaaa    aaaa
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
     dddd    dddd    ....    dddd    dddd
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
     gggg    gggg    ....    gggg    gggg
    """

    s = 0
    for disp in displays:
        ic(disp.patterns)
        ic(disp.value)
        pm = compute(disp)
        ic(pm.data)

        result = (
            pm[disp.value[0]] * 1000 + pm[disp.value[1]] * 100 + pm[disp.value[2]] * 10 + pm[disp.value[3]]
        )
        ic(result)
        s += result

    print(s)


def main():
    with open("aoc_08.txt") as infile:
        displays = parse([x.strip() for x in infile.readlines()])

    solve_1(displays)
    solve_2(displays)


if __name__ == "__main__":
    sys.exit(main())
