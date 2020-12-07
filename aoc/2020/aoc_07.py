#!/usr/bin/env python3

import re


class Tree:
    def __init__(self):
        self.nodes = {}

    def ensure_node(self, name, **kwargs):
        if name in self.nodes:
            return self.nodes[name]
        else:
            node = Node(name, **kwargs)
            self.nodes[name] = node
            return node

    def make_node(self, name, children):
        node = self.ensure_node(name)
        child_nodes = []
        child_nodes = [(self.ensure_node(name), amount) for name, amount in children]
        node.children = child_nodes
        for child_node, _ in child_nodes:
            child_node.parents.append(node)

        return node


class Node:
    def __init__(self, name, children=None, parents=None):
        if not children:
            children = []
        self.children = children
        if not parents:
            parents = []
        self.parents = parents
        self.name = name
        self.value = None

    def calculate_value(self):
        if self.value is not None:
            return self.value

        value = 1
        for child_node, amount in self.children:
            value += amount * child_node.calculate_value()

        self.value = value
        return value

    def __repr__(self):
        return "<Node name='{}' children={!r}>".format(self.name, self.children)

    def iterate_parents(self):
        if not self.parents:
            return

        yield from self.parents

        for parent in self.parents:
            yield from parent.iterate_parents()


def parse_file(path: str):
    with open(path) as infile:
        for line in infile:
            # light red bags contain 1 bright white bag, 2 muted yellow bags.
            if m := re.match("([a-z ]+) bags contain", line):
                bag_name = m.groups()[0]
                if contains := re.findall("(\d+) ([a-z ]+) bag", line):
                    contains = [(x[1], int(x[0])) for x in contains]
                elif line.rstrip().endswith("contain no other bags."):
                    contains = []
                else:
                    raise ValueError(line)

                yield (bag_name, contains)
            else:
                raise ValueError(line)


def make_tree(data):
    tree = Tree()
    for bag_name, contains in data:
        tree.make_node(bag_name, contains)

    return tree


def solve_1(tree: Tree, start_name="shiny gold"):
    start_node = tree.nodes[start_name]
    result = set()
    cnt = 0
    for parent in start_node.iterate_parents():
        result.add(parent.name)
        cnt += 1

    return len(result)


def solve_2(tree: Tree, start_name="shiny gold"):
    start_node = tree.nodes[start_name]
    return start_node.calculate_value() - 1


def main():
    data = list(parse_file("aoc_07.txt"))
    tree = make_tree(data)
    print("solve_1", solve_1(tree))
    print("solve_2", solve_2(tree))


if __name__ == "__main__":
    main()
