#!/usr/bin/python3

# pylint: disable=all

import sys

infile = sys.stdin
outfile = sys.stdout
#logfile = open("/tmp/log.txt", "a")
cnt = 0


class Continue(Exception):
    pass


class Exit(Exception):
    pass


def log(msg):
    pass
#    logfile.write(str(msg) + "\n")
#    logfile.flush()


def read_int(f):
    return int(f.readline())


def read_pos():
    pos_x, pos_y = map(int, infile.readline().strip().split())
    if pos_x == -1 and pos_y == -1:
        raise Exit()
    if pos_x == 0 and pos_y == 0:
        raise Continue()

    return (pos_x, pos_y)


def write_pos(pos_x, pos_y):
    global cnt
    outfile.write("{} {}\n".format(pos_x, pos_y))
    outfile.flush()
    cnt += 1
    return read_pos()


def check(matrix, pos_x, pos_y):
    for x in [pos_x - 1, pos_x, pos_x + 1]:
        for y in [pos_y - 1, pos_y, pos_y + 1]:
            if matrix[x][y] != 1:
                return False
    return True


def fill(matrix, pos_x, pos_y):
    while not check(matrix, pos_x, pos_y):
        new_x, new_y = write_pos(pos_x, pos_y)
        matrix[new_x][new_y] = 1


def solve(area):
    global cnt
    cnt = 0
    matrix = [[0] * 1000 for x in range(1000)]

    if area == 20:
        fill(matrix, 2, 2)
        fill(matrix, 3, 2)
        fill(matrix, 2, 4)
        fill(matrix, 3, 4)
    elif area == 200:
        for pos_x in [2, 5, 8, 11, 14, 17, 19]:
            for pos_y in [2, 5, 8, 9]:
                fill(matrix, pos_x, pos_y)

    else:
        raise Exit()


def main():
    global cnt
    no_cases = read_int(infile)
    for case_idx in range(no_cases):
        area = read_int(infile)
        log("area {}".format(area))

        try:
            solve(area)
        except Continue:
            log("cnt {}".format(cnt))
            cnt = 0
            continue
        except Exit:
            sys.exit(1)


if __name__ == "__main__":
    main()
