#!/usr/bin/env python3


def parse_file(path: str):
    retval = []
    with open(path) as infile:
        record = []
        for raw_line in infile:
            line = raw_line.rstrip()
            if line == "":
                retval.append(record)
                record = []
            else:
                record.append(line)

    if record:
        retval.append(record)

    return retval


def solve_1(data):
    cnt = 0
    for record in data:
        questions = set()
        for person in record:
            questions.update(person)

        cnt += len(questions)

    return cnt


def solve_2(data):
    cnt = 0
    for record in data:
        questions = set(record[0])
        for person in record[1:]:
            person_answers = set(person)
            questions = questions.intersection(person_answers)
            if not questions:
                break

        cnt += len(questions)

    return cnt


def main():
    data = parse_file("aoc_06.txt")
    print(solve_1(data))
    print(solve_2(data))


if __name__ == "__main__":
    main()
