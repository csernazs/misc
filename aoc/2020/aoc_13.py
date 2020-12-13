#!/usr/bin/env python3


from typing import List


def parse_file(path: str):
    with open(path) as infile:
        timestamp = int(infile.readline())
        schedule = infile.readline().rstrip().split(",")
    return timestamp, schedule


def solve_1(timestamp: int, schedule: List[str]):
    schedule: List[int] = [int(x) for x in schedule if x != "x"]

    best = None
    min_wait = None
    for bus_id in schedule:
        to_wait = bus_id - (timestamp % bus_id)
        if min_wait is None:
            best = bus_id
            min_wait = to_wait
        elif to_wait < min_wait:
            min_wait = to_wait
            best = bus_id

    return best * min_wait


def solve_2(schedule: List[str]):
    data = []
    for idx, item in enumerate(schedule):
        if item != "x":
            data.append((idx, int(item)))

    n = 0
    step = data[0][1]
    steps = {}
    data2 = tuple(data[1:])
    last_step_idx = 0

    while True:
        n = n + step
        # print(n)
        for idx, (offset, item) in enumerate(data2):
            if (n + offset) % item > 0:
                if idx > last_step_idx:
                    if idx in steps:
                        step = n - steps[idx]
                        # print("step for idx={}: {}".format(idx, step))
                        last_step_idx = idx
                    else:
                        steps[idx] = n
                    # print(n, idx)
                break
        else:
            return n


def main():
    timestamp, schedule = parse_file("aoc_13.txt")
    print("solve_1", solve_1(timestamp, schedule))
    print("solve_2", solve_2(schedule))


if __name__ == "__main__":
    main()
