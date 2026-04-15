"""
Breadth-First Search (BFS) on a graph.

BFS explores a graph level by level using a FIFO queue. It finds the shortest
path (in edges) from a source to all reachable nodes in an unweighted graph.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/breadth_first_search.py

>>> g = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'],
...      'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E']}
>>> bfs(g, 'A')
['A', 'B', 'C', 'D', 'E', 'F']

>>> bfs_shortest_path(g, 'A', 'F')
['A', 'C', 'F']

>>> bfs_shortest_path(g, 'A', 'A')
['A']

>>> bfs_shortest_path({'A': []}, 'A', 'B')
[]
"""

from collections import deque


def bfs(graph: dict, start) -> list:
    """Return nodes in BFS order from start.

    >>> bfs({'A': ['B'], 'B': ['A']}, 'A')
    ['A', 'B']
    """
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nbr in graph.get(node, []):
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)
    return order


def bfs_shortest_path(graph: dict, start, goal) -> list:
    """Return shortest path (by edges) from start to goal. Empty if unreachable.

    >>> bfs_shortest_path({'A': ['B'], 'B': ['A', 'C'], 'C': ['B']}, 'A', 'C')
    ['A', 'B', 'C']
    """
    if start == goal:
        return [start]
    visited = {start}
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nbr in graph.get(node, []):
            if nbr in visited:
                continue
            visited.add(nbr)
            parent[nbr] = node
            if nbr == goal:
                path = []
                cur = goal
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                return path[::-1]
            queue.append(nbr)
    return []


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    demo = {
        'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'],
        'D': ['B'], 'E': ['B', 'F'], 'F': ['C', 'E'],
    }
    print("BFS order from A:", bfs(demo, 'A'))
    print("Shortest A->F:", bfs_shortest_path(demo, 'A', 'F'))
