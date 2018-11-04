#!/usr/bin/python3
# pylint: disable=all

import sys

try:
    infile = open(sys.argv[1], "r")
except IndexError:
    infile = sys.stdin

try:
    outfile = open(sys.argv[2], "w")
except IndexError:
    outfile = sys.stdout


def read_int(f):
    return int(f.readline())


def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))


def read_lines(f, no_lines):
    retval = []
    for i in range(no_lines):
        retval.append(f.readline().rstrip())
    return retval


def evaluate_program(program):
    retval = 0
    beam = 1
    for instr in program:
        if instr == "C":
            beam = beam * 2
        elif instr == "S":
            retval = retval + beam

    return retval


def solve(shield, program):
    if evaluate_program(program) <= shield:
        return 0

    if "C" not in program:
        return "IMPOSSIBLE"

    if "S" not in program:
        return 0

    #print("P", program, evaluate_program(program))
    cnt = 1
    while True:
        old_program = program
        swap_idx = program.rfind("CS")
        if swap_idx == -1:
            return "IMPOSSIBLE"

        program_list = list(program)
        program_list[swap_idx] = "S"
        program_list[swap_idx + 1] = "C"

        program = "".join(program_list)
        if evaluate_program(program) <= shield:
            return cnt
        print(program)
        cnt += 1

def main():
    no_cases = read_int(infile)

    for case_idx in range(no_cases):
        shield, program = infile.readline().strip().split(" ")
        shield = int(shield)
        #print("CASE", shield, program)
        solution = solve(shield, program)

        outfile.write("Case #%d: %s\n" % (case_idx + 1, solution))


if __name__ == "__main__":
    main()
