#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Dict, List, Set
from collections import defaultdict


@dataclass
class Food:
    allergens: Set[str]
    ingredients: Set[str]

    def copy(self):
        return Food(set(self.allergens), set(self.ingredients))


def set_to_value(s):
    assert len(s) == 1
    l = list(s)
    return l[0]


def parse_file(path: str) -> List[Food]:
    retval = []
    with open(path) as infile:
        for raw_line in infile:
            line = raw_line.rstrip()

            ingredients, allergens = line.split("(")
            ingredients = set(ingredients.split())

            allergens = set(allergens[len("contains ") : -1].split(", "))
            retval.append(Food(allergens, ingredients))
    return retval


def intersect(sets: List[Set]):
    s = sets[0].copy()
    for s_next in sets[1:]:
        s.intersection_update(s_next)
    return s


def find_allergen(all_allergens: Dict[str, List[Set[str]]]):
    for allergen, foods in all_allergens.items():
        reduced = intersect(foods)
        # print("reduced", allergen, reduced, foods)
        if len(reduced) == 1:
            return (allergen, set_to_value(reduced))
    return (None, None)


def get_known_ingredients(food_list: List[Food]):
    food_list = [x.copy() for x in food_list]
    all_allergens = defaultdict(list)

    for food in food_list:
        for allergen in food.allergens:
            all_allergens[allergen].append(food.ingredients)

    known = {}

    while len(known) < len(all_allergens):
        # print("ALL ---")
        # for key, value in all_allergens.items():
        #     print("    ", key, value)

        allergen, ingredient = find_allergen(all_allergens)
        # print("known", allergen, ingredient)
        known[allergen] = ingredient
        if allergen is None:
            raise ValueError()

        for allergen, foods in all_allergens.items():
            for food in foods:
                if ingredient in food:
                    food.remove(ingredient)

    return known


def solve_1(food_list: List[Food]):
    known = get_known_ingredients(food_list)
    known_ingredients = set(known.values())

    cnt = 0
    for food in food_list:
        cnt += len(food.ingredients - known_ingredients)

    return cnt


def solve_2(food_list: List[Food]):
    known = get_known_ingredients(food_list)
    known_ingredients = [known[key] for key in sorted(known)]
    return ",".join(known_ingredients)


def main():
    foods = parse_file("aoc_21.txt")
    print("solve_1", solve_1(foods))
    print("solve_2", solve_2(foods))


if __name__ == "__main__":
    main()
