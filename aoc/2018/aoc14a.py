#!/usr/bin/python3

from collections import deque


def print_recipes(recipes, elves):
    buff = []
    for idx, recipe in enumerate(recipes):
        if idx in elves:
            buff.append("({})".format(recipe))
        else:
            buff.append(" {} ".format(recipe))

    return " ".join(buff)


def solve(iterations):
    recipes = [3, 7]
    elves = [0, 1]
    print_recipes(recipes, elves)

    cnt = 1
    while len(recipes) < iterations:
        recpies_sum = recipes[elves[0]] + recipes[elves[1]]
        digits = [int(x) for x in str(recpies_sum)]
        recipes.extend(digits)

        for elf_idx, elf in enumerate(elves):
            current_recipe = recipes[elf]
            new_pos = elf + current_recipe + 1
            while new_pos > len(recipes) - 1:
                new_pos = new_pos - len(recipes)

            elves[elf_idx] = new_pos

        # print(cnt, "\t", print_recipes(recipes, elves))
        print(cnt)
        cnt += 1

    return "".join(map(str, recipes[-10:]))


def main():
    print(solve(681901 + 10))


if __name__ == "__main__":
    main()
