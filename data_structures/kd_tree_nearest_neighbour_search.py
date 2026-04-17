#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  Reference: https://github.com/TheAlgorithms/Python/pull/11532

from __future__ import annotations


class KDNode:
    """Node in a KD-Tree."""

    def __init__(
        self,
        point: list[float],
        left: KDNode | None = None,
        right: KDNode | None = None,
    ) -> None:
        self.point = point
        self.left = left
        self.right = right


def build_kdtree(points: list[list[float]], depth: int = 0) -> KDNode | None:
    """Build a KD-Tree from a list of points."""
    if not points:
        return None
    k = len(points[0])
    axis = depth % k
    points.sort(key=lambda point: point[axis])
    median_idx = len(points) // 2
    return KDNode(
        point=points[median_idx],
        left=build_kdtree(points[:median_idx], depth + 1),
        right=build_kdtree(points[median_idx + 1 :], depth + 1),
    )


def nearest_neighbour_search(
    root: KDNode | None, query_point: list[float]
) -> tuple[list[float] | None, float, int]:
    """
    Performs a nearest neighbor search in a KD-Tree for a given query point.

    Args:
        root (KDNode | None): The root node of the KD-Tree.
        query_point (list[float]): The point for which the nearest neighbor
                                    is being searched.

    Returns:
        tuple[list[float] | None, float, int]:
            - The nearest point found in the KD-Tree to the query point,
              or None if no point is found.
            - The squared distance to the nearest point.
            - The number of nodes visited during the search.

    >>> points = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
    >>> tree = build_kdtree(points)
    >>> nearest, dist, visited = nearest_neighbour_search(tree, [9, 2])
    >>> nearest
    [8, 1]
    >>> dist
    2
    >>> visited > 0
    True

    >>> nearest_neighbour_search(None, [1, 2])
    (None, inf, 0)
    """
    nearest_point: list[float] | None = None
    nearest_dist: float = float("inf")
    nodes_visited: int = 0

    def search(node: KDNode | None, depth: int = 0) -> None:
        nonlocal nearest_point, nearest_dist, nodes_visited
        if node is None:
            return

        nodes_visited += 1

        current_point = node.point
        current_dist = sum(
            (query_coord - point_coord) ** 2
            for query_coord, point_coord in zip(query_point, current_point)
        )

        if nearest_point is None or current_dist < nearest_dist:
            nearest_point = current_point
            nearest_dist = current_dist

        k = len(query_point)
        axis = depth % k

        if query_point[axis] <= current_point[axis]:
            nearer_subtree = node.left
            further_subtree = node.right
        else:
            nearer_subtree = node.right
            further_subtree = node.left

        search(nearer_subtree, depth + 1)

        if (query_point[axis] - current_point[axis]) ** 2 < nearest_dist:
            search(further_subtree, depth + 1)

    search(root, 0)
    return nearest_point, nearest_dist, nodes_visited


if __name__ == "__main__":
    import doctest

    doctest.testmod()
