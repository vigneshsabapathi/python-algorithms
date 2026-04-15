"""
A* Search Algorithm

Informed search algorithm that finds the shortest path using
heuristic function. Combines Dijkstra's (actual cost) with
greedy best-first (estimated cost): f(n) = g(n) + h(n).

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/astar.py
"""

import heapq
import numpy as np


class GridAStar:
    """
    A* pathfinding on a 2D grid.

    0 = passable, 1 = obstacle.

    >>> grid = np.array([
    ...     [0, 0, 0, 0],
    ...     [0, 1, 1, 0],
    ...     [0, 0, 0, 0],
    ...     [0, 0, 0, 0]
    ... ])
    >>> astar = GridAStar(grid)
    >>> path = astar.search((0, 0), (3, 3))
    >>> path is not None
    True
    >>> path[0] == (0, 0) and path[-1] == (3, 3)
    True
    """

    def __init__(self, grid: np.ndarray) -> None:
        self.grid = grid
        self.rows, self.cols = grid.shape

    @staticmethod
    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
        """
        Manhattan distance heuristic.

        >>> GridAStar.heuristic((0, 0), (3, 4))
        7
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        """Get valid neighboring cells (4-directional)."""
        r, c = pos
        result = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr, nc] == 0:
                result.append((nr, nc))
        return result

    def search(
        self, start: tuple[int, int], goal: tuple[int, int]
    ) -> list[tuple[int, int]] | None:
        """
        Find shortest path from start to goal.

        Returns list of (row, col) positions, or None if no path exists.
        """
        if self.grid[start[0], start[1]] == 1 or self.grid[goal[0], goal[1]] == 1:
            return None

        open_set = [(0 + self.heuristic(start, goal), 0, start)]
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], float] = {start: 0}
        closed_set: set[tuple[int, int]] = set()

        while open_set:
            f, g, current = heapq.heappop(open_set)

            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            if current in closed_set:
                continue
            closed_set.add(current)

            for neighbor in self._neighbors(current):
                if neighbor in closed_set:
                    continue
                tentative_g = g + 1

                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

        return None  # No path found


class GraphAStar:
    """
    A* on a weighted graph (adjacency dict).

    >>> graph = {
    ...     'A': [('B', 1), ('C', 4)],
    ...     'B': [('C', 2), ('D', 5)],
    ...     'C': [('D', 1)],
    ...     'D': []
    ... }
    >>> heuristic = {'A': 3, 'B': 2, 'C': 1, 'D': 0}
    >>> path, cost = GraphAStar.search(graph, 'A', 'D', heuristic)
    >>> path
    ['A', 'B', 'C', 'D']
    >>> cost
    4
    """

    @staticmethod
    def search(
        graph: dict,
        start: str,
        goal: str,
        heuristic: dict[str, float],
    ) -> tuple[list[str], float]:
        """Find shortest path in weighted graph."""
        open_set = [(heuristic.get(start, 0), 0, start)]
        came_from: dict[str, str] = {}
        g_score: dict[str, float] = {start: 0}

        while open_set:
            _, g, current = heapq.heappop(open_set)

            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1], g

            for neighbor, weight in graph.get(current, []):
                tentative_g = g + weight
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic.get(neighbor, 0)
                    heapq.heappush(open_set, (f, tentative_g, neighbor))

        return [], float("inf")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- A* Search Demo ---")

    # Grid search
    grid = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ])

    astar = GridAStar(grid)
    path = astar.search((0, 0), (6, 6))
    print(f"Grid path (0,0) -> (6,6): {path}")
    print(f"Path length: {len(path) if path else 'No path'}")

    # Graph search
    graph = {
        "S": [("A", 1), ("B", 4)],
        "A": [("B", 2), ("C", 5), ("G", 12)],
        "B": [("C", 2)],
        "C": [("G", 3)],
        "G": [],
    }
    h = {"S": 7, "A": 6, "B": 4, "C": 2, "G": 0}
    path, cost = GraphAStar.search(graph, "S", "G", h)
    print(f"\nGraph path S -> G: {path}, cost: {cost}")
