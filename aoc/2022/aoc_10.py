#!/usr/bin/env python3
import sys
from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np
from pyparsing import Iterable
import pytest
from attr import dataclass
from numpy.typing import NDArray


@dataclass
class Registers:
    x: int
    pc: int


class Instruction(ABC):
    @abstractmethod
    def execute(self, registers: Registers):
        pass

    def reset(self):
        pass


class Noop(Instruction):
    def execute(self, registers: Registers):
        registers.pc += 1

    def __eq__(self, other) -> bool:
        return isinstance(other, Noop)

    def __repr__(self) -> str:
        return "<Noop>"


class AddX(Instruction):
    def __init__(self, param: int):
        self.cycle = 0
        self.param = param

    def execute(self, registers: Registers):
        if self.cycle == 0:
            self.cycle += 1

        elif self.cycle == 1:
            self.cycle += 1
            registers.pc += 1
            registers.x += self.param
        else:
            raise ValueError(self.cycle)

    def reset(self):
        self.cycle = 0

    def __eq__(self, other) -> bool:
        if not isinstance(other, AddX):
            return False

        return self.cycle == other.cycle and self.param == other.param

    def __repr__(self) -> str:
        return f"<AddX cycle={self.cycle} param={self.param}>"


class Code:
    def __init__(self, instructions: Sequence[Instruction]):
        self.instrs = instructions

    def execute(self):
        for instr in self.instrs:
            instr.reset()

        regs = Registers(x=1, pc=0)
        while True:
            if regs.pc > len(self.instrs) - 1:
                break

            yield regs

            instr = self.instrs[regs.pc]
            instr.execute(regs)


def parse(lines: list[str]) -> Code:
    retval: list[Instruction] = []
    noop = Noop()
    for line in lines:
        fields = line.split()
        if fields[0] == "noop":
            retval.append(noop)
        elif fields[0] == "addx":
            retval.append(AddX(int(fields[1])))
        else:
            raise ValueError(fields[0])
    return Code(tuple(retval))


def part01(code: Code) -> int:
    retval = 0
    for cycle, regs in enumerate(code.execute(), start=1):
        if cycle == 20 or (cycle - 20) > 0 and (cycle - 20) % 40 == 0:
            signal_strength = cycle * regs.x
            retval += signal_strength

    return retval


def format_screen(array: NDArray):
    rows = []
    for array_row in array:
        row = ""
        for cell in array_row:
            if cell == 1:
                row += "#"
            else:
                row += "."
        rows.append(row)

    return rows


def part02(code: Code):
    width = 40
    height = 6

    screen = np.zeros(width * height, dtype=np.int8)
    pos = 0

    for pos, regs in enumerate(code.execute(), start=0):
        if (pos % width) >= regs.x - 1 and (pos % width) <= regs.x + 1:
            screen[pos] = 1

    retval = format_screen(screen.reshape(height, width))
    return retval


def main():
    with open("aoc_10.txt") as infile:
        lines = [x.strip() for x in infile.readlines()]
    code = parse(lines)
    print(part01(code))
    print("\n".join(part02(code)))


@pytest.fixture(scope="session")
def lines() -> list[str]:
    with open("aoc_10.sample") as infile:
        lines = [x.strip() for x in infile.readlines()]

    return lines


@pytest.fixture
def sample(lines: list[str]) -> Code:
    return parse(lines)


def test_parser(lines: list[str]):
    parsed = parse(lines)
    assert parsed.instrs[:10] == (
        AddX(15),
        AddX(-11),
        AddX(6),
        AddX(-3),
        AddX(5),
        AddX(-1),
        AddX(-8),
        AddX(13),
        AddX(4),
        Noop(),
    )
    assert len(parsed.instrs) == 146


def test_part01(sample: Code):
    assert part01(sample) == 13140


def test_part02(sample: Code):
    screen = part02(sample)

    assert screen == [
        "##..##..##..##..##..##..##..##..##..##..",
        "###...###...###...###...###...###...###.",
        "####....####....####....####....####....",
        "#####.....#####.....#####.....#####.....",
        "######......######......######......####",
        "#######.......#######.......#######.....",
    ]


if __name__ == "__main__":
    sys.exit(main())
