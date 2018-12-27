import sys
import os.path
from part1 import Track


class Track2(Track):
    def after_cart_moves(self, cart):
        # might have been removed in the after_cart_moves of another cart earlier this tick
        if cart not in self.carts:
            return

        if len(self.carts) == 1:
            raise StopIteration(cart.pos)

        for other in self.carts:
            if other is not cart and cart.pos == other.pos:
                self.carts.remove(other)
                self.carts.remove(cart)
                return


def main():
    file_name = os.path.dirname(__file__) + "/input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().split("\n")

    grid = {(x, y): c for y, row in enumerate(lines) for x, c in enumerate(row)}
    track = Track2(grid)

    tick = 0
    while True:
        tick += 1
        try:
            next(track)
        except StopIteration as exc:
            print("Last cart at {0} after tick {1}".format(exc.value, tick))
            break


if __name__ == "__main__":
    main()
