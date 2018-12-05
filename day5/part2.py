import sys
from part1 import react

if __name__ == '__main__':
    file_name = 'input.txt'
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, 'rU') as f:
        input_polymer = [c for c in f.read().strip()]

    types = frozenset(unit.lower() for unit in input_polymer)

    # map a unit type to the length of the reacted polymer
    # that results when the type is removed
    polymer_lengths = {}
    for t in types:
        without_t = filter(
            lambda u: u != t.lower() and u != t.upper(),
            input_polymer
        )
        polymer_lengths[t] = len(react(without_t))

    result = min(polymer_lengths.values())
    print(result)

