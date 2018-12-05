import sys
import re
from collections import namedtuple
from typing import List

Claim = namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])

claim_re = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

_overlap = 'X'

def parse_claim(line: str) -> Claim:
    match = claim_re.match(line)
    if match is None:
        return None
    return Claim(
        id=match.group(1),
        left=int(match.group(2)),
        top=int(match.group(3)),
        width=int(match.group(4)),
        height=int(match.group(5)),
    )

def apply_claim(c: Claim, grid: List[List[str]]):
    for y in range(c.top, c.top + c.height):
        for x in range(c.left, c.left + c.width):
            if grid[y][x] is None:
                grid[y][x] = c.id
            else:
                grid[y][x] = _overlap

def count_overlaps(grid: List[List[str]]) -> int:
    return sum(row.count(_overlap) for row in grid)

def print_grid(grid: List[List[str]]):
    for row in grid:
        print(['.' if p is None else p for p in row])


if __name__ == '__main__':
    file_name = 'input.txt'
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, 'rU') as f:
        lines = f.read().strip().split('\n')

    claims = [parse_claim(line) for line in lines]

    width = max(c.left + c.width for c in claims)
    height = max(c.top + c.height for c in claims)

    # NB: producing the grid as [[None] * width] * height
    # caused [None] * width to be copied by reference
    grid = [[None for x in range(width)] for y in range(height)]

    for c in claims:
        apply_claim(c, grid)

    result = count_overlaps(grid)
    print(result)
