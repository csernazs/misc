#!/usr/bin/python3

from functools import lru_cache


def calc_erosion_level(geo_index, depth):
    return (geo_index + depth) % 20183


@lru_cache(maxsize=1024*128)
def calc_geo_index(x, y, target, depth):
    if x == 0:
        return y * 48271
    elif y == 0:
        return x * 16807
    elif x == target[0] and y == target[1]:
        return 0

    left = (calc_geo_index(x - 1, y, target, depth) + depth) % 20183
    up = (calc_geo_index(x, y - 1, target, depth) + depth) % 20183
    return left * up


def get_type(x, y, target, depth):
    geo_index = calc_geo_index(x, y, target, depth)
    print("geo", x, y, geo_index)
    erosion = calc_erosion_level(geo_index, depth)
    return erosion % 3


def solve(depth, target):
    retval = 0
    for y in range(target[1] + 1):
        for x in range(target[0] + 1):
            cell_type = get_type(x, y, target, depth)
            print("typ", x, y, cell_type)
            retval += cell_type
    return retval


def main():
    print(solve(7305, (13, 734)))


if __name__ == "__main__":
    main()
