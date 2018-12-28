#!/usr/bin/python3

import re
from collections import namedtuple
import itertools
from pprint import pprint
from typing import List, Tuple


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


class Bot(namedtuple("Bot", ("pos", "radius"))):
    def distance(self, other):
        if isinstance(other, Bot):
            return distance(self.pos, other.pos)
        elif isinstance(other, (tuple, list)):
            return distance(self.pos, other)

    def get_boundary_points(self):
        retval = [
            (self.pos[0] - self.radius, self.pos[1], self.pos[2]),
            (self.pos[0] + self.radius, self.pos[1], self.pos[2]),
            (self.pos[0], self.pos[1] - self.radius, self.pos[2]),
            (self.pos[0], self.pos[1] + self.radius, self.pos[2]),
            (self.pos[0], self.pos[1], self.pos[2] - self.radius),
            (self.pos[0], self.pos[1], self.pos[2] + self.radius),
        ]
        return retval

    def is_overlap(self, other: "Bot"):
        for b_point in other.get_boundary_points():
            if self.distance(b_point) <= self.radius:
                return True
        return False

    def get_bots_in_range_count(self, bots: List["Bot"]) -> int:
        cnt = 0
        for bot in bots:
            if self.distance(bot) <= (bot.radius + self.radius):
                cnt += 1
        return cnt

    def is_in_range(self, pos: tuple):
        dst = self.distance(pos)
        return dst <= self.radius

    def divide(self):
        r = self.radius // 2

        return [
            Bot((self.pos[0] + r, self.pos[1], self.pos[2]), r),
            Bot((self.pos[0] - r, self.pos[1], self.pos[2]), r),
            Bot((self.pos[0], self.pos[1] + r, self.pos[2]), r),
            Bot((self.pos[0], self.pos[1] - r, self.pos[2]), r),
            Bot((self.pos[0], self.pos[1], self.pos[2] + r), r),
            Bot((self.pos[0], self.pos[1], self.pos[2] - r), r),
        ]

    def replace(self, **kwargs):
        return self._replace(**kwargs)


def parse(input_text: str):
    # "pos=<0,0,0>, r=4"
    retval = []
    for line in input_text.splitlines():
        match = re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)
        if match:
            fields = [int(x) for x in match.groups()]
            retval.append(Bot(fields[:3], fields[3]))
        else:
            raise ValueError(line)

    return retval


def bots_in_range(bots, pos):
    cnt = 0
    for bot in bots:
        if bot.is_in_range(pos):
            cnt += 1

    return cnt


def solve_a(bots):
    largest = max(bots, key=lambda bot: bot.radius)
    print(largest)
    cnt = 0
    for bot in bots:
        dst = bot.distance(largest)
        if dst <= largest.radius:
            cnt += 1

    return cnt


def solve_b(bots):
    bot = Bot((0, 0, 0), 1)
    while bot.get_bots_in_range_count(bots) < len(bots):
        bot = bot.replace(radius=bot.radius * 2)

    while bot.radius > 1:
        distances = [(b, b.get_bots_in_range_count(bots)) for b in bot.divide()]
        # pprint(distances)
        most_likely = max(distances, key=lambda x: x[1])[0]
        bot = most_likely
        print(most_likely)

    current = bot
    cnt = bots_in_range(bots, current.pos)
    print("current", current)
    print("cnt", cnt)


def main():
    input_text = """
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""".strip()

    input_text = open("aoc23.txt").read().strip()

    bots = parse(input_text)

    solve_b(bots)


if __name__ == "__main__":
    main()
