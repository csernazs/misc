#!/usr/bin/env python3


def parse_file(path: str):
    with open(path) as infile:
        for line in infile:
            yield line.rstrip()


def iter_seats(data):
    for entry in data:
        pos_row = convert_to_int(entry[:7], "FB")
        pos_col = convert_to_int(entry[7:], "LR")
        seat_id = pos_row * 8 + pos_col
        yield (pos_row, pos_col, seat_id)


def convert_to_int(text, replaces):
    return int(text.replace(replaces[0], "0").replace(replaces[1], "1"), 2)


def solve_1(data):
    return max(iter_seats(data), key=lambda x: x[2])[2]


def solve_2(data):
    seats = set()
    for row, col, _ in iter_seats(data):
        seats.add((row, col))

    min_row = min(seats, key=lambda x: x[0])[0]
    max_row = max(seats, key=lambda x: x[0])[0]

    for row in range(min_row + 1, max_row, 1):
        for col in range(8):
            if (row, col) not in seats:
                return row * 8 + col


def main():
    data = list(parse_file("aoc_05.txt"))
    print("solve_1", solve_1(data))
    print("solve_2", solve_2(data))


if __name__ == "__main__":
    main()
