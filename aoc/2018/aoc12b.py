#!/usr/bin/python3

from collections import deque

def parse(input_text):
    lines = input_text.splitlines()
    initial_state = lines[0].split(" ")[-1]

    rules = {}
    for line in lines[2:]:
        rule = line.split(" => ")
        rules[rule[0]] = rule[1]

    return initial_state, rules


def get_state_sum(state):
    retval = 0
    for idx, item in enumerate(state):
        if item == "#":
            value = idx - 500
            retval += value

    return retval


def solve(init, rules, iterations):
    maxlength = 30
    sums = deque([], maxlength)
    rules = {tuple(k): v for k, v in rules.items()}

    state = ["."] * 500 + list(init) + ["."] * 500
    clean_state = ["."] * len(state)
    print(0, "\t", "".join(state).strip("."))

    old_state_sum = None
    for cnt in range(500):
        new_state = clean_state[:]
        for idx in range(len(state) - 4):
            substr = tuple(state[idx : idx + 5])
            new_state[idx + 2] = rules.get(substr, ".")

        state_sum = get_state_sum(new_state)
        if old_state_sum is not None:
            diff = state_sum - old_state_sum
            print(diff)
            sums.appendleft(diff)
            if len(sums) == maxlength and list(sums) == [sums[0]] * len(sums):
                break

        state = new_state
        old_state_sum = state_sum

    print(cnt)

    return get_state_sum(state) + diff * (iterations - cnt)


def main():
    input_text = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""

    input_text = open("aoc12.txt").read()
    init, rules = parse(input_text)
    print(init)
    print(rules)
    print(solve(init, rules, 50000000000))


if __name__ == "__main__":
    main()
