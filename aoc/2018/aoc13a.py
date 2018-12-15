#!/usr/bin/python3


CART_CELLS = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}






class Matrix:
    def __init__(self, rows):
        self.data = rows

    @classmethod
    def parse(cls, input_text):
        lines = input_text.splitlines()
        width = max(map(len, lines))

        rows = []
        for line in lines:
            row = list(line)
            if len(row) < width:
                row.extend([" "] * (width - len(row)))
            rows.append(row)

        return cls(rows)

    def __setitem__(self, position, value):
        self.data[position[1]][position[0]] = value

    def __getitem__(self, position):
        return self.data[position[1]][position[0]]

    @property
    def width(self):
        return max(filter(len, self.data))

    @property
    def height(self):
        return len(self.data)

    def print(self):
        for row in self.data:
            print("".join(row))

    def __iter__(self):
        for y, row in enumerate(self.data):
            for x, cell in enumerate(row):
                yield (x, y, cell)

    def parse_carts(self):
        carts = []
        for x, y, cell in self:
            if cell in CART_CELLS:
                carts.append(Cart(x, y, cell))

        return carts


class Cart:
    def __init__(self, x, y, face):
        self.x = x
        self.y = y
        self.face = face
        self.original_face = self.get_original_face()

    def get_original_face(self):
        if self.face in ("<", ">"):
            original_face = "-"
        elif self.face in ("v", "^"):
            original_face = "|"

        return original_face

    def move(self, matrix: Matrix):
        new_position = (self.x + CART_CELLS[self.face][0], self.y + CART_CELLS[self.face][1])
        new_cell = matrix[new_position]

        print(new_cell)

    def __repr__(self):
        return "<Cart x={x}, y={y}, face={face!r}>".format_map(self.__dict__)


def main():
    input_text = r"""
/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
""".strip()

    print(input_text)

    matrix = Matrix.parse(input_text)
    matrix.print()
    carts = matrix.parse_carts()
    carts[0].move(matrix)

if __name__ == "__main__":
    main()
