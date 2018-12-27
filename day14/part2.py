import sys
import os.path
from part1 import simulation
from typing import List


def subsequence(search: List, seq: List) -> bool:
    """Determine if seq is a subsequence of search, starting at index 0.
    """
    return len(search) >= len(seq) and all(x == y for (x, y) in zip(search, seq))


def main():
    sequence = [int(c) for c in sys.argv[1]]
    n = len(sequence)
    sim = simulation()

    recipes = []
    result = None
    while result is None:
        recipes = next(sim)
        # only one or two recipes are added each iteration
        # so we can just check for a subsequence starting at two positions
        if subsequence(recipes[-n:], sequence):
            result = len(recipes) - n
        if subsequence(recipes[-n - 1 :], sequence):
            result = len(recipes) - n - 1

    print(result)


if __name__ == "__main__":
    main()
