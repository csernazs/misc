#!/usr/bin/env python3


from pathlib import Path
import sys
from itertools import cycle


def get_checksum(int_list: list[int]):
    retval = 0
    for idx, num in enumerate(int_list):
        retval += idx * num

    return retval


def defrag(inflated: list[int]) -> list[int]:
    rev = reversed([x for x in inflated if x > -1])
    taken_length = len([x for x in inflated if x > -1])
    retval: list[int] = []

    for num in inflated:
        if len(retval) == taken_length:
            return retval

        if num == -1:
            retval.append(next(rev))
        else:
            retval.append(num)

    return retval


def main():
    contents = Path(sys.argv[1]).read_text().strip()

    inflated = []
    for state, (idx, char) in zip(cycle([0, 1]), enumerate(contents)):
        if state == 0:
            inflated.extend([idx // 2] * int(char))
        else:
            inflated.extend([-1] * int(char))

    Path("/tmp/inflate_py.txt").write_text("\n".join([str(x) for x in inflated]))

    defragged = defrag(inflated)
    Path("/tmp/defragged_py.txt").write_text("\n".join([str(x) for x in defragged]))
    checksum = get_checksum(defragged)

    print(checksum)


if __name__ == "__main__":
    sys.exit(main())
