import sys
from itertools import cycle

def first_revisit(changes, start=0):
    visited = {}
    current = start

    for val in cycle(changes):
        if current in visited:
            return current
        visited[current] = True
        current += val


if __name__ == '__main__':
    file_name = 'input.txt'
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, 'rU') as f:
        lines = f.read().strip().split('\n')

    changes = (int(val) for val in lines)

    result = first_revisit(changes)
    print(result)
