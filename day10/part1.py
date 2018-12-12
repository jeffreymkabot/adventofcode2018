import sys
import re
import math
from time import sleep
from collections import namedtuple
from typing import List, Iterator, Tuple

point_re = re.compile(
    r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>"
)

Point = namedtuple("Point", ["x", "y", "vx", "vy"])


def parse_point(line: str) -> Point:
    match = point_re.match(line)
    if not match:
        raise ValueError
    return Point(
        x=int(match.group(1)),
        y=int(match.group(2)),
        vx=int(match.group(3)),
        vy=int(match.group(4)),
    )


def simulation(points: List[Point]):
    while True:
        yield points[:]
        points = [Point(p.x + p.vx, p.y + p.vy, p.vx, p.vy) for p in points]


def find_range_ys_local_min(
    sim: Iterator[List[Point]], max_iterations=1000000
) -> Tuple[int, List[Point]]:
    """Return the iteration after which the range of y-values starts increasing.
    """
    points: List[Point] = []
    range_ys = math.inf

    for second in range(max_iterations):
        next_points = next(sim)
        next_range_ys = abs(
            max(p.y for p in next_points) - min(p.y for p in next_points)
        )
        if next_range_ys > range_ys:
            return (second - 1, points)

        points = next_points
        range_ys = next_range_ys

    return (-1, [])


def print_grid(points: List[Point]):
    x_min = min(p.x for p in points)
    x_max = max(p.x for p in points)

    y_min = min(p.y for p in points)
    y_max = max(p.y for p in points)

    grid = [[" " for x in range(x_min, x_max + 1)] for y in range(y_min, y_max + 1)]
    for p in points:
        grid[p.y - y_min][p.x - x_min] = "#"

    for row in grid:
        print("".join(row))


def main():
    file_name = "input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    points = [parse_point(line) for line in lines]
    sim = simulation(points)

    (second, aligned_points) = find_range_ys_local_min(sim)
    print("Aligned at {0} seconds.".format(second))
    print_grid(aligned_points)


if __name__ == "__main__":
    main()
