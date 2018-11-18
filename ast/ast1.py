#!/usr/bin/python3

import argparse
import ast
import astunparse
import astor


class NodeTransformer(ast.NodeTransformer):
    def patch_name(self, name):
        if name.startswith("__") and not name.endswith("__"):
            return name[1:]
        else:
            return name

    def visit_Name(self, node):
        print("name:", node.id)
        node.id = self.patch_name(node.id)
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        node.name = self.patch_name(node.name)
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        node.attr = self.patch_name(node.attr)
        self.generic_visit(node)
        return node


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Source to process")
    parser.add_argument("-o", "--output", help="Where to write patched code")

    args = parser.parse_args()

    path = args.file

    tree = ast.parse(open(path, "r").read())

    new_tree = NodeTransformer().visit(tree)

    source = astor.to_source(new_tree)
    print(astor.dump_tree(tree))
    print(source)

    if args.output:
        open(args.output, "w").write(source)

if __name__ == "__main__":
    main()

