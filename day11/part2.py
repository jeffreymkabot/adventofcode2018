import sys
from part1 import Grid, N, power_grid, max_power_window
from typing import List, Tuple, Dict

Cache = Dict[Tuple[int, int], int]
"""Cache the sum of the bottom and right edges of ending at (x, y).
(x, y) -> partial sum
"""


def window_power_level(
    base_grid: Grid,
    prev_grid: Grid,
    prev_partials: Cache,
    current_partials: Cache,
    left: int,
    top: int,
    window: int,
) -> int:
    """Compute the sum of power levels in a square window of a given size starting at (left, top).
    Optimized by using partial sums previously calculated for smaller windows.

    The sum for a window of size w starting at (left, top) is divided into four parts that were already computed:
        a. the window of size w-1 starting at (left, top)
        b. top-right cell
        c. bottom-left cell
        d. the bottom and right edges for the window of size w-1 starting at (left+1, top+1)

    Region b and c come from the baseline grid.
    Region a and d were computed for windows of size w-1.

    E.g, For a 4x4 window
    a a a b
    a a a d
    a a a d
    c d d d
    """
    prev_sum = prev_grid[top][left]

    right = left + window - 1
    bottom = top + window - 1
    prev_partial = prev_partials[(right, bottom)]

    partial = prev_partial + base_grid[top][right] + base_grid[bottom][left]
    current_partials[(right, bottom)] = partial

    return prev_sum + partial


def window_power_grid(
    base_grid: Grid, prev_grid: Grid, prev_partials: Cache, window: int
) -> Tuple[Grid, Cache]:
    """Compute all windowed power levels of a given size.
    Returns the grid and a dictionary of partial sums described in window_power_level.
    """
    current_partials: Cache = {}
    return (
        [
            [
                window_power_level(
                    base_grid, prev_grid, prev_partials, current_partials, x, y, window
                )
                for x in range(N - window + 1)
            ]
            for y in range(N - window + 1)
        ],
        current_partials,
    )


def max_power_window_size(serial: int, max_window=N):
    """Find the window size and coordinate that provides the maximum power level.
    """
    base_grid = power_grid(serial)

    prev_grid = base_grid
    prev_partials = {(x, y): base_grid[y][x] for x in range(N) for y in range(N)}

    x_max, y_max, p_max = max_power_window(base_grid)
    w_max = 1

    for window in range(2, max_window + 1):
        print("Window size", window)
        grid, partials = window_power_grid(base_grid, prev_grid, prev_partials, window)
        prev_grid, prev_partials = grid, partials
        x, y, p = max_power_window(grid)
        if p > p_max:
            x_max, y_max, p_max, w_max = x, y, p, window

    return x_max, y_max, p_max, w_max


def main():
    serial = 0
    if len(sys.argv) >= 2:
        serial = int(sys.argv[1])

    x, y, p, w = max_power_window_size(serial)
    print(
        "Max total power {0} at {1} with window size {2}".format(p, (x + 1, y + 1), w)
    )


if __name__ == "__main__":
    main()
