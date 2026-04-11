#!/usr/bin/env python3
"""
Optimized and alternative implementations of Convex Hull.

The reference uses Andrew's monotone chain — O(n log n), robust, simple.

Three additional variants:
  gift_wrapping  — Jarvis march, O(nh) where h = hull size; intuitive
  graham_scan    — Graham scan with polar angle sort; classic textbook
  quickhull      — Divide-and-conquer quickhull; practical fastest for random points

Run:
    python divide_and_conquer/convex_hull_optimized.py
"""

from __future__ import annotations

import math
import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.convex_hull import convex_hull as reference
from divide_and_conquer.convex_hull import cross


# ---------------------------------------------------------------------------
# Variant 1 — Gift Wrapping (Jarvis March): O(nh)
# ---------------------------------------------------------------------------

def gift_wrapping(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Convex hull via Jarvis march (gift wrapping).
    O(nh) where h = number of hull points.

    >>> sorted(gift_wrapping([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]))
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    >>> gift_wrapping([(0, 0)])
    [(0, 0)]
    """
    pts = list(set(points))
    n = len(pts)
    if n <= 1:
        return pts

    # Start from leftmost point
    start = min(range(n), key=lambda i: (pts[i][0], pts[i][1]))
    hull = []
    current = start

    while True:
        hull.append(pts[current])
        candidate = 0
        for i in range(1, n):
            if i == current:
                continue
            if candidate == current:
                candidate = i
                continue
            c = cross(pts[current], pts[candidate], pts[i])
            if c < 0:
                candidate = i
            elif c == 0:
                # Collinear — take the farther point
                d1 = (pts[candidate][0] - pts[current][0]) ** 2 + (pts[candidate][1] - pts[current][1]) ** 2
                d2 = (pts[i][0] - pts[current][0]) ** 2 + (pts[i][1] - pts[current][1]) ** 2
                if d2 > d1:
                    candidate = i
        current = candidate
        if current == start:
            break

    return hull


# ---------------------------------------------------------------------------
# Variant 2 — Graham Scan: O(n log n)
# ---------------------------------------------------------------------------

def graham_scan(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Convex hull via Graham scan with polar angle sort.

    >>> sorted(graham_scan([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]))
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    >>> graham_scan([(0, 0)])
    [(0, 0)]
    """
    pts = list(set(points))
    n = len(pts)
    if n <= 1:
        return pts
    if n == 2:
        return pts

    # Find lowest point (break ties by x)
    pivot = min(pts, key=lambda p: (p[1], p[0]))

    # Remove pivot from list, we'll add it as the starting point
    others = [p for p in pts if p != pivot]

    def polar_angle_key(p: tuple[float, float]) -> tuple[float, float]:
        dx = p[0] - pivot[0]
        dy = p[1] - pivot[1]
        return (math.atan2(dy, dx), dx * dx + dy * dy)

    others.sort(key=polar_angle_key)

    stack = [pivot, others[0]]
    for i in range(1, len(others)):
        while len(stack) > 1 and cross(stack[-2], stack[-1], others[i]) <= 0:
            stack.pop()
        stack.append(others[i])

    return stack


# ---------------------------------------------------------------------------
# Variant 3 — Quickhull: O(n log n) average, O(n^2) worst
# ---------------------------------------------------------------------------

def quickhull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Convex hull via quickhull algorithm.

    >>> sorted(quickhull([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]))
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    >>> quickhull([(0, 0)])
    [(0, 0)]
    """
    pts = list(set(points))
    n = len(pts)
    if n <= 1:
        return pts
    if n == 2:
        return pts

    # Find leftmost and rightmost
    min_pt = min(pts, key=lambda p: p[0])
    max_pt = max(pts, key=lambda p: p[0])

    upper = [p for p in pts if cross(min_pt, max_pt, p) > 0]
    lower = [p for p in pts if cross(min_pt, max_pt, p) < 0]

    hull: list[tuple[float, float]] = []
    _quickhull_rec(min_pt, max_pt, upper, hull)
    _quickhull_rec(max_pt, min_pt, lower, hull)

    if not hull:
        hull = [min_pt, max_pt]

    # Remove collinear points by filtering through monotone chain
    return reference(hull)


def _quickhull_rec(
    a: tuple[float, float],
    b: tuple[float, float],
    points: list[tuple[float, float]],
    hull: list[tuple[float, float]],
) -> None:
    if not points:
        hull.append(a)
        return

    # Find farthest point from line AB
    farthest = max(points, key=lambda p: abs(cross(a, b, p)))

    # Points left of A->farthest
    left_af = [p for p in points if cross(a, farthest, p) > 0]
    # Points left of farthest->B
    left_fb = [p for p in points if cross(farthest, b, p) > 0]

    _quickhull_rec(a, farthest, left_af, hull)
    _quickhull_rec(farthest, b, left_fb, hull)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)],
    [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
    [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(30)],
]

IMPLS = [
    ("reference", reference),
    ("gift_wrap", gift_wrapping),
    ("graham", graham_scan),
    ("quickhull", quickhull),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for pts in TEST_CASES:
        hulls = {}
        for name, fn in IMPLS:
            h = fn(pts)
            hulls[name] = len(h)
        ref_size = hulls["reference"]
        ok = all(v == ref_size for v in hulls.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] n={len(pts):<4} hull_size={ref_size}  "
              + "  ".join(f"{nm}={v}" for nm, v in hulls.items()))

    sizes = [100, 500, 2000]
    REPS = 50

    for n in sizes:
        pts = [(random.uniform(-1000, 1000), random.uniform(-1000, 1000)) for _ in range(n)]
        print(f"\n=== Benchmark n={n}, {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn: fn(pts), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
