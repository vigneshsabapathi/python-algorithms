"""
Closest Pair of Points — Divide and Conquer

Given n points in 2D, find the pair with the smallest Euclidean distance.

Brute force: O(n^2) — check every pair.
Divide and conquer: O(n log n) — split by x-coordinate, recurse on halves,
merge by checking a 2*delta strip (at most 6 comparisons per point in strip).

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/closest_pair_of_points.py
"""

from __future__ import annotations

import math


def euclidean_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two 2D points.

    >>> euclidean_distance((0, 0), (3, 4))
    5.0
    >>> euclidean_distance((1, 1), (1, 1))
    0.0
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def _brute_force(
    points: list[tuple[float, float]],
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    """
    Brute-force closest pair for small inputs.

    >>> _brute_force([(0, 0), (3, 4), (1, 1)])
    (1.4142135623730951, ((0, 0), (1, 1)))
    """
    n = len(points)
    best = float("inf")
    pair = (points[0], points[1])
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean_distance(points[i], points[j])
            if d < best:
                best = d
                pair = (points[i], points[j])
    return best, pair


def _strip_closest(
    strip: list[tuple[float, float]],
    delta: float,
    best_pair: tuple[tuple[float, float], tuple[float, float]],
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    """
    Check points in the strip sorted by y-coordinate.
    At most 6 comparisons per point (geometric packing argument).
    """
    strip.sort(key=lambda p: p[1])
    best = delta
    pair = best_pair
    n = len(strip)
    for i in range(n):
        j = i + 1
        while j < n and (strip[j][1] - strip[i][1]) < best:
            d = euclidean_distance(strip[i], strip[j])
            if d < best:
                best = d
                pair = (strip[i], strip[j])
            j += 1
    return best, pair


def closest_pair(
    points: list[tuple[float, float]],
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    """
    Find the closest pair of points using divide and conquer.

    Returns (distance, (point1, point2)).

    >>> closest_pair([(0, 0), (3, 4), (1, 1), (5, 5)])
    (1.4142135623730951, ((0, 0), (1, 1)))
    >>> closest_pair([(0, 0), (10, 10), (0, 1)])
    (1.0, ((0, 0), (0, 1)))
    >>> closest_pair([(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)])
    (1.4142135623730951, ((2, 3), (3, 4)))
    """
    if len(points) < 2:
        raise ValueError("Need at least 2 points")

    points_sorted = sorted(points, key=lambda p: p[0])
    return _closest_pair_rec(points_sorted)


def _closest_pair_rec(
    points: list[tuple[float, float]],
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    n = len(points)
    if n <= 3:
        return _brute_force(points)

    mid = n // 2
    mid_point = points[mid]

    left_dist, left_pair = _closest_pair_rec(points[:mid])
    right_dist, right_pair = _closest_pair_rec(points[mid:])

    if left_dist < right_dist:
        delta = left_dist
        best_pair = left_pair
    else:
        delta = right_dist
        best_pair = right_pair

    strip = [p for p in points if abs(p[0] - mid_point[0]) < delta]

    return _strip_closest(strip, delta, best_pair)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
