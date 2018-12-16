#!/usr/bin/python3
from collections import deque


class Scene:
    def __init__(self, rows):
        self.data = rows

    @classmethod
    def parse(cls, input_text):
        lines = input_text.splitlines()
        rows = []
        for line in lines:
            row = list(line)
            rows.append(row)

        return cls(rows)

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

    def iter_cells(self, cell_types, klass):
        for x, y, cell in self:
            if cell in cell_types:
                yield klass(x, y, cell)

    def iter_nearby_cells(self, position):
        x, y = position
        positions = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]

        for x, y in positions:
            cell = self.get(x, y)
            if cell is not None:
                yield (x, y, cell)


class Player:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        return "<{} x={} y={}>".format(self.type, self.x, self.y)


class ScenePlayer:
    def __init__(self, player: Player, scene: Scene):
        self.player = player
        self.scene = scene

    def get_reading_order(self):
        return self.player.y * self.scene.width + self.player.x

    def iter_nearby_cells(self):
        return self.scene.iter_nearby_cells((self.player.x, self.player.y))

    def walk(self):
        seen = {(self.player.x, self.player.y): 0}
        queue = deque([(self.player.x, self.player.y, self.player.type, 0)])

        while len(queue) > 0:
            current = queue.popleft()
            for x, y, cell in self.scene.iter_nearby_cells((current[0], current[1])):
                distance = current[3] + 1

                if cell != "#":
                    pos = (x, y)
                    if pos in seen and distance < seen[pos]:
                        seen[pos] = distance

                    if pos not in seen:
                        seen[pos] = distance
                        queue.append((x, y, cell, distance))

        for position, distance in sorted(seen.items(), key=lambda x: (x[1], x[0])):
            yield (position[0], position[1], self.scene[position], distance)

    def find_closest(self, cell_to_find):
        results = []
        for x, y, cell, distance in self.walk():
            if cell == cell_to_find and distance > 0:
                results.append((x, y, distance))

            if len(results) == 2:
                break


def main():
    input_text = """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########""".strip()

    scene = Scene.parse(input_text)
    players = [ScenePlayer(player, scene) for player in scene.iter_cells("EG", Player)]
    print(players[4].player)
    distance_scene = Scene.parse(input_text)
    for x, y, cell, distance in players[4].walk():
        distance_scene[x, y] = str(distance)
        print(x, y, cell, distance)

    distance_scene.print()


if __name__ == "__main__":
    main()
