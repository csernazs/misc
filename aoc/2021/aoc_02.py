#!/usr/bin/env python3


def part1():
    hpos = 0
    depth = 0
    with open("aoc_02.txt") as infile:
        for line in infile:
            command, distance = line.strip().split()
            distance = int(distance)
            if command == "forward":
                hpos += distance
            elif command == "up":
                depth -= distance
            elif command == "down":
                depth += distance

    print(hpos * depth)


def part2():
    hpos = 0
    depth = 0
    aim = 0
    with open("aoc_02.txt") as infile:
        for line in infile:
            command, distance = line.strip().split()
            distance = int(distance)
            if command == "forward":
                hpos += distance
                depth += aim * distance
            elif command == "up":
                aim -= distance
            elif command == "down":
                aim += distance

    print(hpos * depth)


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()