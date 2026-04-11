"""
Graham Scan — Convex hull algorithm for 2D points.

Finds the convex hull of a set of points in O(n log n) time by sorting
points by polar angle and using a stack to detect left/right turns.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/graham_scan.py
"""

from __future__ import annotations

import math


def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
    """
    Cross product of vectors OA and OB — positive if counter-clockwise.

    >>> cross((0, 0), (1, 0), (0, 1))
    1
    >>> cross((0, 0), (0, 1), (1, 0))
    -1
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Euclidean distance between two points."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def graham_scan(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Compute the convex hull of a set of 2D points using Graham Scan.

    Returns the hull vertices in counter-clockwise order.

    >>> graham_scan([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)])
    [(0, 0), (1, 0), (1, 1), (0, 1)]
    >>> graham_scan([(0, 0), (1, 0), (2, 0)])
    [(0, 0), (2, 0)]
    >>> graham_scan([(0, 0)])
    [(0, 0)]
    >>> graham_scan([])
    []
    >>> graham_scan([(0, 0), (1, 1)])
    [(0, 0), (1, 1)]
    """
    if len(points) <= 1:
        return list(points)

    # Find the lowest point (and leftmost if tie)
    pivot = min(points, key=lambda p: (p[1], p[0]))

    def polar_angle_key(p: tuple[float, float]) -> tuple[float, float]:
        angle = math.atan2(p[1] - pivot[1], p[0] - pivot[0])
        dist = distance(pivot, p)
        return (angle, dist)

    # Sort by polar angle w.r.t. pivot
    sorted_points = sorted(
        (p for p in points if p != pivot), key=polar_angle_key
    )

    if not sorted_points:
        return [pivot]

    # Build the hull using a stack
    hull = [pivot]
    for p in sorted_points:
        while len(hull) > 1 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)

    return hull


if __name__ == "__main__":
    import doctest

    doctest.testmod()
