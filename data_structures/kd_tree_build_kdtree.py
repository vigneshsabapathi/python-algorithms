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
    """
    Builds a KD-Tree from a list of points.

    Args:
        points: The list of points to build the KD-Tree from.
        depth: The current depth in the tree (used to determine axis for splitting).

    Returns:
        The root node of the KD-Tree, or None if no points are provided.

    >>> tree = build_kdtree([[3, 6], [17, 15], [13, 15], [6, 12], [9, 1], [2, 7], [10, 19]])
    >>> tree.point
    [9, 1]
    >>> tree.left is not None
    True
    >>> tree.right is not None
    True

    >>> build_kdtree([]) is None
    True

    >>> single = build_kdtree([[5, 5]])
    >>> single.point
    [5, 5]
    >>> single.left is None
    True
    >>> single.right is None
    True
    """
    if not points:
        return None

    k = len(points[0])  # Dimensionality of the points
    axis = depth % k

    points.sort(key=lambda point: point[axis])
    median_idx = len(points) // 2

    left_points = points[:median_idx]
    right_points = points[median_idx + 1 :]

    return KDNode(
        point=points[median_idx],
        left=build_kdtree(left_points, depth + 1),
        right=build_kdtree(right_points, depth + 1),
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
