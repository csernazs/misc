#!/usr/bin/python3


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

    rules = {tuple(k): v for k, v in rules.items()}

    state = ["."] * 500 + list(init) + ["."] * 500
    clean_state = ["."] * len(state)
    print(0, "\t", "".join(state).strip("."))

    for cnt in range(iterations):
        new_state = clean_state[:]
        for idx in range(len(state) - 4):
            substr = tuple(state[idx : idx + 5])
            new_state[idx + 2] = rules.get(substr, ".")

        state = new_state
        print(cnt + 1, "\t", get_state_sum(state), "\t", "".join(state).strip("."))

    return get_state_sum(state)


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
    print(solve(init, rules, 20))


if __name__ == "__main__":
    main()
