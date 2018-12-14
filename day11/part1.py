import sys
from collections import defaultdict
from typing import List, Tuple

Grid = List[List[int]]

N = 300


def power_level(serial: int, x: int, y: int) -> int:
    """Compute the power level of the fuel cell at x, y.
    """
    rack_id = x + 10
    p = rack_id * y + serial
    p *= rack_id
    p = (p // 100) % 10
    return p - 5


def power_grid(serial: int) -> Grid:
    """Compute the power level of fuel cells in a 300x300 grid.
    The grid is 0-indexed.
    """
    return [[power_level(serial, x + 1, y + 1) for x in range(N)] for y in range(N)]


def window_power_level(base_grid: Grid, left: int, top: int, window: int) -> int:
    """Compute the sum of power levels in a square window of a given size staring at (left, top).
    """
    return sum(
        base_grid[y][x]
        for x in range(left, left + window)
        for y in range(top, top + window)
    )


def window_power_grid(serial: int, window: int) -> Grid:
    """Compute all windowed power levels of a given size.
    """
    base_grid = power_grid(serial)
    return [
        [window_power_level(base_grid, x, y, window) for x in range(N - window + 1)]
        for y in range(N - window + 1)
    ]


def max_power_window(grid: Grid):
    """Find the coordinate of the maximum power in a grid.
    For a windowed power grid this is the top-left corner.
    """
    power_levels = (
        (x, y, p) for (y, row) in enumerate(grid) for (x, p) in enumerate(row)
    )
    return max(power_levels, key=lambda t: t[2])


def main():
    serial = 0
    if len(sys.argv) >= 2:
        serial = int(sys.argv[1])

    grid = window_power_grid(serial, 3)
    x, y, p = max_power_window(grid)
    print("Max total power {0} at {1}".format(p, (x + 1, y + 1)))


if __name__ == "__main__":
    main()
