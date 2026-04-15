"""
Multi-Heuristic A* Search - Optimized Variants

Uses multiple heuristics (consistent + inadmissible) to guide pathfinding.
Explores promising paths from each heuristic, converging faster than single-heuristic.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/multi_heuristic_astar.py
"""

import heapq
import math
import time


# ---------- Variant 1: Clean multi-heuristic with heapq ----------
def multi_heuristic_astar(
    grid_size: int,
    obstacles: set[tuple[int, int]],
    start: tuple[int, int],
    goal: tuple[int, int],
    w1: float = 1.0,
    w2: float = 1.0,
) -> list[tuple[int, int]] | None:
    """
    Multi-heuristic A* with configurable weights and heuristics.

    >>> path = multi_heuristic_astar(5, set(), (0, 0), (4, 4))
    >>> path is not None and path[0] == (0, 0) and path[-1] == (4, 4)
    True
    >>> multi_heuristic_astar(5, {(1,0),(1,1),(1,2),(1,3)}, (0,0), (2,2)) is not None
    True
    """
    def manhattan(p, g):
        return abs(p[0] - g[0]) + abs(p[1] - g[1])

    def euclidean(p, g):
        return math.sqrt((p[0] - g[0]) ** 2 + (p[1] - g[1]) ** 2)

    def chebyshev(p, g):
        return max(abs(p[0] - g[0]), abs(p[1] - g[1]))

    heuristics = [manhattan, euclidean, chebyshev]
    n_h = len(heuristics)

    g = {start: 0}
    parent = {start: None}
    open_lists = [[] for _ in range(n_h)]
    closed_anchor = set()
    closed_inad = set()

    for i in range(n_h):
        h_val = g[start] + w1 * heuristics[i](start, goal)
        heapq.heappush(open_lists[i], (h_val, start))

    def expand(s, idx):
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = s[0] + dy, s[1] + dx
            nbr = (ny, nx)
            if 0 <= ny < grid_size and 0 <= nx < grid_size and nbr not in obstacles:
                new_g = g[s] + 1
                if nbr not in g or new_g < g[nbr]:
                    g[nbr] = new_g
                    parent[nbr] = s
                    if nbr not in closed_anchor:
                        heapq.heappush(open_lists[0], (new_g + w1 * heuristics[0](nbr, goal), nbr))
                        if nbr not in closed_inad:
                            for j in range(1, n_h):
                                key_j = new_g + w1 * heuristics[j](nbr, goal)
                                if key_j <= w2 * (new_g + w1 * heuristics[0](nbr, goal)):
                                    heapq.heappush(open_lists[j], (key_j, nbr))

    while open_lists[0]:
        for i in range(1, n_h):
            if open_lists[i] and open_lists[i][0][0] <= w2 * (open_lists[0][0][0] if open_lists[0] else float('inf')):
                if goal in g and g[goal] <= open_lists[i][0][0]:
                    path = []
                    node = goal
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    return path[::-1]
                _, s = heapq.heappop(open_lists[i])
                expand(s, i)
                closed_inad.add(s)
            else:
                if goal in g and open_lists[0] and g[goal] <= open_lists[0][0][0]:
                    path = []
                    node = goal
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    return path[::-1]
                if open_lists[0]:
                    _, s = heapq.heappop(open_lists[0])
                    expand(s, 0)
                    closed_anchor.add(s)

        if not any(open_lists):
            break

    if goal in g:
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        return path[::-1]
    return None


# ---------- Variant 2: Single-heuristic A* for comparison ----------
def astar_single(
    grid_size: int, obstacles: set[tuple[int, int]],
    start: tuple[int, int], goal: tuple[int, int]
) -> list[tuple[int, int]] | None:
    """
    Standard A* with Manhattan heuristic for comparison.

    >>> path = astar_single(5, set(), (0, 0), (4, 4))
    >>> path[0] == (0, 0) and path[-1] == (4, 4)
    True
    """
    def h(p):
        return abs(p[0] - goal[0]) + abs(p[1] - goal[1])

    open_set = [(h(start), 0, start)]
    g_score = {start: 0}
    parent = {start: None}

    while open_set:
        _, g_curr, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nbr = (current[0] + dy, current[1] + dx)
            if 0 <= nbr[0] < grid_size and 0 <= nbr[1] < grid_size and nbr not in obstacles:
                new_g = g_score[current] + 1
                if nbr not in g_score or new_g < g_score[nbr]:
                    g_score[nbr] = new_g
                    parent[nbr] = current
                    heapq.heappush(open_set, (new_g + h(nbr), new_g, nbr))
    return None


# ---------- Variant 3: Weighted A* ----------
def weighted_astar(
    grid_size: int, obstacles: set[tuple[int, int]],
    start: tuple[int, int], goal: tuple[int, int], epsilon: float = 2.0
) -> list[tuple[int, int]] | None:
    """
    Weighted A* with inflation factor epsilon. Faster but suboptimal.

    >>> path = weighted_astar(10, set(), (0, 0), (9, 9), 2.0)
    >>> path[0] == (0, 0) and path[-1] == (9, 9)
    True
    """
    def h(p):
        return abs(p[0] - goal[0]) + abs(p[1] - goal[1])

    open_set = [(epsilon * h(start), 0, start)]
    g_score = {start: 0}
    parent = {start: None}

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nbr = (current[0] + dy, current[1] + dx)
            if 0 <= nbr[0] < grid_size and 0 <= nbr[1] < grid_size and nbr not in obstacles:
                new_g = g_score[current] + 1
                if nbr not in g_score or new_g < g_score[nbr]:
                    g_score[nbr] = new_g
                    parent[nbr] = current
                    heapq.heappush(open_set, (new_g + epsilon * h(nbr), new_g, nbr))
    return None


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 50
    obstacles = {(random.randint(1, n - 2), random.randint(1, n - 2)) for _ in range(n * 5)}
    obstacles.discard((0, 0))
    obstacles.discard((n - 1, n - 1))

    for name, fn in [
        ("multi_heuristic", lambda: multi_heuristic_astar(n, obstacles, (0, 0), (n - 1, n - 1))),
        ("single_astar", lambda: astar_single(n, obstacles, (0, 0), (n - 1, n - 1))),
        ("weighted_astar", lambda: weighted_astar(n, obstacles, (0, 0), (n - 1, n - 1), 2.0)),
    ]:
        start = time.perf_counter()
        for _ in range(100):
            path = fn()
        elapsed = (time.perf_counter() - start) / 100 * 1000
        plen = len(path) if path else 0
        print(f"  {name:20s}: {elapsed:.3f} ms (path len: {plen})")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Multi-Heuristic A* Benchmark (50x50 grid, 100 runs) ===")
    benchmark()
