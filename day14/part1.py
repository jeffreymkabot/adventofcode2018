import sys
import os.path
from typing import List, Iterator


def child_recipes(a: int, b: int) -> List[int]:
    z = a + b
    if z < 10:
        return [z]
    return [1, z % 10]


def simulation() -> Iterator[List[int]]:
    recipes = [3, 7]
    elf_a = 0
    elf_b = 1

    while True:
        a, b = recipes[elf_a], recipes[elf_b]
        recipes.extend(child_recipes(a, b))

        elf_a = (elf_a + a + 1) % len(recipes)
        elf_b = (elf_b + b + 1) % len(recipes)
        yield recipes


def main():
    n = int(sys.argv[1])
    sim = simulation()
    recipes = []
    while len(recipes) < n + 10:
        recipes = next(sim)

    next_ten = recipes[n : n + 10]
    print("".join(str(r) for r in next_ten))


if __name__ == "__main__":
    main()
