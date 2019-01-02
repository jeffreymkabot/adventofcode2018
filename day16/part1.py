import sys
import os.path
import re
from collections import defaultdict, namedtuple
from typing import Dict, DefaultDict, Set, Callable, List

Op = Callable[[List[int], int, int, int], None]


def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]


def addi(reg, a, b, c):
    reg[c] = reg[a] + b


def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]


def muli(reg, a, b, c):
    reg[c] = reg[a] * b


def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]


def bani(reg, a, b, c):
    reg[c] = reg[a] & b


def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]


def bori(reg, a, b, c):
    reg[c] = reg[a] | b


def setr(reg, a, b, c):
    reg[c] = reg[a]


def seti(reg, a, b, c):
    reg[c] = a


def gtir(reg, a, b, c):
    reg[c] = 1 if a > reg[b] else 0


def gtri(reg, a, b, c):
    reg[c] = 1 if reg[a] > b else 0


def gtrr(reg, a, b, c):
    reg[c] = 1 if reg[a] > reg[b] else 0


def eqir(reg, a, b, c):
    reg[c] = 1 if a == reg[b] else 0


def eqri(reg, a, b, c):
    reg[c] = 1 if reg[a] == b else 0


def eqrr(reg, a, b, c):
    reg[c] = 1 if reg[a] == reg[b] else 0


ops = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]


sample_re = r"Before: \[(\d+, \d+, \d+, \d+)\]\n(\d+ \d+ \d+ \d+)\nAfter:  \[(\d+, \d+, \d+, \d+)\]"
program_re = re.compile(r"\n\n\n\n(\d+ \d+ \d+ \d+\n?)+")

Sample = namedtuple("Sample", ["before", "instruction", "after"])


def identify_opcodes(opcode_candidates: Dict[int, Set[Op]]) -> Dict[int, Op]:
    """Identify the function object corresponding to each opcode.

    Until all opcodes are identified:
    1. Find opcodes with only one candidate function
    2. Eliminate those functions as candidates from other opcodes
    """
    while any(len(matches) > 1 for matches in opcode_candidates.values()):
        identified = [
            matches.copy().pop()
            for matches in opcode_candidates.values()
            if len(matches) == 1
        ]
        for matches in opcode_candidates.values():
            if len(matches) > 1:
                for x in identified:
                    matches.discard(x)

    return {opcode: matches.pop() for (opcode, matches) in opcode_candidates.items()}


def main():
    file_name = os.path.dirname(__file__) + "/input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        inp = f.read()

    sample_texts = re.findall(sample_re, inp)
    samples = [
        Sample(
            before=[int(x) for x in sp[0].split(", ")],
            instruction=[int(x) for x in sp[1].split(" ")],
            after=[int(x) for x in sp[2].split(", ")],
        )
        for sp in sample_texts
    ]

    program_text = program_re.search(inp)
    instructions = [
        [int(x) for x in line.split(" ")]
        for line in program_text.group(0).strip().split("\n")
    ]

    # map opcodes to a set of candidate function objects
    opcode_candidates = defaultdict(set)
    samples_matching_three_or_more_opcodes = 0

    for s in samples:
        opcode, a, b, c, = s.instruction
        matching_ops = 0
        for op in ops:
            reg = s.before.copy()
            op(reg, a, b, c)

            if all(x == y for (x, y) in zip(reg, s.after)):
                opcode_candidates[opcode].add(op)
                matching_ops += 1

        if matching_ops >= 3:
            samples_matching_three_or_more_opcodes += 1

    print(
        "Number of samples matching behavior of three or more ops: ",
        samples_matching_three_or_more_opcodes,
    )

    opcode_dict = identify_opcodes(opcode_candidates)

    reg = [0, 0, 0, 0]
    for instr in instructions:
        opcode, a, b, c = instr
        if opcode in opcode_dict:
            opcode_dict[opcode](reg, a, b, c)

    print("Registers", reg)


if __name__ == "__main__":
    main()
