#!/usr/bin/env python3

import re

def iter_file():
    for line in open("aoc_02.txt"):
        # 1-3 a: abcde
        if m := re.match("(\d+)-(\d+) (\w): (\w+)", line.rstrip()):
            groups = list(m.groups())
            groups[0] = int(groups[0])
            groups[1] = int(groups[1])
            yield groups
        else:
            print("No match", line)
            return


def main():
    cnt = 0
    data = list(iter_file())
    for start, end, char, password in data:
        c = password.count(char)
        if c >= start and c <= end:
            cnt += 1
    print(cnt)

    cnt = 0
    for pos1, pos2, char, password in data:
        c1 = password[pos1 - 1]
        c2 = password[pos2 - 1]
        if (c1 == char and c2 != char) or (c1 != char and c2 == char):
            cnt += 1
    print(cnt)


if __name__ == "__main__":
    main()
