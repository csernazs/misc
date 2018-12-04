#!/usr/bin/python3


from collections import Counter

lines = [x.strip() for x in open("aoc02.txt")]

two = 0
three = 0
for line in lines:
    counter = Counter(line)
    has_two = 0
    has_three = 0

    for letter, count in counter.items():
        if count == 2 and not has_two:
            has_two = 1
        elif count == 3 and not has_three:
            has_three = 1

    two += has_two
    three += has_three

print(two * three)
