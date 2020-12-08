#!/usr/bin/env python3


def parse_file(path: str):
    retval = []
    with open(path) as infile:
        for line in infile:
            fields = line.rstrip().split()
            retval.append([fields[0], int(fields[1])])

    return retval


def run_program(program):
    acc = 0
    ip = 0
    seen = set()
    while True:
        if ip in seen:
            return (acc, True)
        seen.add(ip)
        op, arg = program[ip]

        if op == "nop":
            ip += 1
        elif op == "acc":
            acc += arg
            ip += 1
        elif op == "jmp":
            ip += arg

        if ip == len(program) - 1:
            return (acc, False)


def solve_1(data):
    acc, _ = run_program(data)
    return acc


def solve_2(data):
    acc, loop = run_program(data)
    if not loop:
        return acc

    patch_indexes = []
    for idx, (op, _) in enumerate(data):
        if op == "nop" or op == "jmp":
            patch_indexes.append(idx)

    for idx in patch_indexes:
        if data[idx][0] == "jmp":
            data[idx][0] = "nop"
        elif data[idx][0] == "nop":
            data[idx][0] = "jmp"

        acc, loop = run_program(data)
        if not loop:
            return acc

        if data[idx][0] == "jmp":
            data[idx][0] = "nop"
        elif data[idx][0] == "nop":
            data[idx][0] = "jmp"


def main():
    data = parse_file("aoc_08.txt")
    print(solve_1(data))
    print(solve_2(data))


if __name__ == "__main__":
    main()
