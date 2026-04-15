"""
A* Search Algorithm for finding the shortest path in a weighted graph.

A* uses a heuristic function to guide the search, combining the actual cost
from the start (g) with an estimated cost to the goal (h) to prioritize
which nodes to explore first: f(n) = g(n) + h(n).

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/a_star.py

>>> graph = {
...     "A": [("B", 1), ("C", 4)],
...     "B": [("C", 2), ("D", 5)],
...     "C": [("D", 1)],
...     "D": [],
... }
>>> heuristic = {"A": 5, "B": 3, "C": 1, "D": 0}
>>> a_star(graph, "A", "D", heuristic)
(['A', 'B', 'C', 'D'], 4)

>>> a_star(graph, "A", "A", heuristic)
(['A'], 0)

>>> a_star(graph, "D", "A", heuristic)
([], inf)
"""

import heapq
from math import inf


def a_star(
    graph: dict[str, list[tuple[str, int]]],
    start: str,
    goal: str,
    heuristic: dict[str, float],
) -> tuple[list[str], float]:
    """
    A* search algorithm.

    Args:
        graph: adjacency list with (neighbor, weight) tuples
        start: starting node
        goal: target node
        heuristic: estimated cost from each node to goal (must be admissible)

    Returns:
        (path, cost) tuple; empty path and inf cost if unreachable

    >>> graph = {"A": [("B", 1)], "B": [("C", 1)], "C": []}
    >>> heuristic = {"A": 2, "B": 1, "C": 0}
    >>> a_star(graph, "A", "C", heuristic)
    (['A', 'B', 'C'], 2)
    """
    if start == goal:
        return [start], 0

    open_set: list[tuple[float, str]] = [(heuristic.get(start, 0), start)]
    came_from: dict[str, str] = {}
    g_score: dict[str, float] = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[goal]

        for neighbor, weight in graph.get(current, []):
            tentative_g = g_score[current] + weight
            if tentative_g < g_score.get(neighbor, inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic.get(neighbor, 0)
                heapq.heappush(open_set, (f_score, neighbor))

    return [], inf


class GridAStar:
    """
    A* on a 2D grid with obstacles.

    >>> g = GridAStar(5, 5, obstacles={(1,1),(1,2),(1,3)})
    >>> path = g.search((0,0), (2,2))
    >>> (0,0) in path and (2,2) in path
    True
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        obstacles: set[tuple[int, int]] | None = None,
    ) -> None:
        self.rows = rows
        self.cols = cols
        self.obstacles = obstacles or set()

    @staticmethod
    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node: tuple[int, int]) -> list[tuple[int, int]]:
        r, c = node
        result = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in self.obstacles:
                result.append((nr, nc))
        return result

    def search(
        self, start: tuple[int, int], goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Find shortest path on grid using A*."""
        open_set: list[tuple[float, tuple[int, int]]] = [
            (self.heuristic(start, goal), start)
        ]
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], float] = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for neighbor in self.neighbors(current):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, inf):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))

        return []


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("C", 2), ("D", 5)],
        "C": [("D", 1)],
        "D": [],
    }
    heuristic = {"A": 5, "B": 3, "C": 1, "D": 0}
    path, cost = a_star(graph, "A", "D", heuristic)
    print(f"A* path: {path}, cost: {cost}")

    # Grid demo
    grid = GridAStar(5, 5, obstacles={(1, 1), (1, 2), (1, 3)})
    grid_path = grid.search((0, 0), (4, 4))
    print(f"Grid A* path: {grid_path}")
