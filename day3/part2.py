import sys
from part1 import Claim, Grid, parse_claim, apply_claim


def claim_intact(c: Claim, grid: Grid) -> bool:
    return all(
        grid[y][x] == c.id
        for y in range(c.top, c.top + c.height)
        for x in range(c.left, c.left + c.width)
    )


if __name__ == "__main__":
    file_name = "input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    claims = [parse_claim(line) for line in lines]

    width = max(c.left + c.width for c in claims)
    height = max(c.top + c.height for c in claims)

    # NB: producing the grid as [[None] * width] * height
    # caused [None] * width to be copied by reference
    grid: Grid = [[None for x in range(width)] for y in range(height)]

    for c in claims:
        apply_claim(c, grid)

    result = next(c.id for c in claims if claim_intact(c, grid))
    print(result)
