#!/usr/bin/python3

from functools import lru_cache
from collections import defaultdict, deque
import pdb

CLIMB = 0
TORCH = 1
NEITHER = 2

TYPE_TOOL_MAP = {0: (CLIMB, TORCH), 1: (CLIMB, NEITHER), 2: (TORCH, NEITHER), 99: (TORCH,)}
TYPES = ".=|"


class Matrix:
    def __init__(self, rows):
        self.data = rows

    def copy(self):
        return Matrix([x.copy() for x in self.data])

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

    def print_callable(self, func):
        for row in self.data:
            print("".join([func(x) for x in row]))

    def print_mapping(self, mapping):
        for row in self.data:
            print("".join([mapping[x] for x in row]))

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

    def get_nearby_cells_4_positions(self, position):
        x, y = position
        positions = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        return [pos for pos in positions if self.is_valid_position(pos)]

    def iter_nearby_cells_4(self, position):
        for x, y in self.get_nearby_cells_4_positions(position):
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


def calc_erosion_level(geo_index, depth):
    return (geo_index + depth) % 20183


@lru_cache(maxsize=1024 * 128)
def calc_geo_index(x, y, target, depth):
    if x == 0:
        return y * 48271
    elif y == 0:
        return x * 16807
    elif x == target[0] and y == target[1]:
        return 0

    left = (calc_geo_index(x - 1, y, target, depth) + depth) % 20183
    up = (calc_geo_index(x, y - 1, target, depth) + depth) % 20183
    return left * up


def get_type(x, y, target, depth):
    geo_index = calc_geo_index(x, y, target, depth)
    erosion = calc_erosion_level(geo_index, depth)
    return erosion % 3


def create_matrix(depth, size, target):
    rows = []
    for y in range(size[1] + 1):
        row = []
        for x in range(size[0] + 1):
            cell_type = get_type(x, y, target, depth)
            row.append(cell_type)

        rows.append(row)

    return Matrix(rows)


def calc_distances(matrix: Matrix, distances: Matrix, origin):
#    if origin == (10, 11):
#        pdb.set_trace()
    retval = []
    current_distance, current_tools, _ = distances[origin]
    for nearby_pos in matrix.get_nearby_cells_4_positions(origin):
        next_required_tools = TYPE_TOOL_MAP[matrix[nearby_pos]]

        current_tools_set = set(current_tools)

        intersection = set(next_required_tools).intersection(current_tools_set)
        if intersection:
            new_tools = intersection
            cost = 1
        else:
            new_tools = set(next_required_tools).intersection(set(TYPE_TOOL_MAP[matrix[origin]]))
#            new_tools = set(next_required_tools).intersection(set(TYPE_TOOL_MAP[matrix[origin]]))
            # print(new_tools)
            cost = 8

        distance = current_distance + cost
        nearby_distance = distances[nearby_pos]

        if nearby_distance is None or distance < nearby_distance[0]:
            distances[nearby_pos] = nearby_distance = [distance, new_tools, [origin]]
            if nearby_pos not in retval:
                retval.append(nearby_pos)
        elif distance == nearby_distance[0]:
            if new_tools - nearby_distance[1]:
                if nearby_pos not in retval:
                    retval.append(nearby_pos)
                nearby_distance[1].update(new_tools)
            if origin not in nearby_distance[2]:
                nearby_distance[2].append(origin)

    return retval


def get_route(distances, target):
    excluded = []
    pos = target
    retval = []
    while pos != (0, 0):
        for origin_pos in distances[pos][2]:
            if origin_pos not in excluded:
                break
        else:
            raise RuntimeError("Something went wrong")

        pos = origin_pos
        retval.append(pos)

    #    retval.reverse()

    return retval


def calc_route_cost(matrix: Matrix, distances: Matrix, route: list):
    cost = 0
    current_tools = set([TORCH])
    for wpt in route:
        required_tools = set(TYPE_TOOL_MAP[matrix[wpt]])
        intersection = required_tools.intersection(current_tools)

        if not intersection:
            current_tools = required_tools
            cost += 8
        else:
            current_tools = intersection
            cost += 1
        # print(
        #     "go",
        #     wpt,
        #     "req=",
        #     required_tools,
        #     "curr=",
        #     current_tools,
        #     "cost=",
        #     cost,
        #     "distance=",
        #     distances[wpt],
        # )

    return cost


def solve(depth: int, target: tuple):
    matrix_size = (target[0] + 100, target[1] + 100)
    matrix = create_matrix(depth, matrix_size, target)
    # matrix = Matrix.new(target[0] * 2, target[1] * 2, 0)
#    matrix.print_mapping(TYPES)
    distances = Matrix.new(matrix.width, matrix.height, None)
    distances[0, 0] = [0, set([TORCH]), []]
    matrix[target] = 99

    queue = deque([(0, 0)])
    while len(queue) > 0:
        pos = queue.popleft()
        batch = calc_distances(matrix, distances, pos)
        queue.extend(batch)

    target_distance = distances[target]

#    distances.print_callable(lambda cell: "{:4}".format(str(cell[0])))
#    route = get_route(distances, target)
#    for cnt, waypoint in enumerate(route, 1):
#        print(cnt, waypoint)

    #    print("cost", calc_route_cost(matrix, distances, route))
    print(target_distance)
    return target_distance[0]


def main():
#    print(solve(510, (10, 10)))


    print(solve(7305, (13, 734)))


if __name__ == "__main__":
    main()
