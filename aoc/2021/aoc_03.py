#!/usr/bin/env python3

import sys
from typing import Optional, List
from icecream import ic

def solve_1(rows: List[str]):
    for line in rows:
        line = line.strip()
        if columns is None:
            columns = [[c] for c in line]
        else:
            for idx, c in enumerate(line):
                columns[idx].append(c)

    if columns is None:
        return 1

    most_common_bits = []
    for column in columns:
        if column.count("1") > column.count("0"):
            most_common_bits.append("1")
        else:
            most_common_bits.append("0")

    print(most_common_bits)
    least_common_bits = ["0" if x == "1" else "1" for x in most_common_bits]
    print(least_common_bits)

    most_common = int("".join(most_common_bits), base=2)
    least_common = int("".join(least_common_bits), base=2)

    print(most_common, least_common)
    print("sol1", most_common * least_common)


def get_most_common_bit(rows: List[str], pos: int):
    cnt_1 = 0
    cnt_0 = 0
    for row in rows:
        if row[pos] == "0":
            cnt_0 += 1
        elif row[pos] == "1":
            cnt_1 += 1
        else:
            raise ValueError(row[pos])

    if cnt_1 >= cnt_0:
        return "1"
    else:
        return "0"

def get_least_common_bit(rows: List[str], pos: int):
    cnt_1 = 0
    cnt_0 = 0
    for row in rows:
        if row[pos] == "0":
            cnt_0 += 1
        elif row[pos] == "1":
            cnt_1 += 1
        else:
            raise ValueError(row[pos])

    if cnt_1 < cnt_0:
        return "1"
    else:
        return "0"


def filter_prefix(rows: List[str], prefix: str):
    retval = []
    for row in rows:
        if not prefix or row.startswith(prefix):
            retval.append(row)
    return retval


def get_rating(rows: List[str], callable):
    prefix = ""
    pos = 0
    found = None

    while True:
        filtered = filter_prefix(rows, prefix)
        if len(filtered) == 1:
            found = filtered[0]
            break
        elif not filtered:
            raise ValueError(rows, prefix)
        else:
            rows = filtered
            prefix += callable(filtered, pos)
            pos += 1
            ic(prefix)

    ic(found)
    return found


def solve_2(rows: List[str]):
    most_common_found = ic(get_rating(rows, get_most_common_bit))
    least_common_found = ic(get_rating(rows, get_least_common_bit))

    print(int(most_common_found, 2) * int(least_common_found, 2))

def main():
    # ic.disable()

    columns: Optional[List[List[str]]] = None

    rows: List[str] = []

    with open("aoc_03.txt") as infile:
        rows = [x.strip() for x in infile]

    # solve_1(rows)
    solve_2(rows)


if __name__ == "__main__":
    sys.exit(main())
