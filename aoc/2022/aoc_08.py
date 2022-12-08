#!/usr/bin/env python3

import sys
import time

import numpy as np
import pytest
from numpy.typing import NDArray


def parse(lines: list[str]):
    rows = []
    for line in lines:
        rows.append([int(x) for x in line])

    return np.array(rows, dtype=np.int8)


def get_visible_tree_count(array: NDArray):
    retval = 0

    for cell in (it := np.nditer(array, flags=["multi_index"])):
        rowidx = it.multi_index[0]
        colidx = it.multi_index[1]
        if rowidx == 0 or colidx == 0 or rowidx == array.shape[0] - 1 or colidx == array.shape[1] - 1:
            retval += 1
            continue

        left = array[rowidx, :colidx].max()
        if left < cell:
            retval += 1
            continue

        right = array[rowidx, colidx + 1 :].max()
        if right < cell:
            retval += 1
            continue

        top = array[:rowidx, colidx].max()
        if top < cell:
            retval += 1
            continue

        bottom = array[rowidx + 1 :, colidx].max()
        if bottom < cell:
            retval += 1
            continue

    return retval


def get_max_scenic_score(array: NDArray):
    retval = 0

    for cell in (it := np.nditer(array, flags=["multi_index"])):
        rowidx = it.multi_index[0]
        colidx = it.multi_index[1]
        if rowidx == 0 or colidx == 0 or rowidx == array.shape[0] - 1 or colidx == array.shape[1] - 1:
            continue

        left_cnt = 0
        for n in np.flip(array[rowidx, :colidx]):
            left_cnt += 1
            if n >= cell:
                break

        right_cnt = 0
        for n in array[rowidx, colidx + 1 :]:
            right_cnt += 1
            if n >= cell:
                break

        top_cnt = 0
        for n in np.flip(array[:rowidx, colidx]):
            top_cnt += 1
            if n >= cell:
                break

        bottom_cnt = 0
        for n in array[rowidx + 1 :, colidx]:
            bottom_cnt += 1
            if n >= cell:
                break

        score = top_cnt * bottom_cnt * right_cnt * left_cnt
        if score > retval:
            retval = score

    return retval


def part01(arr: NDArray):
    return get_visible_tree_count(arr)


def part02(arr: NDArray):
    return get_max_scenic_score(arr)


def main():
    with open("aoc_08.txt") as infile:
        lines = [x.strip() for x in infile]
    arr = parse(lines)
    print(part01(arr))
    print(part02(arr))


@pytest.fixture
def sample():
    return np.array(
        [
            [3, 0, 3, 7, 3],
            [2, 5, 5, 1, 2],
            [6, 5, 3, 3, 2],
            [3, 3, 5, 4, 9],
            [3, 5, 3, 9, 0],
        ]
    )


def test_part02(sample: NDArray):
    assert part02(sample) == 8


def test_part01(sample: NDArray):
    assert part01(sample) == 21


def test_parse(sample: NDArray):
    lines = [
        "30373",
        "25512",
        "65332",
        "33549",
        "35390",
    ]
    parse(lines) == sample


if __name__ == "__main__":
    main()
