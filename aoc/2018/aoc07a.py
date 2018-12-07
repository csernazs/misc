#!/usr/bin/python3

from pprint import pprint
from collections import defaultdict


def main():
    input_text = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    input_text = open("aoc07.txt").read()
    requirements = defaultdict(list)

    for line in input_text.splitlines():
        line = line.strip()
        fields = line.split()
        dependency = fields[1]
        step = fields[7]

        requirements[step].append(dependency)
        requirements[dependency]

    pprint(requirements)

    completed = []

    while len(completed) < len(requirements):
        temp_completed = []
        for step, deps in requirements.items():
            if step in completed:
                continue
            for dep in deps:
                if dep not in completed:
                    break
            else: # not terminated by break
                temp_completed.append(step)

        print(temp_completed)
        temp_completed.sort()
        completed.append(temp_completed[0])

    print("".join(completed))

if __name__ == "__main__":
    main()
