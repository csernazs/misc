#!/usr/bin/python3

from pprint import pprint
import itertools

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])


def parse(input_text: str):
    retval = []
    for line in input_text.splitlines():
        retval.append(tuple([int(x) for x in line.strip().split(",")]))

    return retval


def solve_a(points):
    points = set(points)

    groups = []

    while True:
        group = None
        for a, b in itertools.combinations(points, 2):
            if distance(a, b) <= 3:
                group = set((a, b))
                break

        if group is None:
            print("unable to form new group")
            break

        while True:
            new_member_added = False
            for p in points - group:
                new_member = None
                for member in group:
                    if distance(member, p) <= 3:
                        new_member = p
                        break
                if new_member:
                    break

            if new_member:
                # print("new_member", new_member, "into", group)
                group.add(new_member)
                new_member_added = True

            if not new_member_added:
                break

        points = points - group
        # print(points)
        groups.append(group)

        if not points:
            print("no more points")
            break

    #print("final groups", groups)
    #print("remaining points", points)
    return len(groups) + len(points)


def main():
    input_text = """
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,0,6
 9,0,0,0
12,0,0,0
 0,0,3,0
 0,0,0,3
50,0,0,0
54,0,0,0
51,0,0,0

""".strip()

    input_text = """
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2
""".strip()
    input_text = open("aoc25.txt").read().strip()
    points = parse(input_text)
    # pprint(points)
    print(solve_a(points))


if __name__ == "__main__":
    main()
