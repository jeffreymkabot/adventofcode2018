import sys
import re
from collections import namedtuple
from typing import Dict, List
from part1 import parse_edge, is_root

Job = namedtuple("Job", ["vertex", "time_done"])


def simulate(graph: Dict[str, List[str]], workers: int, base_cost: int) -> int:
    roots = [v for v in graph.keys() if is_root(v, graph)]
    jobs_in_progress: List[Job] = []
    idle_workers = workers

    now = 0

    while len(roots) > 0 or len(jobs_in_progress) > 0:
        for job in jobs_in_progress:
            if now >= job.time_done:
                jobs_in_progress.remove(job)
                idle_workers += 1

                A = job.vertex
                children = graph.get(A, [])
                for B in sorted(children):
                    children.remove(B)
                    if is_root(B, graph):
                        roots.append(B)

        roots.sort()
        while idle_workers > 0 and len(roots) > 0:
            A = roots.pop(0)
            cost = base_cost + added_cost(A)
            job = Job(vertex=A, time_done=now + cost)

            jobs_in_progress.append(job)
            idle_workers -= 1

        now += 1 if len(roots) > 0 or len(jobs_in_progress) > 0 else 0
    return now


def added_cost(vertex: str) -> int:
    first_letter = vertex[0].upper()
    return ord(first_letter) - ord("A") + 1


def main():
    file_name = "input.txt"
    workers = 5
    base_cost = 60
    if len(sys.argv) >= 2:
        file_name = sys.argv[1]
    if len(sys.argv) >= 3:
        workers = int(sys.argv[2])
    if len(sys.argv) >= 4:
        base_cost = int(sys.argv[3])

    with open(file_name, "rU") as f:
        lines = f.read().strip().split("\n")

    edges = [parse_edge(line) for line in lines]

    graph = {}
    for (A, B) in edges:
        # make sure there is an entry for each vertex, even if it has no children
        graph[B] = graph.get(B, [])
        graph[A] = graph.get(A, []) + [B]

    result = simulate(graph, workers, base_cost)
    print(result)


if __name__ == "__main__":
    main()
