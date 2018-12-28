#!/usr/bin/python3 -u


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_boundary(points):
    topleft = list(points[0])
    bottomright = list(points[0])

    for point in points[1:]:
        topleft[0] = min(point[0], topleft[0])
        topleft[1] = min(point[1], topleft[1])

        bottomright[0] = max(point[0], bottomright[0])
        bottomright[1] = max(point[1], bottomright[1])

    return tuple(topleft), tuple(bottomright)


def parse(input_text):
    points = []
    for line in input_text.splitlines():
        position = tuple(map(int, line.split(", ")))
        points.append((position[0], position[1]))

    return points


def solve(points):
    points.sort()

    p = points[-1]
    cnt = 0
    for x in range(p[0] - 2000, p[0] + 2000):
        for y in range(p[1] - 2000, p[1] + 2000):
            dist = 0
            for point in points:
                dist += distance(point, (x, y))
                if dist > 10000:
                    break
            else:
                cnt += 1

        if x % 1000 == 0:
            print(x, cnt)

    return cnt


def main():
    source = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""

    source = open("aoc06.txt").read().strip()

    points = parse(source)
    # print(get_boundary(points))
    print("sol", solve(points))


if __name__ == "__main__":
    main()
