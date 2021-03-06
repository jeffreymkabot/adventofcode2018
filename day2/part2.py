import sys
from typing import List, Tuple


def which_pair(box_ids: List[str]) -> Tuple[str, str]:
    pairs = ((x, y) for x in box_ids for y in box_ids if x != y)
    return next((x, y) for (x, y) in pairs if boxes_match(x, y))


def shared_letters(pair: Tuple[str, str]):
    return "".join(c1 for (c1, c2) in zip(*pair) if c1 == c2)


def boxes_match(box1: str, box2: str) -> bool:
    char_pairs = zip(box1, box2)
    diffs = 0
    for (c1, c2) in char_pairs:
        if diffs > 1:
            return False
        diffs += 0 if c1 == c2 else 1

    return diffs == 1


if __name__ == "__main__":
    file_name = "input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    result = shared_letters(which_pair(lines))
    print(result)
