import sys
from collections import namedtuple
from typing import List

Node = namedtuple("Node", ["children", "metadata"])


def build_tree(data: List[int], cursor_start=0) -> Node:
    cursor = cursor_start

    def parse_node(data: List[int]) -> Node:
        nonlocal cursor

        node = Node(children=[], metadata=[])

        n_children = data[cursor]
        n_metadata = data[cursor + 1]

        cursor = cursor + 2

        for x in range(n_children):
            child = parse_node(data)
            node.children.append(child)

        metadata = data[cursor : cursor + n_metadata]
        for m in metadata:
            node.metadata.append(m)

        cursor = cursor + n_metadata

        return node

    return parse_node(data)


def sum_metadata(node: Node) -> int:
    return sum(node.metadata) + sum(sum_metadata(child) for child in node.children)


def main():
    file_name = "input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        data = [int(d) for d in f.read().strip().split(" ")]

    root = build_tree(data)

    result = sum_metadata(root)
    print(result)


if __name__ == "__main__":
    main()
