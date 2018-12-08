#!/usr/bin/python3


class Node:
    def __init__(self, children=None, meta=None):
        if children is None:
            children = []

        if meta is None:
            meta = []

        self.children = children
        self.meta = meta

    def __getitem__(self, idx):
        return self.children[idx]

    def __len__(self):
        return sum([len(x) for x in self.children]) + 2 + len(self.meta)

    def get_value(self):
        if self.children:
            retval = 0
            for child_no in self.meta:
                child_idx = child_no - 1
                if child_idx < len(self.children):
                    child = self[child_idx]
                    retval += child.get_value()

            return retval
        else:
            return sum(self.meta)

    @classmethod
    def parse(cls, sequence, depth=0):
        no_children = sequence[0]
        no_meta = sequence[1]
        indent = depth * "    "

        children = []
        children_len = 0
        print(indent, "no_children", no_children)
        print(indent, "no_meta", no_meta)
        for _ in range(no_children):
            child = cls.parse(sequence[2 + children_len :], depth=depth + 1)
            children.append(child)
            children_len += len(child)

        print(indent, "length", children_len)
        meta = sequence[children_len + 2 : children_len + 2 + no_meta]
        print(indent, "meta", meta)
        return cls(children, meta)

    def walk(self):
        retval = [self]
        for child in self.children:
            retval.extend(child.walk())
        return retval


def solve_a(sequence):
    root = Node.parse(sequence)

    meta_sum = 0
    for node in root.walk():
        meta_sum += sum(node.meta)

    print("sum", meta_sum)


def solve_b(sequence):
    root = Node.parse(sequence)
    print("value", root.get_value())


def main():
    input_text = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

    input_text = open("aoc08.txt").read()

    input_text = input_text.strip()
    sequence = [int(x) for x in input_text.split()]

    # solve_a(sequence)
    solve_b(sequence)


if __name__ == "__main__":
    main()
