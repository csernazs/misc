#!/usr/bin/python3

def common_letters(str1, str2):
    for c1, c2 in zip(str1, str2):
        if c1 == c2:
            yield c1


def difference(str1, str2):
    retval = 0
    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            retval += 1
    return retval


lines = [x.strip() for x in open("aoc02.txt")]


sol1 = sol2 = None

for line1 in lines:
    for line2 in lines:
        if line1 == line2:
            continue

        if difference(line1, line2) == 1:
            print(line1, line2)
            sol1, sol2 = line1, line2

if sol1:
    print("".join(common_letters(sol1, sol2)))
