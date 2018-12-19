#!/usr/bin/python3

from collections import defaultdict


class Area:
    def __init__(self, rows):
        self.data = rows

    def copy(self):
        return Area([x.copy() for x in self.data])

    def to_tuple(self):
        return tuple([tuple(row) for row in self.data])

    @classmethod
    def parse(cls, input_text):
        lines = input_text.splitlines()
        rows = []
        for line in lines:
            row = list(line)
            rows.append(row)

        return cls(rows)

    @classmethod
    def new(cls, width, height, cell=None):
        data = [[cell] * width for _ in range(height)]
        return cls(data)

    def __setitem__(self, position, value):
        self.data[position[1]][position[0]] = value

    def __getitem__(self, position):
        return self.data[position[1]][position[0]]

    def get(self, x, y, default=None):
        try:
            return self[x, y]
        except KeyError:
            return default

    @property
    def width(self):
        return len(self.data[0])

    @property
    def height(self):
        return len(self.data)

    def is_valid_position(self, position):
        if position[0] < 0 or position[0] > self.width - 1:
            return False
        if position[1] < 0 or position[1] > self.height - 1:
            return False

        return True

    def print(self):
        for row in self.data:
            print("".join(row))

    def __iter__(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                yield (x, y, cell)

    def iter_cells(self, cell_types, callable=None):
        if callable is None:
            callable = lambda x, y, z: (x, y, z)

        for x, y, cell in self:
            if cell in cell_types:
                yield callable(x, y, cell)

    def count_cells(self):
        counts = defaultdict(int)
        for _, _, cell in self:
            counts[cell] += 1

        return dict(counts)

    def iter_nearby_cells_4(self, position):
        x, y = position
        positions = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]

        for x, y in positions:
            if self.is_valid_position((x, y)):
                cell = self.get(x, y)
                if cell is not None:
                    yield (x, y, cell)

    def iter_nearby_cells_8(self, position):
        x, y = position

        for y_offset in (-1, 0, 1):
            for x_offset in (-1, 0, 1):
                if x_offset == 0 and y_offset == 0:
                    continue
                if self.is_valid_position((x + x_offset, y + y_offset)):
                    cell = self.get(x + x_offset, y + y_offset)
                    if cell is not None:
                        yield (x, y, cell)


def icount(iterator):
    cnt = 0
    for _ in iterator:
        cnt += 1
    return cnt


def solve(input_text, minutes):
    area = Area.parse(input_text)

    area.print()

    areas = {}

    for minute in range(minutes):
        if minute % 10000 == 0:
            print(minute)

        cache_key = area.to_tuple()
        if cache_key in areas:
            print("HIT")
            new_area = areas[cache_key]
            continue
        else:
            print("MISS")

        # print("-------------")
        new_area = area.copy()

        for x, y, cell in area:
            sums = {".": 0, "#": 0, "|": 0}
            for near_x, near_y, near_cell in area.iter_nearby_cells_8((x, y)):
                sums[near_cell] += 1

            if cell == "." and sums["|"] >= 3:  # open
                new_cell = "|"
            elif cell == "|" and sums["#"] >= 3:  # trees
                new_cell = "#"
            elif cell == "#" and (sums["#"] < 1 or sums["|"] < 1):  # lumperyard
                new_cell = "."
            else:
                new_cell = cell

            new_area[x, y] = new_cell

#        new_area.print()

        areas[area.to_tuple()] = new_area
        area = new_area

    counts = area.count_cells()
    resource_value = counts["|"] * counts["#"]
    # print(resource_value)

    return resource_value


def main():
    input_text = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".strip()

    input_text = open("aoc18.txt").read().strip()

    # print(solve(input_text, 10))
    print(solve(input_text, 1000000000))

if __name__ == "__main__":
    main()
