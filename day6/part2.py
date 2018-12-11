import sys
from typing import List
from part1 import parse_point, Point, Site, manhattan_distance


def rate_distances(sites: List[Site]) -> List[List[int]]:
    right = max(site.p.x for site in sites)
    bottom = max(site.p.y for site in sites)

    grid = [[0 for x in range(right + 1)] for y in range(bottom + 1)]
    for y in range(bottom + 1):
        for x in range(right + 1):
            p = Point(x, y)
            rating = sum(manhattan_distance(p, site.p) for site in sites)
            grid[y][x] = rating

    return grid


def main():
    file_name = "input.txt"
    threshold = 10000
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
    if len(sys.argv) >= 3:
        threshold = int(sys.argv[2])

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    points = [parse_point(line) for line in lines]
    sites = [Site(idx, p) for (idx, p) in enumerate(points)]
    rates = rate_distances(sites)

    # this just counts how many points in the grid are "safe"
    # it does not make sure the region is contiguous
    result = sum(1 if rating < threshold else 0 for row in rates for rating in row)
    print("Points with a rating less than {0}".format(threshold), result)


if __name__ == "__main__":
    main()
