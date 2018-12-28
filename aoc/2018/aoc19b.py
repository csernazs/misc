#!/usr/bin/python3

from collections import namedtuple, defaultdict
import re


INDENT = "    "


class Processor:
    def __init__(self):
        self.operations = {}
        for name in dir(self):
            if name.startswith("op_"):
                self.operations[name[3:]] = getattr(self, name)

    def get_callable(self, operation):
        return self.operations[operation]

    def convert_to_c(self, code, registers, ip_register):
        lines = []
        lines.append("#define IP_REGISTER {}".format(ip_register))
        lines.append("#define REGISTERS {{ {} }}".format(", ".join([str(x) for x in registers])))
        lines.append("#define CODE_LEN {}".format(len(code)))
        lines.append("")
        for idx, instruction in enumerate(code):
            lines.append("inline void instr_{}(long* registers) {{".format(idx))
            operation, param_a, param_b, param_c = instruction
            func = self.get_callable(operation)
            lines.extend(func(param_a, param_b, param_c))

            lines.append("}")

        lines.append("")

        lines.append("inline void run_instr(int idx, long* registers) {")
        lines.append(INDENT + "switch (idx) {")
        for idx in range(len(code)):
            lines.append(INDENT*2 + "case {}: instr_{}(registers); break;".format(idx, idx))
        lines.append(INDENT + "};")
        lines.append("}")
        return "\n".join(lines)

    def op_addr(self, param_a, param_b, param_c):
        return [INDENT + "registers[{}] = registers[{}] + registers[{}];".format(param_c, param_a, param_b)]

    def op_addi(self, param_a, param_b, param_c):
        return [INDENT + "registers[{}] = registers[{}] + {};".format(param_c, param_a, param_b)]

    def op_mulr(self, param_a, param_b, param_c):
        return [INDENT + "registers[{}] = registers[{}] * registers[{}];".format(param_c, param_a, param_b)]

    def op_muli(self, param_a, param_b, param_c):
        return [INDENT + "registers[{}] = registers[{}] * {};".format(param_c, param_a, param_b)]

    def op_banr(self, param_a, param_b, param_c):
        return [INDENT + "registers[{}] = registers[{}] & registers[{}];".format(param_c, param_a, param_b)]

    def op_bani(self, param_a, param_b, param_c):
        return [INDENT + "registers[{}] = registers[{}] & {};".format(param_c, param_a, param_b)]

    def op_borr(self, param_a, param_b, param_c):
        return [INDENT + "registers[{}] = registers[{}] | registers[{}];".format(param_c, param_a, param_b)]

    def op_bori(self, param_a, param_b, param_c):
        return [INDENT + "registers[{}] = registers[{}] | {};".format(param_c, param_a, param_b)]

    def op_setr(self, param_a, _, param_c):
        return [INDENT + "registers[{}] = registers[{}];".format(param_c, param_a)]

    def op_seti(self, param_a, _, param_c):
        return [INDENT + "registers[{}] = {};".format(param_c, param_a)]

    def op_gtir(self, param_a, param_b, param_c):
        return [
            INDENT
            + "if ({} > registers[{}]) {{ registers[{}] = 1; }} else {{ registers[{}] = 0; }}".format(
                param_a, param_b, param_c, param_c
            )
        ]

    def op_gtri(self, param_a, param_b, param_c):
        return [
            INDENT
            + "if (registers[{}] > {}) {{ registers[{}] = 1; }} else {{ registers[{}] = 0; }}".format(
                param_a, param_b, param_c, param_c
            )
        ]


    def op_gtrr(self, param_a, param_b, param_c):
        return [
            INDENT
            + "if (registers[{}] > registers[{}]) {{ registers[{}] = 1; }} else {{ registers[{}] = 0; }}".format(
                param_a, param_b, param_c, param_c
            )
        ]


    def op_eqir(self, param_a, param_b, param_c):
        return [
            INDENT
            + "if ({} == registers[{}]) {{ registers[{}] = 1; }} else {{ registers[{}] = 0; }}".format(
                param_a, param_b, param_c, param_c
            )
        ]

    def op_eqri(self, param_a, param_b, param_c):
        return [
            INDENT
            + "if (registers[{}] == {}) {{ registers[{}] = 1; }} else {{ registers[{}] = 0; }}".format(
                param_a, param_b, param_c, param_c
            )
        ]


    def op_eqrr(self, param_a, param_b, param_c):
        return [
            INDENT
            + "if (registers[{}] == registers[{}]) {{ registers[{}] = 1; }} else {{ registers[{}] = 0; }}".format(
                param_a, param_b, param_c, param_c
            )
        ]

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


def solve_b(code, ip_register):
    proc = Processor()

    print(proc.convert_to_c(code, [1, 0, 0, 0, 0, 0], ip_register))


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
    solve_b(code, ip_register)


if __name__ == "__main__":
    main()
