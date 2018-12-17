import sys
import os.path
from part1 import State, parse_initial_state, parse_rules, simulate, sum_state
from typing import List, Tuple
from statistics import mean, variance

Sample = Tuple[int, int]


def hash_state(state: State) -> str:
    """Create a string representing the pattern of plants
    **starting at the first plant and ending at the last plant**.
    """
    left = min(k for k in state.keys() if state[k] == "#")
    right = max(k for k in state.keys() if state[k] == "#")

    order = sorted(state.keys())[left : right + 1]
    return "".join(state[pot] for pot in order)


def linear_regression(samples: List[Sample]) -> Tuple[float, float]:
    """Linear regression
    https://en.wikipedia.org/wiki/Simple_linear_regression
    """
    xs = [s[0] for s in samples]
    ys = [s[1] for s in samples]
    x_mean = mean(xs)
    y_mean = mean(ys)
    cov = sum((x - x_mean) * (y - y_mean) for (x, y) in samples)
    var = sum((x - x_mean) ** 2 for x in xs)
    coeff = cov / var
    intercept = y_mean - coeff * x_mean
    return (coeff, intercept)


def main():
    file_name = os.path.dirname(__file__) + "/input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    initial_state = parse_initial_state(lines[0])
    rules = parse_rules(lines[2:])

    # find where the plant pattern starts to repeat (though maybe not starting at the same index)
    # sample the generation number (x) and the sum of plant pots (y)
    # assume a linear relationship and extrapolate for the 50 billionth generation
    found_cycle = False
    hashes = []
    samples = []
    sim = simulate(initial_state, rules)
    for x in range(1, 1000):
        gen = next(sim)
        h = hash_state(gen)
        found_cycle = h in hashes
        if not found_cycle:
            hashes.append(h)
        else:
            samples.append((x, sum_state(gen)))

    if not found_cycle:
        print("No cycles")
        return

    coeff, intercept = linear_regression(samples)
    result = int(coeff * 50_000_000_000 + intercept)
    print(result)


if __name__ == "__main__":
    main()
