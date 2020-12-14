#!/usr/bin/env python3

import re
from typing import List

from dataclasses import dataclass
from functools import cached_property
import itertools


@dataclass
class Mask:
    value: str

    @cached_property
    def and_mask(self):
        value_string = "".join(["0" if x == "0" else "1" for x in self.value])
        return int(value_string, 2)

    @cached_property
    def or_mask(self):
        value_string = "".join(["1" if x == "1" else "0" for x in self.value])
        return int(value_string, 2)

    def apply(self, value):
        return value & self.and_mask | self.or_mask

    def apply_floating(self, value: int):
        retval = []
        bits = list(bin(value)[2:].zfill(36))
        floatings = [idx for idx, value in enumerate(self.value) if value == "X"]
        no_floating = len(floatings)
        for floating in itertools.product(["0", "1"], repeat=no_floating):
            for i, new in enumerate(floating):
                bits[floatings[i]] = new

            retval.append(int("".join(bits), 2))
        return retval


@dataclass
class SetItem:
    address: int
    value: int


def parse_file(path: str):
    retval = []
    with open(path) as infile:
        for line in infile:
            if m := re.match(r"mem\[(\d+)\] = (\d+)", line):
                retval.append(SetItem(address=int(m.group(1)), value=int(m.group(2))))
            elif m := re.match(r"mask = ([1X0]+)", line):
                retval.append(Mask(m.group(1)))
            else:
                raise ValueError("Invalid line")
    return retval


def solve_1(data):
    memory = {}
    mask = Mask("X" * 36)
    for cmd in data:
        if isinstance(cmd, SetItem):
            memory[cmd.address] = mask.apply(cmd.value)
        elif isinstance(cmd, Mask):
            mask = cmd

    return sum(memory.values())


def solve_2(data):
    memory = {}
    mask = None
    for cmd in data:
        if isinstance(cmd, Mask):
            mask = cmd
        elif isinstance(cmd, SetItem):
            assert mask is not None
            address = cmd.address | mask.or_mask

            for target in mask.apply_floating(address):
                memory[target] = cmd.value

    return sum(memory.values())


def main():
    data = parse_file("aoc_14.txt")
    print("solve_1", solve_1(data))
    print("solve_2", solve_2(data))


if __name__ == "__main__":
    main()
