"""
Greedy Best-First Search - Optimized Variants

Greedy BFS uses a heuristic to expand the most promising node first.
Unlike A*, it only considers the heuristic (not path cost).

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/greedy_best_first.py
"""

import heapq
import time
import math


# ---------- Variant 1: Heap-based (O(n log n) vs O(n^2) sorting) ----------
def greedy_best_first_heap(
    grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
) -> list[tuple[int, int]] | None:
    """
    Greedy BFS using heapq for efficient node selection.

    >>> grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    >>> greedy_best_first_heap(grid, (0, 0), (2, 2))
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
    """
    rows, cols = len(grid), len(grid[0])

    def heuristic(pos):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    open_set = [(heuristic(start), start)]
    came_from = {start: None}
    closed = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        if current in closed:
            continue
        closed.add(current)

        for dy, dx in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ny, nx = current[0] + dy, current[1] + dx
            neighbor = (ny, nx)
            if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0 and neighbor not in closed:
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (heuristic(neighbor), neighbor))

    return [start]  # no path found


# ---------- Variant 2: Euclidean heuristic ----------
def greedy_best_first_euclidean(
    grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
) -> list[tuple[int, int]] | None:
    """
    Greedy BFS with Euclidean distance heuristic.

    >>> grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    >>> path = greedy_best_first_euclidean(grid, (0, 0), (2, 2))
    >>> path[0] == (0, 0) and path[-1] == (2, 2)
    True
    """
    rows, cols = len(grid), len(grid[0])

    def heuristic(pos):
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

    open_set = [(heuristic(start), start)]
    came_from = {start: None}
    closed = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        if current in closed:
            continue
        closed.add(current)

        for dy, dx in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ny, nx = current[0] + dy, current[1] + dx
            neighbor = (ny, nx)
            if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0 and neighbor not in closed:
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (heuristic(neighbor), neighbor))

    return [start]


# ---------- Variant 3: 8-directional movement ----------
def greedy_best_first_8dir(
    grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
) -> list[tuple[int, int]] | None:
    """
    Greedy BFS with 8-directional movement (including diagonals).

    >>> grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    >>> path = greedy_best_first_8dir(grid, (0, 0), (2, 2))
    >>> len(path) <= 5  # diagonal path is shorter
    True
    """
    rows, cols = len(grid), len(grid[0])
    dirs = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def heuristic(pos):
        dx = abs(pos[0] - goal[0])
        dy = abs(pos[1] - goal[1])
        return max(dx, dy)  # Chebyshev distance for 8-dir

    open_set = [(heuristic(start), start)]
    came_from = {start: None}
    closed = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        if current in closed:
            continue
        closed.add(current)

        for dy, dx in dirs:
            ny, nx = current[0] + dy, current[1] + dx
            neighbor = (ny, nx)
            if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0 and neighbor not in closed:
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (heuristic(neighbor), neighbor))

    return [start]


# ---------- Benchmark ----------
def benchmark():
    grid = [[0] * 50 for _ in range(50)]
    # Add some obstacles
    for i in range(10, 40):
        grid[25][i] = 1
    start = (0, 0)
    goal = (49, 49)

    for name, fn in [
        ("heap_manhattan", lambda: greedy_best_first_heap(grid, start, goal)),
        ("heap_euclidean", lambda: greedy_best_first_euclidean(grid, start, goal)),
        ("8_directional", lambda: greedy_best_first_8dir(grid, start, goal)),
    ]:
        s = time.perf_counter()
        for _ in range(500):
            path = fn()
        elapsed = (time.perf_counter() - s) / 500 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms (path len: {len(path)})")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Greedy Best-First Benchmark (50x50 grid, 500 runs) ===")
    benchmark()
