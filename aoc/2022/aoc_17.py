from itertools import cycle
from typing import Iterable, Optional
from numpy.typing import NDArray
import numpy as np

from dataclasses import dataclass
import sys


@dataclass
class P:
    x: int
    y: int


PLIST = list[P]


class Shape:
    def __init__(self, points: PLIST):
        self.points = points
        self.width: int = max(points, key=lambda p: p.x).x + 1
        self.height: int = max(points, key=lambda p: p.y).y + 1

    def can_be_placed(self, offset: P, matrix: NDArray):
        if (
            offset.x < 0
            or offset.y < 0
            or offset.x + self.width + 1 > matrix.shape[1]
            or offset.y + self.height + 1 > matrix.shape[0]
        ):
            return False

        for pos in self.points:
            if matrix[(pos.y + offset.y, pos.x + offset.x)] == 1:
                return False

        return True

    def set(self, offset: P, matrix: NDArray, value: int):
        for pos in self.points:
            matrix[(pos.y + offset.y, pos.x + offset.x)] = value

    def place(self, offset: P, matrix: NDArray) -> bool:
        if self.can_be_placed(offset, matrix):
            self.set(offset, matrix, 1)
            return True
        else:
            return False

    def move(self, orig_pos: P, new_pos: P, matrix: NDArray) -> bool:
        # remove
        self.set(orig_pos, matrix, 0)
        print("AFTER REMOVE")
        print_matrix(matrix)

        if self.can_be_placed(new_pos, matrix):
            # place
            self.set(new_pos, matrix, 1)
            print("AFTER MOVE")
            print_matrix(matrix)
            return True
        else:
            # restore
            self.set(orig_pos, matrix, 1)
            return False

    def move_left(self, orig_pos: P, matrix: NDArray) -> bool:
        new_pos = P(orig_pos.x - 1, orig_pos.y)
        return self.move(orig_pos, new_pos, matrix)

    def move_right(self, orig_pos: P, matrix: NDArray) -> bool:
        new_pos = P(orig_pos.x + 1, orig_pos.y)
        return self.move(orig_pos, new_pos, matrix)

    def move_down(self, orig_pos: P, matrix: NDArray) -> bool:
        new_pos = P(orig_pos.x, orig_pos.y + 1)
        return self.move(orig_pos, new_pos, matrix)


shapes = [
    Shape([P(0, 0), P(1, 0), P(2, 0), P(3, 0)]),
    Shape([P(0, 1), P(1, 0), P(1, 1), P(2, 1), P(1, 2)]),
    Shape(
        [
            P(2, 0),
            P(2, 1),
            P(2, 2),
            P(1, 2),
            P(0, 2),
        ]
    ),
    Shape([P(0, 0), P(0, 1), P(0, 2), P(0, 3)]),
    Shape(
        [
            P(0, 0),
            P(0, 1),
            P(1, 0),
            P(1, 1),
        ]
    ),
]


def print_matrix(matrix: NDArray):
    for row in matrix:
        for cell in row:
            if cell == 1:
                sys.stdout.write("@")
            elif cell == 0:
                sys.stdout.write(".")
        sys.stdout.write("\n")

    print("=" * matrix.shape[1])


def play_shape(shape: Shape, matrix: NDArray, jets: Iterable[str]):
    pos = P(2, 0)
    assert shape.place(pos, matrix)
    print_matrix(matrix)
    for jet in jets:
        if jet == "<":
            side_pos = P(pos.x - 1, pos.y)
        elif jet == ">":
            side_pos = P(pos.x + 1, pos.y)

        if shape.move(pos, side_pos, matrix):
            down_pos = P(pos.x - 1, pos.y + 1)
            if shape.move(side_pos, down_pos, matrix):
                pos = down_pos
            else:
                break
        else:
            down_pos = P(pos.x, pos.y + 1)
            if shape.move(side_pos, down_pos, matrix):
                pos = down_pos
            else:
                break


def play_shapes(shapes: Iterable[Shape], jets: Iterable[str]) -> NDArray:
    matrix: Optional[NDArray] = None

    for shape in shapes:
        if matrix is None:
            matrix = np.zeros((shape.height + 3, 7), int)
        else:
            no_empty_lines = get_empty_lines(matrix)
            new_lines = np.zeros((shape.height - no_empty_lines + 3, 7), int)
            matrix = np.vstack((new_lines, matrix))

        play_shape(shape, matrix, jets)
        print("after play shape")
        print_matrix(matrix)

    assert matrix is not None
    return matrix


def get_empty_lines(matrix: NDArray):
    cnt = 0
    for row in matrix:
        if row.any():
            return cnt
        else:
            cnt += 1
    return cnt


def test_play_shapes():
    matrix = play_shapes(shapes[:2], jets=cycle(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"))
    print_matrix(matrix)


def test_play_shape():
    shape = shapes[0]
    matrix = np.zeros((shape.height + 3, 7), int)
    assert get_empty_lines(matrix) == 4
    play_shape(shape, matrix, jets=">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    print("AFTER PLAY 1")
    print_matrix(matrix)
    assert get_empty_lines(matrix) == 3

    new_rows = np.zeros((1, 7))
    matrix = np.vstack((new_rows, matrix))
    play_shape(shape, matrix, jets=">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    print("AFTER PLAY 2")
    print_matrix(matrix)


def test_shape():
    shape = Shape([P(0, 1), P(1, 0), P(1, 1), P(2, 1), P(1, 2)])
    matrix = np.zeros((7, 7), int)
    assert shape.place(P(0, 0), matrix)

    assert (
        matrix
        == np.array(
            [
                [0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]
        )
    ).all()

    assert shape.move(P(0, 0), P(1, 0), matrix)
    assert (
        matrix
        == np.array(
            [
                [0, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]
        )
    ).all()

    assert not shape.can_be_placed(P(1, 0), matrix)
    assert not shape.can_be_placed(P(0, 0), matrix)

    assert shape.move_left(P(1, 0), matrix)
    assert (
        matrix
        == np.array(
            [
                [0, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]
        )
    ).all()
    assert not shape.move_left(P(1, 0), matrix)
