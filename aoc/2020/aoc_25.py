#!/usr/bin/env python3


def parse_file(path: str):
    with open(path) as infile:
        pubkey1 = int(infile.readline().rstrip())
        pubkey2 = int(infile.readline().rstrip())

    return (pubkey1, pubkey2)


def calculate_loop_size(pubkey, init=7):
    acc = init
    cnt = 1
    while acc != pubkey:
        acc = (acc * init) % 20201227
        cnt += 1
    return cnt


def calculate_private_key(init, loop_size):
    acc = init
    for _ in range(loop_size - 1):
        acc = (acc * init) % 20201227

    return acc


def solve_1(pubkeys):
    loop0 = calculate_loop_size(pubkeys[0])
    loop1 = calculate_loop_size(pubkeys[1])

    print("loop0", loop0)
    print("loop1", loop1)

    priv = calculate_private_key(pubkeys[1], loop0)
    return priv


def main():
    pubkeys = parse_file("aoc_25.txt")

    print("solve_1", solve_1(pubkeys))


if __name__ == "__main__":
    main()
