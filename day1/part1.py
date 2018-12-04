import sys

if __name__ == '__main__':
    file_name = 'input.txt'
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, 'rU') as f:
        lines = f.read().strip().split('\n')

    changes = (int(val) for val in lines)

    result = sum(changes)
    print(result)
