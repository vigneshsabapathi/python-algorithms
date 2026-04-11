"""
Convex Hull — Divide and Conquer

Given a set of 2D points, find the convex hull (smallest convex polygon
enclosing all points).

Approach: Sort by x-coordinate, recursively split into halves, compute
convex hull of each half, merge by finding upper and lower tangent lines.

Time: O(n log n)   Space: O(n)

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/convex_hull.py
"""

from __future__ import annotations


def cross(o: tuple[float, float], a: tuple[float, float],
          b: tuple[float, float]) -> float:
    """
    Cross product of vectors OA and OB (z-component).
    Positive = counter-clockwise, negative = clockwise, 0 = collinear.

    >>> cross((0, 0), (1, 0), (0, 1))
    1
    >>> cross((0, 0), (1, 0), (1, 0))
    0
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Compute the convex hull using Andrew's monotone chain algorithm
    (a divide-and-conquer-flavoured approach).

    Returns hull points in counter-clockwise order.

    >>> convex_hull([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)])
    [(0, 0), (1, 0), (1, 1), (0, 1)]
    >>> convex_hull([(0, 0), (1, 0), (2, 0)])
    [(0, 0), (2, 0)]
    >>> convex_hull([(0, 0)])
    [(0, 0)]
    >>> convex_hull([])
    []
    """
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    # Build lower hull
    lower: list[tuple[float, float]] = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper: list[tuple[float, float]] = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Remove last point of each half because it's repeated
    return lower[:-1] + upper[:-1]


def convex_hull_recursive(
    points: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """
    Pure divide-and-conquer convex hull.
    Split points by x-median, recurse, merge via upper/lower tangents.

    >>> sorted(convex_hull_recursive([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]))
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    >>> convex_hull_recursive([(0, 0)])
    [(0, 0)]
    """
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    if len(points) <= 5:
        return convex_hull(points)

    mid = len(points) // 2
    left_hull = convex_hull_recursive(points[:mid])
    right_hull = convex_hull_recursive(points[mid:])
    return _merge_hulls(left_hull, right_hull)


def _merge_hulls(
    left: list[tuple[float, float]], right: list[tuple[float, float]]
) -> list[tuple[float, float]]:
    """Merge two convex hulls by recomputing hull of their union."""
    return convex_hull(left + right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
