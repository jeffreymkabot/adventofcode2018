import sys
from collections import namedtuple
from typing import List, Dict, Set, Optional

Point = namedtuple("Point", ["x", "y"])


Site = namedtuple("Site", ["label", "p"])
"""Site is a point with an integer label.
"""


def parse_point(line: str) -> Point:
    parts = line.split(",")
    if len(parts) < 2:
        raise ValueError
    return Point(int(parts[0]), int(parts[1]))


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def nearest_site(p: Point, sites: List[Site]) -> Optional[Site]:
    """Find the nearest site to a point using manhattan distance.
    Returns None if the nearest sites are equally distant.
    """
    distances = map(lambda site: (site, manhattan_distance(p, site.p)), sites)
    nearest_two = sorted(distances, key=lambda d: d[1])[0:2]
    return nearest_two[0][0] if nearest_two[0][1] != nearest_two[1][1] else None


def neighborhood_sizes(sites: List[Site]) -> Dict[int, int]:
    """Return a dictionary mapping site labels to the size of their neighborhoods.
    The neighborhood of a site is the set of points for which the site is the nearest out of all sites.
    Sites with infinite neighborhoods are excluded.
    """
    right = max(site.p.x for site in sites)
    bottom = max(site.p.y for site in sites)

    perimeter = set(
        [Point(0, y) for y in range(bottom + 1)]
        + [Point(right, y) for y in range(bottom + 1)]
        + [Point(x, 0) for x in range(right + 1)]
        + [Point(x, bottom) for x in range(right + 1)]
    )

    # site has infinite area if it is the nearest site to any point on the perimeter
    sites_with_infinite_area: Set[Site] = set()
    for p in perimeter:
        nearest = nearest_site(p, sites)
        if nearest is not None:
            sites_with_infinite_area.add(nearest)

    sizes: Dict[int, int] = {}

    for y in range(bottom + 1):
        for x in range(right + 1):
            nearest = nearest_site(Point(x, y), sites)
            if nearest is not None and nearest not in sites_with_infinite_area:
                sizes[nearest.label] = sizes.get(nearest.label, 0) + 1

    return sizes


def main():
    file_name = "input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    points = [parse_point(line) for line in lines]
    sites = [Site(idx, p) for (idx, p) in enumerate(points)]

    sizes = neighborhood_sizes(sites)
    print("Neighborhood sizes", sizes)

    result = max(sizes.values())
    print("Largest neighborhood", result)


if __name__ == "__main__":
    main()
