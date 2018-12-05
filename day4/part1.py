import sys
import re
from typing import List, Dict
from statistics import mode

guard_re = re.compile(r'Guard #(\d+) begins shift')
# all asleep/awake times are during the midnight hour
asleep_re = re.compile(r'00:(\d\d)\] falls asleep')
awake_re = re.compile(r'00:(\d\d)\] wakes up')

def sleep_times(lines: List[str]) -> Dict[int, List[int]]:
    """Map guard ids to a list of the minutes the guard is asleep.
    """
    guards = {}
    current_guard = None
    asleep_at = None

    for line in lines:
        guard_match = guard_re.search(line)
        if guard_match is not None:
            current_guard = int(guard_match.group(1))
            asleep_at = None
            continue

        asleep_match = asleep_re.search(line)
        if asleep_match is not None:
            asleep_at = int(asleep_match.group(1))
            continue

        awake_match = awake_re.search(line)
        if (
            awake_match is not None
            and asleep_at is not None
            and current_guard is not None
        ):
            awake_at = int(awake_match.group(1))
            minutes_asleep = list(range(asleep_at, awake_at))
            asleep_at = None

            if current_guard not in guards:
                guards[current_guard] = []

            guards[current_guard] += minutes_asleep
            continue

    return guards


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

    most_asleep_guard, minutes_asleep = max(
        guards.items(),
        key=lambda item: len(item[1])
    )
    most_asleep_minute = mode(minutes_asleep)
    print('Most asleep guard:', most_asleep_guard)
    print('His most common minute:', most_asleep_minute)

    result = most_asleep_guard * most_asleep_minute
    print(result)
