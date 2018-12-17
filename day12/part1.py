import sys
import os.path
import re
from collections import defaultdict
from typing import List, DefaultDict, Iterator

initial_state_re = re.compile(r"initial state: ([.#]+)")
rule_re = re.compile(r"([.#]+) => ([.#])")

State = DefaultDict[int, str]
"""Represent a configuration of plants by mapping index to "#" if the pot has a plant, else ".".
"""

Rules = DefaultDict[str, str]
"""Represent the generation rules by mapping a sequence of five pots
to "#" if the center pot has a plant, else ".".
"""


def parse_initial_state(line: str) -> State:
    initial_state: State = defaultdict(lambda: ".")

    match = initial_state_re.match(line)
    if not match:
        raise ValueError

    for idx, c in enumerate(match.group(1)):
        initial_state[idx] = c

    return initial_state


def parse_rules(lines: List[str]) -> Rules:
    rules: Rules = defaultdict(lambda: ".")

    for line in lines:
        match = rule_re.search(line)
        if not match:
            raise ValueError

        rules[match.group(1)] = match.group(2)
    return rules


def simulate(initial_state: State, rules: Rules) -> Iterator[State]:
    """Produce an iterator yielding successive generations of plants.
    """
    prev_state = initial_state.copy()
    while True:
        state = prev_state.copy()
        left = min(k for k in state.keys() if state[k] == "#")
        right = max(k for k in state.keys() if state[k] == "#")

        for pot in range(left - 2, right + 3):
            sequence = "".join(prev_state[p] for p in range(pot - 2, pot + 3))
            state[pot] = rules[sequence]

        yield state
        prev_state = state


def sum_state(state: State) -> int:
    return sum(p for p in state.keys() if state[p] == "#")


def main():
    file_name = os.path.dirname(__file__) + "/input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    initial_state = parse_initial_state(lines[0])
    rules = parse_rules(lines[2:])

    sim = simulate(initial_state, rules)
    for x in range(20):
        gen = next(sim)

    result = sum(gen)
    print(result)


if __name__ == "__main__":
    main()
