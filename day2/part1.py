import sys
from collections import Counter


def checksum(box_ids):
    counts = [Counter(box_id).values() for box_id in box_ids]
    num_two_letter = len([c for c in counts if 2 in c])
    num_three_letter = len([c for c in counts if 3 in c])
    return num_two_letter * num_three_letter


if __name__ == "__main__":
    file_name = "input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    result = checksum(lines)
    print(result)
