#!/usr/bin/env python3

from functools import lru_cache
import numpy as np
import time

EMPTY = 0
FLOOR = 1
TAKEN = 2

SIGN2INT = {"L": EMPTY, "#": TAKEN, ".": FLOOR}
INT2SIGN = ("L", ".", "#")

DTYPE = np.int64


class Time:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, *args, **kwargs):
        if 0:
            print(self.name, time.perf_counter() - self.start)


def parse_file(path: str):
    rows = []
    with open(path) as infile:
        for line in infile:
            rows.append([SIGN2INT[x] for x in line.rstrip()])

    return np.array(rows, dtype=DTYPE)


@lru_cache(maxsize=None)
def relative_to(shape, rowidx, colidx):
    rows = []
    cols = []
    for diff_row in (-1, 0, 1):
        for diff_col in (-1, 0, 1):
            if diff_row == 0 and diff_col == 0:
                continue

            row = rowidx + diff_row
            col = colidx + diff_col
            if row < 0 or row >= shape[0] or col < 0 or col >= shape[1]:
                continue
            rows.append(row)
            cols.append(col)

    return (np.array(rows, dtype=DTYPE), np.array(cols, dtype=DTYPE))


def adjacent_1(data: np.array, rowidx, colidx, min_cnt, max_cnt) -> np.array:
    rows, cols = relative_to(data.shape, rowidx, colidx)
    acells = data[rows, cols]
    return min_cnt < np.count_nonzero(acells == TAKEN) < max_cnt


def find_taken(data: np.array):
    for i in data:
        if i == TAKEN:
            return 1
        elif i == EMPTY:
            return 0
    return 0


def adjacent_2(data: np.array, rowidx, colidx, min_cnt, max_cnt) -> np.array:
    height, width = data.shape
    row = data[rowidx]
    retval = find_taken(row[colidx + 1 :])
    if retval > max_cnt:
        return False

    if colidx > 0:
        retval += find_taken(row[colidx - 1 :: -1])
        if retval > max_cnt:
            return False

    col = data[..., colidx]

    retval += find_taken(col[rowidx + 1 :])
    if retval > max_cnt:
        return False

    if rowidx > 0:
        retval += find_taken(col[rowidx - 1 :: -1])
        if retval > max_cnt:
            return False

    vec = ((-1, -1), (-1, 1), (1, -1), (1, 1))

    for row_diff, col_diff in vec:
        pos = [rowidx, colidx]
        while True:
            pos = [pos[0] + row_diff, pos[1] + col_diff]
            if pos[0] < 0 or pos[1] < 0 or pos[0] > height - 1 or pos[1] > width - 1:
                break
            cell = data[pos[0], pos[1]]
            if cell == TAKEN:
                retval += 1
                if retval > max_cnt:
                    return False
                break
            elif cell == EMPTY:
                break

    return min_cnt < retval < max_cnt


def print_data(data):
    for row in data:
        [INT2SIGN[x] for x in row]
        print("".join([INT2SIGN[x] for x in row]))


def step(data: np.array, retval: np.array, min_cnt: int, adjacent_fn):
    dirty = False
    with Time("step"):
        for rowidx, colidx in np.ndindex(data.shape):
            with Time("loop"):
                cell = data[rowidx, colidx]
                if cell == FLOOR:
                    new_cell = FLOOR
                else:
                    if cell == EMPTY and adjacent_fn(data, rowidx, colidx, min_cnt=-1, max_cnt=1):
                        new_cell = TAKEN
                        dirty = True
                    elif cell == TAKEN and adjacent_fn(data, rowidx, colidx, min_cnt=min_cnt, max_cnt=100):
                        new_cell = EMPTY
                        dirty = True
                    else:
                        new_cell = cell

                retval[rowidx, colidx] = new_cell

    return dirty


def solve(data, min_cnt, adjacent_fn):
    dirty = True

    new_data = np.zeros(data.shape, dtype=DTYPE)
    while dirty:
        dirty = step(data, new_data, min_cnt=min_cnt, adjacent_fn=adjacent_fn)
        if not dirty:
            break
        data, new_data = new_data, np.zeros(data.shape, dtype=DTYPE)

    cnt = np.count_nonzero(new_data == TAKEN)
    return cnt


def solve_1(data):
    return solve(data, 3, adjacent_1)


def solve_2(data):
    return solve(data, 4, adjacent_2)


def main():
    data = parse_file("aoc_11.txt")
    print("solve_1", solve_1(data))
    print("solve_2", solve_2(data))


if __name__ == "__main__":
    main()
