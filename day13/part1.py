import sys
import os.path
from itertools import cycle

# use complex numbers to make it easy to rotate headings
EAST = 1 + 0j
NORTH = 0 - 1j
WEST = -1 + 0j
SOUTH = 0 + 1j

arrows = {">": (EAST, "-"), "^": (NORTH, "|"), "<": (WEST, "-"), "v": (SOUTH, "|")}


class Cart:
    def __init__(self, pos, heading):
        self.pos = pos
        self.heading = heading
        self.intersection_rotations = cycle([0 - 1j, 1, 0 + 1j])

    def rotate_intersection(self):
        self.heading *= next(self.intersection_rotations)

    def rotate_left(self):
        self.heading *= 0 - 1j

    def rotate_right(self):
        self.heading *= 0 + 1j


class Track:
    def __init__(self, grid):
        self.carts = []
        self.grid = grid
        for pos, c in grid.items():
            if c in arrows:
                heading, pipe = arrows[c]
                cart = Cart(pos, heading)
                self.carts.append(cart)
                self.grid[pos] = pipe

    def __iter__(self):
        return self

    def after_cart_moves(self, cart):
        for other in self.carts:
            if other is not cart and cart.pos == other.pos:
                raise StopIteration(cart.pos)

    def __next__(self):
        if len(self.carts) == 0:
            raise StopIteration("No carts")

        # sort from top-to-bottom, left-to-right
        self.carts.sort(key=lambda c: (c.pos[1], c.pos[0]))

        for cart in self.carts[:]:
            next_pos = (
                cart.pos[0] + int(cart.heading.real),
                cart.pos[1] + int(cart.heading.imag),
            )
            next_tile = self.grid[next_pos]
            cart.pos = next_pos

            self.after_cart_moves(cart)

            if next_tile == "+":
                cart.rotate_intersection()
            elif next_tile == "\\":
                if cart.heading == NORTH or cart.heading == SOUTH:
                    cart.rotate_left()
                else:
                    cart.rotate_right()
            elif next_tile == "/":
                if cart.heading == NORTH or cart.heading == SOUTH:
                    cart.rotate_right()
                else:
                    cart.rotate_left()

        return self.carts


def main():
    file_name = os.path.dirname(__file__) + "/input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().split("\n")

    grid = {(x, y): c for y, row in enumerate(lines) for x, c in enumerate(row)}
    track = Track(grid)

    tick = 0
    while True:
        tick += 1
        try:
            next(track)
        except StopIteration as exc:
            print("Collision at {0} on tick {1}".format(exc.value, tick))
            break


if __name__ == "__main__":
    main()
