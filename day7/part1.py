import sys
import re
from typing import Dict, List, Tuple

edge_re = re.compile(r"Step (\w+) must be finished before step (\w+) can begin.")


def parse_edge(line: str) -> Tuple[str, str]:
    match = edge_re.match(line)
    if not match:
        raise ValueError
    return (match.group(1), match.group(2))


def is_root(vertex: str, graph: Dict[str, List[str]]):
    """A vertex is a root vertex if it has no incoming edges.
    """
    return all(vertex not in x for x in graph.values())


def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
    """
    out = []
    roots = [A for A in graph.keys() if is_root(A, graph)]

    while len(roots) > 0:
        roots.sort()
        A = roots.pop(0)
        out.append(A)

        children = graph.get(A, [])
        for B in sorted(children):
            children.remove(B)
            if is_root(B, graph):
                roots.append(B)

    return out


def main():
    file_name = "input.txt"
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    edges = [parse_edge(line) for line in lines]

    graph = {}
    for (A, B) in edges:
        # make sure there is an entry for each vertex, even if it has no children
        graph[B] = graph.get(B, [])
        graph[A] = graph.get(A, []) + [B]

    order = topological_sort(graph)
    result = "".join(order)
    print(result)


if __name__ == "__main__":
    main()
