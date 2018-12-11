#!/usr/bin/python3


def calc(x, y, serial):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    hundreds = (power // 100) % 10
    power_level = hundreds - 5

    return power_level


def solve_rect(grid, size):
    sums = []
    for x in range(300 - size):
        for y in range(300 - size):
            value = 0
            for offset_x in range(size):
                for offset_y in range(size):
                    value += grid[x + offset_x][y + offset_y]
            sums.append((x + 1, y + 1, value))

    return max(sums, key=lambda x: x[2])

def solve(serial):
    grid = [[0] * 300 for _ in range(300)]

    for x in range(300):
        for y in range(300):
            grid[x][y] = calc(x + 1, y + 1, serial)

    max_sol = None
    for size in range(3, 35):
        sol = solve_rect(grid, size)
        if max_sol is None or max_sol[2] < sol[2]:
            max_sol = sol
        print(size, sol)

    return max_sol


def main():
    print(solve(8979))


#    print(calc(3, 5, 8))
#    print(solve(18))


if __name__ == "__main__":
    main()
