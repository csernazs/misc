#!/usr/bin/python3

import argparse
import ast
import redbaron

def patch_name(name):
    if name.startswith("__") and not name.endswith("__"):
        return name[1:]
    else:
        return name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Source to process")
    parser.add_argument("-o", "--output", help="Where to write patched code")

    args = parser.parse_args()

    path = args.file

    source = open(path, "r").read()

    tree = redbaron.RedBaron(source)

    #tree.help()
    # NameNode, DefNode
    for node in tree.find_all("NameNode"):
        node.value = patch_name(node.value)

    for node in tree.find_all("DefNode"):
        node.name = patch_name(node.name)

    source = tree.dumps()
    print(tree)
    if args.output:
        open(args.output, "w").write(source)

if __name__ == "__main__":
    main()

