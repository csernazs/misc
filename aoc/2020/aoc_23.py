#!/usr/bin/env python3

from collections import deque
from time import perf_counter
from array import array


class Timer:
    def __init__(self, name):
        self.name = name
        self.t = None

    def __enter__(self):
        pass

    #        self.t = perf_counter()

    def __exit__(self, *args, **kwargs):
        pass


#        print(self.name, int((perf_counter() - self.t) * 1000))


def do_round(data):
    # print("start", data)
    # data = data.copy()

    with Timer("pop"):
        current = data.pop(0)
        selected = array("I", [data.pop(0), data.pop(0), data.pop(0)])

    with Timer("minmax"):
        min_item = min(data)
        max_item = max(data)

    with Timer("dst selection"):
        dst = current - 1
        if dst < min_item:
            dst = max_item
        while dst in selected:
            dst = dst - 1
            if dst < min_item:
                dst = max_item

        dst_idx = data.index(dst)

    # print("dst", dst)
    # print("dst_idx", dst_idx)

    with Timer("new data alloc"):
        new_data = data[0 : dst_idx + 1] + selected + data[dst_idx + 1 :]
        new_data.append(current)
    # print("new_data", new_data)

    return new_data


def solve_1(data):
    data = list(data)

    for move in range(100):
        # print("=== MOVE", move)
        data = do_round(data)
        # print("result", data)

    idx = data.index(1)
    sol = []
    while True:
        idx = idx + 1
        if idx > len(data) - 1:
            idx = 0
        if data[idx] == 1:
            break
        sol.append(data[idx])

    sol_s = "".join([str(x) for x in sol])
    return sol_s


seen = set()


def solve_2(data):
    data = list(data) + list(range(max(data), 1000001))
    data = array("I", data)
    for move in range(10000):
        if move % 1000 == 0:
            print("=== MOVE", move)
        with Timer("do_round total"):
            data = do_round(data)
        # print("result", data)
        # print(data[0])
        # print("next", data[data.index(1) + 1])
        # print("next next", data[data.index(1) + 2])


def main():
    data_s = "219347865"
    data = tuple([int(x) for x in data_s])

    print(solve_1(data))
    #t1 = perf_counter()
    #solve_2(data)
    #print("total", int((perf_counter() - t1) * 1000))


if __name__ == "__main__":
    main()
