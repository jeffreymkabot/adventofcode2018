import sys
from collections import namedtuple
from typing import List
from part1 import Node, build_tree


def node_value(node: Node) -> int:
    if len(node.children) == 0:
        return sum(node.metadata)

    # metadata references are 1-indexed
    # 1 refers to first child, 2 refers to second child, etc.
    refs = (
        node.children[i - 1]
        for i in node.metadata
        if i >= 1 and i <= len(node.children)
    )
    return sum(node_value(n) for n in refs)


def main():
    file_name = "input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        data = [int(d) for d in f.read().strip().split(" ")]

    root = build_tree(data, 0)

    result = node_value(root)
    print(result)


if __name__ == "__main__":
    main()
