import sys

def which_pair(box_ids):
    pairs = ((x, y) for x in box_ids for y in box_ids if x != y)
    wanted_pair = next(p for p in pairs if boxes_match(*p))

    shared_letters = (c1 for (c1, c2) in zip(*wanted_pair) if c1 == c2)
    return ''.join(shared_letters)

def boxes_match(box1: str, box2: str):
    char_pairs = zip(box1, box2)
    diffs = 0
    for (c1, c2) in char_pairs:
        if diffs > 1:
            return False
        diffs += 0 if c1 == c2 else 1

    return diffs == 1


if __name__ == '__main__':
    file_name = 'input.txt'
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, 'rU') as f:
        lines = f.read().strip().split('\n')

    result = which_pair(lines)
    print(result)
