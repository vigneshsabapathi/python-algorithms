"""
A* Search Algorithm - Optimized Variants with Benchmarks.

Variant 1: Standard A* with heapq (baseline)
Variant 2: A* with closed set optimization (avoids re-expanding)
Variant 3: Bidirectional A* (search from both ends)
Variant 4: Weighted A* (epsilon-weighted heuristic for faster suboptimal paths)

>>> graph = {
...     "A": [("B", 1), ("C", 4)],
...     "B": [("C", 2), ("D", 5)],
...     "C": [("D", 1)],
...     "D": [],
... }
>>> h = {"A": 5, "B": 3, "C": 1, "D": 0}
>>> a_star_standard(graph, "A", "D", h)
(['A', 'B', 'C', 'D'], 4)
>>> a_star_closed_set(graph, "A", "D", h)
(['A', 'B', 'C', 'D'], 4)
>>> a_star_weighted(graph, "A", "D", h, epsilon=1.5)
(['A', 'B', 'C', 'D'], 4)
"""

import heapq
import time
from math import inf


# --- Variant 1: Standard A* (baseline) ---
def a_star_standard(
    graph: dict[str, list[tuple[str, int]]],
    start: str,
    goal: str,
    heuristic: dict[str, float],
) -> tuple[list[str], float]:
    """
    Standard A* with heapq priority queue.

    >>> g = {"X": [("Y", 3)], "Y": [("Z", 2)], "Z": []}
    >>> a_star_standard(g, "X", "Z", {"X": 5, "Y": 2, "Z": 0})
    (['X', 'Y', 'Z'], 5)
    """
    if start == goal:
        return [start], 0

    open_set = [(heuristic.get(start, 0), start)]
    came_from: dict[str, str] = {}
    g_score: dict[str, float] = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = _reconstruct(came_from, current, start)
            return path, g_score[goal]

        for neighbor, weight in graph.get(current, []):
            tentative_g = g_score[current] + weight
            if tentative_g < g_score.get(neighbor, inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heapq.heappush(
                    open_set, (tentative_g + heuristic.get(neighbor, 0), neighbor)
                )

    return [], inf


# --- Variant 2: A* with closed set ---
def a_star_closed_set(
    graph: dict[str, list[tuple[str, int]]],
    start: str,
    goal: str,
    heuristic: dict[str, float],
) -> tuple[list[str], float]:
    """
    A* with a closed set to prevent re-expanding settled nodes.
    More efficient when many paths exist to the same node.

    >>> g = {"A": [("B", 1), ("C", 3)], "B": [("C", 1)], "C": []}
    >>> a_star_closed_set(g, "A", "C", {"A": 3, "B": 1, "C": 0})
    (['A', 'B', 'C'], 2)
    """
    if start == goal:
        return [start], 0

    open_set = [(heuristic.get(start, 0), start)]
    came_from: dict[str, str] = {}
    g_score: dict[str, float] = {start: 0}
    closed: set[str] = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return _reconstruct(came_from, current, start), g_score[goal]

        if current in closed:
            continue
        closed.add(current)

        for neighbor, weight in graph.get(current, []):
            if neighbor in closed:
                continue
            tentative_g = g_score[current] + weight
            if tentative_g < g_score.get(neighbor, inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                heapq.heappush(
                    open_set, (tentative_g + heuristic.get(neighbor, 0), neighbor)
                )

    return [], inf


# --- Variant 3: Weighted A* (epsilon-greedy) ---
def a_star_weighted(
    graph: dict[str, list[tuple[str, int]]],
    start: str,
    goal: str,
    heuristic: dict[str, float],
    epsilon: float = 1.5,
) -> tuple[list[str], float]:
    """
    Weighted A*: f(n) = g(n) + epsilon * h(n).
    Trades optimality for speed. Path cost <= epsilon * optimal cost.

    >>> g = {"A": [("B", 2), ("C", 5)], "B": [("C", 1)], "C": []}
    >>> a_star_weighted(g, "A", "C", {"A": 3, "B": 1, "C": 0}, epsilon=2.0)
    (['A', 'B', 'C'], 3)
    """
    if start == goal:
        return [start], 0

    open_set = [(epsilon * heuristic.get(start, 0), start)]
    came_from: dict[str, str] = {}
    g_score: dict[str, float] = {start: 0}
    closed: set[str] = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return _reconstruct(came_from, current, start), g_score[goal]

        if current in closed:
            continue
        closed.add(current)

        for neighbor, weight in graph.get(current, []):
            if neighbor in closed:
                continue
            tentative_g = g_score[current] + weight
            if tentative_g < g_score.get(neighbor, inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + epsilon * heuristic.get(neighbor, 0)
                heapq.heappush(open_set, (f, neighbor))

    return [], inf


# --- Variant 4: A* with tie-breaking ---
def a_star_tiebreak(
    graph: dict[str, list[tuple[str, int]]],
    start: str,
    goal: str,
    heuristic: dict[str, float],
) -> tuple[list[str], float]:
    """
    A* with tie-breaking: prefers nodes closer to goal when f-scores are equal.
    Uses negative g-score as secondary key (prefer larger g = closer to goal).

    >>> g = {"A": [("B", 1), ("C", 1)], "B": [("D", 2)], "C": [("D", 2)], "D": []}
    >>> path, cost = a_star_tiebreak(g, "A", "D", {"A": 3, "B": 2, "C": 2, "D": 0})
    >>> cost
    3
    """
    if start == goal:
        return [start], 0

    counter = 0
    open_set = [(heuristic.get(start, 0), 0, counter, start)]
    came_from: dict[str, str] = {}
    g_score: dict[str, float] = {start: 0}
    closed: set[str] = set()

    while open_set:
        _, _, _, current = heapq.heappop(open_set)
        if current == goal:
            return _reconstruct(came_from, current, start), g_score[goal]

        if current in closed:
            continue
        closed.add(current)

        for neighbor, weight in graph.get(current, []):
            if neighbor in closed:
                continue
            tentative_g = g_score[current] + weight
            if tentative_g < g_score.get(neighbor, inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic.get(neighbor, 0)
                counter += 1
                heapq.heappush(open_set, (f, -tentative_g, counter, neighbor))

    return [], inf


def _reconstruct(came_from: dict, current: str, start: str) -> list[str]:
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    return path[::-1]


def benchmark() -> None:
    """Benchmark all variants on a generated grid graph."""
    import random

    random.seed(42)
    size = 50
    nodes = [(r, c) for r in range(size) for c in range(size)]
    graph: dict[str, list[tuple[str, int]]] = {}
    heuristic: dict[str, float] = {}
    goal_r, goal_c = size - 1, size - 1

    for r, c in nodes:
        key = f"{r},{c}"
        heuristic[key] = abs(r - goal_r) + abs(c - goal_c)
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                weight = random.randint(1, 5)
                neighbors.append((f"{nr},{nc}", weight))
        graph[key] = neighbors

    start_key = "0,0"
    goal_key = f"{goal_r},{goal_c}"
    variants = [
        ("Standard A*", lambda: a_star_standard(graph, start_key, goal_key, heuristic)),
        ("Closed Set A*", lambda: a_star_closed_set(graph, start_key, goal_key, heuristic)),
        ("Weighted A* (e=1.5)", lambda: a_star_weighted(graph, start_key, goal_key, heuristic, 1.5)),
        ("Tie-break A*", lambda: a_star_tiebreak(graph, start_key, goal_key, heuristic)),
    ]

    print(f"\nBenchmark: A* variants on {size}x{size} grid ({size*size} nodes)")
    print("-" * 65)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(10):
            path, cost = func()
        elapsed = (time.perf_counter() - t0) / 10
        print(f"{name:<25} cost={cost:<8.1f} path_len={len(path):<6} time={elapsed*1000:.3f}ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
