#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import Optional

import PIL.Image
import PIL.ImageDraw
import pytest

P = tuple[int, int]
POINTS = dict[P, int]


def rng(a, b):
    if a < b:
        return range(a, b + 1)
    else:
        return range(b, a + 1)


def parse_line(line: str) -> POINTS:
    retval: POINTS = {}

    point = None
    for point_s in line.split(" -> "):
        point_l = [int(x) for x in point_s.split(",")]
        if point is None:
            point = (point_l[0], point_l[1])
        else:
            new_point: P = (point_l[0], point_l[1])
            for x in rng(point[0], new_point[0]):
                for y in rng(point[1], new_point[1]):
                    retval[(x, y)] = 1
            point = new_point
    return retval


def parse(lines: list[str]) -> POINTS:
    retval: POINTS = {}

    for line in lines:
        retval.update(parse_line(line))
    return retval


class ImageWriter:
    def __init__(
        self,
        size: P,
        offset: P,
        target_dir: Path,
        colormap: Optional[dict[int, tuple[int, int, int]]] = None,
    ):
        assert target_dir.is_dir()

        self.target_dir = target_dir
        self.frame_no = 0
        self.size = size
        self.offset = offset
        self.resize_factor = 5

        print("size", self.size)
        print("offset", self.offset)

        if colormap is None:
            self.colormap = {1: (255, 0, 0), 2: (0, 255, 0)}
        else:
            self.colormap = colormap

    def save(self, points: POINTS):
        im = PIL.Image.new(size=self.size, mode="RGB")
        px = im.load()

        for pos, value in points.items():
            p = (pos[0] - self.offset[0], pos[1] - self.offset[1])
            try:
                px[p] = self.colormap[value]
            except IndexError:
                print("size", self.size)
                print("p", p)
                raise

        with self.target_dir.joinpath(f"IMG_{self.frame_no:05}.jpg").open("wb") as outfile:
            im.resize(
                (self.size[0] * self.resize_factor, self.size[1] * self.resize_factor),
                resample=PIL.Image.Resampling.NEAREST,
            ).save(outfile, "JPEG")

        self.frame_no += 1

    @classmethod
    def from_points(
        cls, points: POINTS, target_dir: Path, colormap: Optional[dict[int, tuple[int, int, int]]] = None
    ):
        upper_left = [-1, -1]
        lower_right = [0, 0]

        for pos in points:
            if pos[0] > lower_right[0]:
                lower_right[0] = pos[0]
            if pos[1] > lower_right[1]:
                lower_right[1] = pos[1]

            if pos[0] < upper_left[0] or upper_left[0] == -1:
                upper_left[0] = pos[0]
            if pos[1] < upper_left[1] or upper_left[1] == -1:
                upper_left[1] = pos[1]

        size = [lower_right[0] - upper_left[0] + 10, lower_right[1] + 10]
        offset = (upper_left[0], 0)

        if size[0] % 2 == 1:
            size[0] += 1

        if size[1] % 2 == 1:
            size[1] += 1

        return cls(tuple(size), offset, target_dir, colormap)


def run_sand(points: POINTS, bottom: int) -> P:
    sand = (500, 0)
    while sand[1] <= bottom:
        trials = [(sand[0], sand[1] + 1), (sand[0] - 1, sand[1] + 1), (sand[0] + 1, sand[1] + 1)]
        for tr in trials:
            if tr not in points:
                sand = tr
                break
        else:  # not terminated by break
            return sand

    return sand


def part01(points: POINTS) -> int:

    target_dir = Path("/tmp/images2")
    if target_dir.is_dir():
        im = ImageWriter.from_points(points, target_dir)
    else:
        im = None

    bottom = max(points, key=lambda x: x[1])[1] + 1
    cnt = 0

    while True:
        sand = run_sand(points, bottom)
        if sand[1] > bottom:
            break
        points[sand] = 2
        if im is not None:
            im.save(points)
        cnt += 1
    return cnt


def part02(points: POINTS) -> int:
    bottom = max(points, key=lambda x: x[1])[1]
    cnt = 0

    target_dir = Path("/tmp/images2")
    if target_dir.is_dir():
        im = ImageWriter.from_points(points, target_dir)
        im.size = (505, 505)
        im.resize_factor = 2
    else:
        im = None

    while True:
        sand = run_sand(points, bottom)
        points[sand] = 2
        if im is not None:
            im.save(points)
        cnt += 1
        if sand == (500, 0):
            break

    return cnt


def main():
    with open("aoc_14.txt") as infile:
        lines = [x.strip() for x in infile]

    parsed = parse(lines)
    print(part01(parsed.copy()))
    print(part02(parsed))


@pytest.fixture
def sample() -> POINTS:
    return {
        (494, 9): 1,
        (495, 9): 1,
        (496, 6): 1,
        (496, 9): 1,
        (497, 6): 1,
        (497, 9): 1,
        (498, 4): 1,
        (498, 5): 1,
        (498, 6): 1,
        (498, 9): 1,
        (499, 9): 1,
        (500, 9): 1,
        (501, 9): 1,
        (502, 4): 1,
        (502, 5): 1,
        (502, 6): 1,
        (502, 7): 1,
        (502, 8): 1,
        (502, 9): 1,
        (503, 4): 1,
    }


def test_parse(sample: POINTS):
    lines = [
        "498,4 -> 498,6 -> 496,6",
        "503,4 -> 502,4 -> 502,9 -> 494,9",
    ]

    assert parse(lines) == sample


def test_part01(sample: POINTS):
    assert part01(sample) == 24


def test_part02(sample: POINTS):
    assert part02(sample) == 93


if __name__ == "__main__":
    sys.exit(main())
