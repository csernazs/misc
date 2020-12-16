#!/usr/bin/env python3

from typing import List, Tuple
from dataclasses import dataclass
from functools import reduce
import operator


def mul(numbers):
    return reduce(operator.mul, numbers)


@dataclass
class Rule:
    name: str
    ranges: List[Tuple[int, int]]

    def match(self, value):
        for rng in self.ranges:
            if rng[0] <= value <= rng[1]:
                return True

        return False


@dataclass
class Data:
    your_ticket: List[int]
    tickets: List[List[int]]
    rules: List[Rule]


def parse_file(path: str) -> Data:
    retval = []
    section = 0
    rules = []
    tickets = []
    your_ticket = None
    with open(path) as infile:
        for raw_line in infile:
            line = raw_line.rstrip()
            if line == "":
                section += 1
                continue

            if section == 0:
                # departure location: 39-715 or 734-949
                name, ranges = line.split(": ")
                ranges = [tuple(map(int, x.split("-"))) for x in ranges.split(" or ")]
                for rng in ranges:
                    assert rng[0] < rng[1]
                rule = Rule(name, ranges)
                rules.append(rule)
            elif section == 1:
                if line == "your ticket:":
                    continue
                your_ticket = list(map(int, line.split(",")))
            elif section == 2:
                if line == "nearby tickets:":
                    continue
                ticket = list(map(int, line.split(",")))
                tickets.append(ticket)

    return Data(your_ticket, tickets, rules)


def set_to_value(s):
    l = list(s)
    assert len(l) == 1
    return l[0]

def get_invalid_numbers(ranges, ticket: List[int]):
    retval = []
    for number in ticket:
        for rng in ranges:
            if rng[0] <= number <= rng[1]:
                break
        else:
            retval.append(number)

    return retval


def is_column_valid(column, rule):
    for value in column:
        if not rule.match(value):
            return False
    return True


def is_ticket_valid(ticket, rules):
    for value in ticket:
        for rule in rules:
            if rule.match(value):
                break
        else:
            return False
    return True


def get_valid_tickets(data: Data):
    retval = []

    for ticket in data.tickets:
        if is_ticket_valid(ticket, data.rules):
            retval.append(ticket)

    return retval


def get_columns(tickets):
    retval = []
    for colidx in range(len(tickets[0])):
        column = []
        for ticket in tickets:
            column.append(ticket[colidx])
        retval.append(column)
    return retval


def get_column_fields(tickets, rules):
    column_fields = []

    for column in get_columns(tickets):
        matching_rules = set()
        for rule in rules:
            if is_column_valid(column, rule):
                matching_rules.add(rule.name)

        if not matching_rules:
            raise ValueError("No match")
        column_fields.append(matching_rules)

    while [x for x in column_fields if len(x) > 1]:
        one_rules = set()
        for matching_rules in column_fields:
            if len(matching_rules) == 1:
                one_rules.add(set_to_value(matching_rules))

        for matching_rules in column_fields:
            if len(matching_rules) > 1:
                matching_rules -= one_rules

    return [set_to_value(x) for x in column_fields]


def solve_1(data: Data):
    retval = 0
    ranges = []
    for rule in data.rules:
        ranges.extend(rule.ranges)

    for ticket in data.tickets:
        invalid_numbers = get_invalid_numbers(ranges, ticket)
        retval += sum(invalid_numbers)

    return retval


def solve_2(data: Data):
    tickets = get_valid_tickets(data)
    fields = get_column_fields(tickets, data.rules)
    column_indexes = [idx for idx, x in enumerate(fields) if x.startswith("departure")]
    values = [data.your_ticket[idx] for idx in column_indexes]
    return mul(values)


def main():
    data = parse_file("aoc_16.txt")
    print("solve_1", solve_1(data))
    print("solve_2", solve_2(data))


if __name__ == "__main__":
    main()
