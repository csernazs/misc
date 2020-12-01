#!/usr/bin/env python3

def main():
    numbers = []
    for line in open("aoc_01.txt"):
        numbers.append(int(line))

    for idx1 in range(len(numbers)):
        for idx2 in range(idx1 + 1, len(numbers)):
            a = numbers[idx1]
            b = numbers[idx2]
            if a + b == 2020:
                print(a * b)


if __name__ == "__main__":
    main()
