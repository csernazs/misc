#!/usr/bin/python3 -u

import pdb
import sys
from collections import Counter
from pprint import pprint


class Distance:
    def __init__(self, distance=None, point=None):
        self.distance = distance
        self.point = point

    def __repr__(self):
        return "d={} p={}".format(self.distance, self.point)

    def update(self, distance, point):
        if self.distance is None or distance < self.distance:
            self.distance = distance
            self.point = point


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def __mul__(self, number):
        return Point(self.x * number, self.y * number)

    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)

    def copy(self):
        return Point(self.x, self.y)


def get_boundary(points):
    start = True
    for point in points:
        if start:
            topleft = point.copy()
            bottomright = point.copy()
            start = False
            continue

        if point.x < topleft.x:
            topleft.x = point.x
        if point.y < topleft.y:
            topleft.y = point.y

        if point.x > bottomright.x:
            bottomright.x = point.x
        if point.y > bottomright.y:
            bottomright.y = point.y

    return topleft, bottomright


def get_infinite_points(matrix):

    infinite = set()
    for distance in matrix[0] + matrix[-1]:
        if distance is not None:
            infinite.add(distance.point.copy())

    for y in range(len(matrix[0])):
        distance = matrix[0][y]
        if distance is not None:
            infinite.add(distance.point.copy())

    for y in range(len(matrix[-1])):
        distance = matrix[-1][y]
        if distance is not None:
            infinite.add(distance.point.copy())

    return infinite


def main():
    source = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""

    source = open("aoc06.txt").read().strip()

    points = []
    for line in source.splitlines():
        position = tuple(map(int, line.split(", ")))
        points.append(Point(position[0], position[1]))

    topleft, bottomright = get_boundary(points)

    new_points = []
    for point in points:
        new_points.append(point - topleft + Point(1, 1))

    points = new_points
    topleft, bottomright = get_boundary(points)
    #bottomright = bottomright + Point(2, 2)

    print(topleft, bottomright)

    matrix = [[None for _ in range(bottomright.y)] for _ in range(bottomright.x)]

    # matrix[1][5].distance = 12333

    for x in range(bottomright.x):
        for y in range(bottomright.y):
            point_distances = [Distance(p.distance(Point(x, y)), p) for p in points]
            point_distances.sort(key=lambda x: x.distance)
            if point_distances[0].distance == point_distances[1].distance:
                matrix[x][y] = None
            else:
                matrix[x][y] = point_distances[0]

    pprint(matrix)

    infinite = get_infinite_points(matrix)
    print("infinite", infinite)

    sums = Counter()

    for row in matrix:
        for element in row:
            if element is None:
                continue

            if element.point in infinite:
                continue

            sums.update([element.point])

    print(sums.most_common(10))

    return

    name_map = {}
    char = ord("a")
    for row in matrix:
        for cell in reversed(row):
            if cell is None:
                sys.stdout.write(".")
                continue

            point = cell.point
            if point not in name_map:
                name_map[point] = chr(char)
                char += 1

            if cell.distance == 0:
                sys.stdout.write(name_map[point].upper())
            else:
                sys.stdout.write(name_map[point])

        sys.stdout.write("\n")

if __name__ == "__main__":
    main()
