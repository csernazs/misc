#!/usr/bin/env python


def part1(numbers):
    cnt = 0
    prev = None
    for curr in numbers:
        if prev is None:
            prev = curr
            continue
        if prev < curr:
            cnt += 1
        prev = curr

    print(cnt)


def part2(numbers):
    cnt = 0
    prev = None
    for idx in range(len(numbers) - 2):
        curr = sum(numbers[idx:idx+3])
        if prev is None:
            prev = curr
            continue
        if prev < curr:
            cnt += 1

        prev = curr

    print(cnt)


def main():
    with open("aoc_01.txt") as infile:
        numbers = [int(x) for x in infile]
    part1(numbers)
    part2(numbers)


if __name__ == "__main__":
    main()