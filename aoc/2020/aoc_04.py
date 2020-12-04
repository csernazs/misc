#!/usr/bin/env python3

import sys
import re


def parse_file(path):
    with open(path) as infile:
        record = {}
        for raw_line in infile:
            line = raw_line.rstrip()
            if line == "":
                yield record
                record = {}
            else:
                fields = [x.split(":") for x in line.split(" ")]
                record.update(fields)


def validate_height(height: str):
    try:
        if height.endswith("cm"):
            return 150 <= int(height[:-2]) <= 193
        elif height.endswith("in"):
            return 59 <= int(height[:-2]) <= 76
    except ValueError:
        return False
    return False


def is_valid(pp):
    if not has_required_fields(pp):
        return False

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    # cid (Country ID) - ignored, missing or not.

    retval = int(pp["byr"]) >= 1920 and int(pp["byr"]) <= 2002
    retval = retval and int(pp["iyr"]) >= 2010 and int(pp["iyr"]) <= 2020
    retval = retval and int(pp["eyr"]) >= 2020 and int(pp["eyr"]) <= 2030
    retval = retval and validate_height(pp["hgt"])
    retval = retval and bool(re.match("#[0-9a-f]{6}$", pp["hcl"]))
    retval = retval and pp["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
    retval = retval and bool(re.match("[0-9]{9}$", pp["pid"]))

    return retval


def has_required_fields(pp):
    required_fields = (
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    )
    for required_field in required_fields:
        if required_field not in pp:
            return False

    return True


def solve_1(data):
    cnt = 0
    for passport in data:
        if has_required_fields(passport):
            cnt += 1

    print(cnt)


def solve_2(data):
    cnt = 0
    for passport in data:
        if is_valid(passport):
            cnt += 1

    print(cnt)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "aoc_04.txt"
    data = list(parse_file(path))
    solve_1(data)
    solve_2(data)


if __name__ == "__main__":
    main()
