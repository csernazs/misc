#!/usr/bin/python3

import argparse
import tokenize
from pprint import pprint

def patch_name(name):
    if name.startswith("__") and not name.endswith("__"):
        print("Patching {!r}".format(name))
        return name[1:]
    else:
        return name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Source to process")
    parser.add_argument("-o", "--output", help="Where to write patched code")

    args = parser.parse_args()

    path = args.file

    with open(path, "rb") as sourcefile:
        tokens = list(tokenize.tokenize(sourcefile.readline))

    new_tokens = []
    for token in tokens:
        print(token)
        new_type, new_string, start, end, line = token
        if token.type == tokenize.NAME:
            new_string = patch_name(token.string)

        new_tokens.append((new_type, new_string, start, end, line))

    new_source = tokenize.untokenize(new_tokens).decode()

    print(new_source)
    if args.output:
        open(args.output, "w").write(new_source)

if __name__ == "__main__":
    main()
