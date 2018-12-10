#!/usr/bin/python3

import re
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, other):
        return math.hypot(abs(self.x - other.x), abs(self.y - other.y))


class Vector:
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity

    def move(self):
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

    def move_back(self):
        self.pos.x -= self.velocity.x
        self.pos.y -= self.velocity.y

    def __repr__(self):
        return "<{} v {}>".format(self.pos, self.velocity)

    def __hash__(self):
        return hash((self.pos, self.velocity))


def get_boundary(points):
    max_y = max(points, key=lambda p: p.y).y
    max_x = max(points, key=lambda p: p.x).x

    min_y = min(points, key=lambda p: p.y).y
    min_x = min(points, key=lambda p: p.x).x

    return (Point(min_x, min_y), Point(max_x, max_y))


def print_points(points):
    boundary = get_boundary(points)
    min_p, max_p = boundary
    width = max_p.x - min_p.x + 1
    height = max_p.y - min_p.y + 1

    for y in range(height):
        line = ""
        for x in range(width):
            p = Point(x + min_p.x, y + min_p.y)
            if p in points:
                line += "#"
            else:
                line += "."
        print(line)


def solve(vectors):
    old_distance = None
    cnt = 0
    while True:
        points = set()
        for vec in vectors:
            points.add(vec.pos)

        boundary = get_boundary(points)
        distance = boundary[0].distance(boundary[1])
        if old_distance is not None and distance > old_distance:
            break
        print(int(distance))

        for vec in vectors:
            vec.move()
            for _ in range(int(distance / 1000)):
                vec.move()

        cnt += int(distance / 1000) + 1
        old_distance = distance

    for vec in vectors:
        vec.move_back()

    points = set()
    for vec in vectors:
        points.add(vec.pos)

    print_points(points)
    print(cnt - 1)


def parse(input_text):
    for line in input_text.splitlines():
        match = re.match("position=<(.*),(.*)> velocity=<(.*),(.*)>", line)
        pos = Point(int(match.group(1)), int(match.group(2)))
        velocity = Point(int(match.group(3)), int(match.group(4)))
        vec = Vector(pos, velocity)
        yield vec


def main():
    input_text = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""
    input_text = open("aoc10.txt").read()
    vectors = list(parse(input_text))
    solve(vectors)


if __name__ == "__main__":
    main()
