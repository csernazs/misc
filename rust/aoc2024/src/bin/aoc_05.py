#!/usr/bin/env python3


from functools import cmp_to_key
from pprint import pprint


input_lines = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13
""".strip().splitlines()


class Ordering:
    def __init__(self, rules: list[tuple[int, int]]):
        self.rules = rules
        self.map_before: dict[int, list[int]] = {}
        self.order: dict[int, int] = {}
        # self.map_after: dict[int, list[int]] = {}

        self.calculate_map_before()
        # self.calculate_map_after()
        self.calculate_orders()

        pprint(self.map_before)
        # pprint(self.map_after)
        pprint(self.order)

    def calculate_orders(self) -> None:
        order = [kv[0] for kv in sorted(self.map_before.items(), key=lambda x: len(x[1]), reverse=True)]
        self.order = {k: idx for idx, k in enumerate(order)}

    def calculate_map_before(self) -> None:
        for left, right in self.rules:
            if left not in self.map_before:
                self.map_before[left] = [right]
            else:
                self.map_before[left].append(right)

    # def calculate_map_after(self) -> None:
    #     for left, right in self.rules:
    #         if left not in self.map_after:
    #             self.map_after[right] = [left]
    #         else:
    #             self.map_after[right].append(left)

    def in_order(self, left: int, right: int) -> bool:
        if right not in self.order:
            return True

        if left not in self.order:
            return False

        return self.order[left] < self.order[right]

    def cmp(self, left: int, right: int) -> int:
        if left == right:
            return 0

        in_order = self.in_order(left, right)
        # print(left, right, in_order)
        if in_order:
            return -1
        else:
            return 1


def pages_in_order(ordering: Ordering, pages: list[int]) -> bool:
    new_pages = sorted(pages, key=cmp_to_key(ordering.cmp))
    # print("pages    ", pages)
    # print("new_pages", new_pages)
    return pages == new_pages


def solve1(rules: list[tuple[int, ...]], pages_list: list[list[int]]) -> int:
    ordering = Ordering(rules)

    retval = 0
    for pages in pages_list:
        if pages_in_order(ordering, pages):
            middle_value = pages[len(pages) // 2]
            print(middle_value)
            retval += middle_value
    return retval


def main() -> None:
    rules: list[tuple[int, int]] = [tuple(map(int, line.split("|"))) for line in input_lines]

    pages_list: list[list[int]] = [
        [75, 47, 61, 53, 29],
        [97, 61, 53, 29, 13],
        [75, 29, 13],
        [75, 97, 47, 61, 53],
        [61, 13, 29],
        [97, 13, 75, 29, 47],
    ]

    ordering = Ordering(rules)

    # pages_in_order(ordering, pages_list[0])

    print(pages_in_order(ordering, pages_list[0]))

    print("===")

    for pages in pages_list:
        print(pages_in_order(ordering, pages))

    print(solve1(rules, pages_list))


if __name__ == "__main__":
    main()
