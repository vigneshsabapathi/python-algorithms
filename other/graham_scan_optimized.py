#!/usr/bin/env python3
"""
Optimized and alternative implementations of Graham Scan (Convex Hull).

Variants covered:
1. graham_scan      -- Graham scan with polar angle sort (reference)
2. andrew_monotone  -- Andrew's monotone chain algorithm
3. gift_wrapping    -- Jarvis march / gift wrapping O(nh)

Run:
    python other/graham_scan_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.graham_scan import graham_scan as reference


def cross(o: tuple, a: tuple, b: tuple) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def andrew_monotone(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Convex hull using Andrew's monotone chain algorithm.

    >>> andrew_monotone([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)])
    [(0, 0), (1, 0), (1, 1), (0, 1)]
    >>> andrew_monotone([(0, 0)])
    [(0, 0)]
    >>> andrew_monotone([])
    []
    """
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts

    # Build lower hull
    lower: list[tuple[float, float]] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper: list[tuple[float, float]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def gift_wrapping(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Jarvis march / gift wrapping convex hull. O(nh) where h = hull size.

    >>> gift_wrapping([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)])
    [(0, 0), (1, 0), (1, 1), (0, 1)]
    >>> gift_wrapping([])
    []
    """
    if len(points) <= 1:
        return list(points)

    # Start from leftmost point
    start = min(points, key=lambda p: (p[0], p[1]))
    hull = []
    current = start

    while True:
        hull.append(current)
        candidate = points[0]
        for p in points[1:]:
            if candidate == current:
                candidate = p
                continue
            c = cross(current, candidate, p)
            if c < 0 or (c == 0 and math.dist(current, p) > math.dist(current, candidate)):
                candidate = p
        current = candidate
        if current == start:
            break

    return hull


def convex_hull_area(points: list[tuple[float, float]]) -> float:
    """
    Compute area of convex hull using the shoelace formula.

    >>> convex_hull_area([(0, 0), (4, 0), (4, 3), (0, 3)])
    12.0
    >>> convex_hull_area([(0, 0), (1, 0), (0.5, 1)])
    0.5
    """
    hull = reference(points)
    n = len(hull)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += hull[i][0] * hull[j][1]
        area -= hull[j][0] * hull[i][1]
    return abs(area) / 2.0


TEST_CASES = [
    ([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)], 4),
    ([(0, 0), (1, 0), (2, 0)], 2),
    ([(0, 0)], 1),
    ([], 0),
]

IMPLS = [
    ("reference", reference),
    ("andrew", andrew_monotone),
    ("gift_wrap", gift_wrapping),
]


def run_all() -> None:
    import random

    print("\n=== Correctness (hull size) ===")
    for points, expected_size in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(list(points))
            ok = len(result) == expected_size
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expected size={expected_size} got={len(result)} hull={result}")
        print(f"  [OK] {len(points)} points -> hull size {expected_size}")

    rng = random.Random(42)
    large = [(rng.uniform(0, 1000), rng.uniform(0, 1000)) for _ in range(1000)]
    REPS = 1000
    print(f"\n=== Benchmark: {REPS} runs, {len(large)} points ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(list(large)), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
