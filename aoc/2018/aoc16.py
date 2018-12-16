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


def parse_assumptions(input_text):
    assumptions = []
    before_registers = after_registers = instruction = None

    prev_line = None
    for line in input_text.splitlines():
        #        print(repr(line))
        if prev_line is not None and prev_line == "" and line == "":
            break

        prev_line = line
        match = re.match(r"Before: \[(\d+), (\d+), (\d+), (\d+)\]", line)
        if match:
            before_registers = [int(x) for x in match.groups()]
            continue

        match = re.match(r"After:  \[(\d+), (\d+), (\d+), (\d+)\]", line)
        if match:
            after_registers = [int(x) for x in match.groups()]
            continue

        match = re.match(r"(\d+) (\d+) (\d+) (\d+)", line)
        if match:
            instruction = [int(x) for x in match.groups()]
            continue

        if line == "":
            assert before_registers
            assert after_registers
            assert instruction

            assumptions.append(Assumption(before_registers, after_registers, instruction))
            before_registers = after_registers = instruction = None

        else:
            raise ValueError(repr(line))

    return assumptions


def parse_code(input_text):
    idx = input_text.find("\n\n\n\n")
    code = []
    for line in input_text[idx + 4 :].splitlines():
        instruction = [int(x) for x in line.split()]
        code.append(instruction)

    return code


def get_possible_operations(before, after, instruction):
    ops = Processor()
    before = before.copy()

    retval = []

    for operation in ops.operations:
        registers = before.copy()

        ops.execute(registers, operation, instruction[1], instruction[2], instruction[3])
        if registers == after:
            retval.append(operation)

    return retval


def solve_a(assumptions):
    cnt = 0
    for assumption in assumptions:
        operations = get_possible_operations(assumption.before, assumption.after, assumption.instruction)
        if len(operations) >= 3:
            cnt += 1

    print(cnt)


def resolve_operations(assumptions):
    proc = Processor()

    opcode_to_op = defaultdict(set)
    for assumption in assumptions:
        operations = get_possible_operations(assumption.before, assumption.after, assumption.instruction)
        for operation in operations:
            opcode_to_op[assumption.instruction[0]].add(operation)

    op_to_opcode = {}
    while len(op_to_opcode) < len(proc.operations):
        for opcode, ops in opcode_to_op.items():
            if len(ops) == 1:
                op_to_opcode[ops.pop()] = opcode

        for opcode, ops in opcode_to_op.items():
            for op_to_remove in op_to_opcode:
                if op_to_remove in ops:
                    ops.remove(op_to_remove)

    return {v: k for k, v in op_to_opcode.items()}


def solve_b(assumptions, code):
    proc = Processor()
    opcodes = resolve_operations(assumptions)
    registers = [0, 0, 0, 0]
    for opcode, param_a, param_b, param_c in code:
        op = opcodes[opcode]
        proc.execute(registers, op, param_a, param_b, param_c)

    print(registers)
    print(registers[0])


def main():
    input_text = """
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]


""".lstrip()

    input_text = open("aoc16.txt").read()

    assumptions = parse_assumptions(input_text)
    solve_a(assumptions)

    code = parse_code(input_text)
    #    print(code)

    solve_b(assumptions, code)


if __name__ == "__main__":
    main()
