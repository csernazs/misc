#!/usr/bin/python3

from collections import namedtuple, defaultdict
import re


class Assumption(namedtuple("Assumption", ("before", "after", "instruction"))):
    pass


class Processor:
    def __init__(self):
        self.operations = {}
        for name in dir(self):
            if name.startswith("op_"):
                self.operations[name[3:]] = getattr(self, name)

    def get_callable(self, operation):
        return self.operations[operation]

    def execute_program(self, code, registers, ip_register):
        registers = registers.copy()
        ip = 0
        cnt = 0
        while ip < len(code):
            if cnt % 1000000 == 0:
                print(registers)
            registers[ip_register] = ip
            self.execute(registers, *code[ip])
            ip = registers[ip_register]
            ip += 1
            cnt += 1

        return registers

    def execute(self, registers, operation, param_a, param_b, param_c):
        func = self.get_callable(operation)
        if func is None:
            raise ValueError("Invalid operation: {!r}".format(operation))

        func(registers, param_a, param_b, param_c)

    def op_addr(self, registers, param_a, param_b, param_c):
        registers[param_c] = registers[param_a] + registers[param_b]

    def op_addi(self, registers, param_a, param_b, param_c):
        registers[param_c] = registers[param_a] + param_b

    def op_mulr(self, registers, param_a, param_b, param_c):
        registers[param_c] = registers[param_a] * registers[param_b]

    def op_muli(self, registers, param_a, param_b, param_c):
        registers[param_c] = registers[param_a] * param_b

    def op_banr(self, registers, param_a, param_b, param_c):
        registers[param_c] = registers[param_a] & registers[param_b]

    def op_bani(self, registers, param_a, param_b, param_c):
        registers[param_c] = registers[param_a] & param_b

    def op_borr(self, registers, param_a, param_b, param_c):
        registers[param_c] = registers[param_a] | registers[param_b]

    def op_bori(self, registers, param_a, param_b, param_c):
        registers[param_c] = registers[param_a] | param_b

    def op_setr(self, registers, param_a, _, param_c):
        registers[param_c] = registers[param_a]

    def op_seti(self, registers, param_a, _, param_c):
        registers[param_c] = param_a

    def op_gtir(self, registers, param_a, param_b, param_c):
        if param_a > registers[param_b]:
            registers[param_c] = 1
        else:
            registers[param_c] = 0

    def op_gtri(self, registers, param_a, param_b, param_c):
        if registers[param_a] > param_b:
            registers[param_c] = 1
        else:
            registers[param_c] = 0

    def op_gtrr(self, registers, param_a, param_b, param_c):
        if registers[param_a] > registers[param_b]:
            registers[param_c] = 1
        else:
            registers[param_c] = 0

    def op_eqir(self, registers, param_a, param_b, param_c):
        if param_a == registers[param_b]:
            registers[param_c] = 1
        else:
            registers[param_c] = 0

    def op_eqri(self, registers, param_a, param_b, param_c):
        if registers[param_a] == param_b:
            registers[param_c] = 1
        else:
            registers[param_c] = 0

    def op_eqrr(self, registers, param_a, param_b, param_c):
        if registers[param_a] == registers[param_b]:
            registers[param_c] = 1
        else:
            registers[param_c] = 0


def parse_code(input_text):
    code = []
    ip_register = None
    for line in input_text.splitlines():
        if line.startswith("#ip "):
            ip_register = int(line[3:])
            continue

        fields = line.split()
        instruction = (fields[0], int(fields[1]), int(fields[2]), int(fields[3]))
        code.append(instruction)

    return code, ip_register


def solve_a(code, ip_register):
    proc = Processor()
    print(proc.execute_program(code, [0] * 6, ip_register))


def solve_b(code, ip_register):
    proc = Processor()
    print(proc.execute_program(code, [1, 0, 0, 0, 0, 0], ip_register))


def main():
    input_text = """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".strip()

    input_text = open("aoc19.txt").read().strip()

    code, ip_register = parse_code(input_text)
#    solve_a(code, ip_register)
    solve_b(code, ip_register)


if __name__ == "__main__":
    main()
