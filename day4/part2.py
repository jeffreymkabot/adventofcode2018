import sys
from collections import Counter
from statistics import mode
from part1 import sleep_times

if __name__ == '__main__':
    file_name = 'input.txt'
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, 'rU') as f:
        lines = f.read().strip().split('\n')

    # timestamps are YYYY-MM-DD hh:mm
    # lexicographic sort will put lines in chronological order
    lines.sort()

    guards = sleep_times(lines)

    most_frequent_guard, minutes_asleep = max(
        guards.items(),
        key=lambda item: max(
            Counter(item[1]).values()
        )
    )
    most_frequent_minute = mode(minutes_asleep)
    print('Most frequent guard:', most_frequent_guard)
    print('His most common minute:', most_frequent_minute)

    result = most_frequent_guard * most_frequent_minute
    print(result)
