import sys
from typing import Iterable, List

def react(input_polymer: Iterable[str]) -> List[str]:
    stack = []
    reacted = False

    for unit in input_polymer:
        if len(stack) > 0 and will_react(stack[-1], unit):
            stack.pop()
            reacted = True
        else:
            stack.append(unit)

    if not reacted:
        return stack

    return react(stack)

_dist = abs(ord('a') - ord('A'))

def will_react(a: str, b: str) -> bool:
    return abs(ord(a) - ord(b)) == _dist


if __name__ == '__main__':
    file_name = 'input.txt'
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, 'rU') as f:
        input_polymer = (c for c in f.read().strip())

    polymer = react(input_polymer)

    result = len(polymer)
    print(result)
