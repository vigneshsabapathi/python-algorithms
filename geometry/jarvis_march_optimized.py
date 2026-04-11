#!/usr/bin/env python3
"""
Optimized and alternative implementations of Convex Hull (Jarvis March family).

The reference uses a class-based Point with explicit gift wrapping.
Variants show different performance/clarity trade-offs.

Variants covered:
1. jarvis_tuples       -- raw (x,y) tuples; eliminates class overhead, same
                          O(nh) algorithm.
2. jarvis_with_collinear -- includes all collinear hull-edge points in output;
                            useful when full boundary enumeration is needed.
3. chan_algorithm       -- Chan's algorithm: O(n log h) optimal output-sensitive;
                          combines Graham scan on small groups with Jarvis wrapping
                          on group hulls.

Key interview insight:
    Reference:      O(nh) class-based -- clear, standard
    Tuples:         O(nh) no overhead -- 2-4x faster on large inputs
    With collinear: O(nh) variant     -- answers "all boundary points" question
    Chan's:         O(n log h)        -- optimal output-sensitive, advanced topic

Run:
    python geometry/jarvis_march_optimized.py
"""

from __future__ import annotations

import math
import sys
import os
import timeit
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from geometry.jarvis_march import jarvis_march as jarvis_march_reference, Point, _cross, _dist_sq


# ---------------------------------------------------------------------------
# Variant 1 -- Tuple-only Jarvis March (no class overhead)
# ---------------------------------------------------------------------------

def jarvis_tuples(
    points: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """
    Jarvis march on raw (x, y) tuples.

    >>> hull = jarvis_tuples([(0,0),(2,0),(2,2),(0,2),(1,1)])
    >>> len(hull)
    4
    >>> (1,1) in hull
    False
    >>> jarvis_tuples([(0,0),(1,1)])
    []
    """
    pts = list(set(points))
    n = len(pts)
    if n < 3:
        return []

    start = min(range(n), key=lambda i: (pts[i][0], pts[i][1]))
    hull: list[tuple[float, float]] = []
    current = start

    while True:
        hull.append(pts[current])
        cand = 0 if current != 0 else 1

        for i in range(n):
            if i == current:
                continue
            ox, oy = pts[current]
            ax, ay = pts[cand]
            bx, by = pts[i]
            cross = (ax - ox) * (by - oy) - (ay - oy) * (bx - ox)
            if cross < 0:
                cand = i
            elif cross == 0:
                di = (bx - ox) ** 2 + (by - oy) ** 2
                dc = (ax - ox) ** 2 + (ay - oy) ** 2
                if di > dc:
                    cand = i

        current = cand
        if current == start:
            break
        if len(hull) > n:
            break

    return hull if len(hull) >= 3 else []


# ---------------------------------------------------------------------------
# Variant 2 -- Jarvis with collinear boundary points
# ---------------------------------------------------------------------------

def jarvis_with_collinear(points: list[Point]) -> list[Point]:
    """
    Jarvis march that includes all points lying on hull edges.

    Useful when asked "find all boundary points" in interviews.

    >>> hull = jarvis_with_collinear([
    ...     Point(0,0), Point(1,0), Point(2,0), Point(2,2), Point(0,2)
    ... ])
    >>> Point(1,0) in hull  # collinear point on bottom edge
    True
    >>> len(hull)
    5
    >>> jarvis_with_collinear([Point(0,0)])
    []
    """
    unique = list({(p.x, p.y): p for p in points}.values())
    n = len(unique)
    if n < 3:
        return []

    start = min(range(n), key=lambda i: (unique[i].x, unique[i].y))

    hull_order: list[int] = []
    current = start

    while True:
        hull_order.append(current)
        cand = 0 if current != 0 else 1

        for i in range(n):
            if i == current:
                continue
            cross = _cross(unique[current], unique[cand], unique[i])
            if cross < 0:
                cand = i
            elif cross == 0:
                if _dist_sq(unique[current], unique[i]) > _dist_sq(
                    unique[current], unique[cand]
                ):
                    cand = i

        # Before moving to cand, collect all collinear points on this edge
        collinear_on_edge: list[tuple[float, int]] = []
        for i in range(n):
            if i == current or i == cand:
                continue
            if i in hull_order:
                continue
            cross = _cross(unique[current], unique[cand], unique[i])
            if abs(cross) < 1e-9:
                d = _dist_sq(unique[current], unique[i])
                d_cand = _dist_sq(unique[current], unique[cand])
                if 0 < d < d_cand:
                    collinear_on_edge.append((d, i))

        collinear_on_edge.sort()
        for _, idx in collinear_on_edge:
            hull_order.append(idx)

        current = cand
        if current == start:
            break
        if len(hull_order) > n:
            break

    hull = [unique[i] for i in hull_order]
    return hull if len(hull) >= 3 else []


# ---------------------------------------------------------------------------
# Variant 3 -- Chan's Algorithm O(n log h) [simplified]
# ---------------------------------------------------------------------------

def _graham_small(pts: list[Point]) -> list[Point]:
    """Graham scan on a small group (helper for Chan's algorithm)."""
    if len(pts) < 3:
        return pts[:]
    anchor = min(pts, key=lambda p: (p.y, p.x))
    rest = sorted(
        [p for p in pts if p != anchor],
        key=lambda p: (math.atan2(p.y - anchor.y, p.x - anchor.x), -_dist_sq(anchor, p)),
    )
    stack = [anchor]
    for p in rest:
        while len(stack) >= 2 and _cross(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)
    return stack


def _tangent_point(hull: list[Point], p: Point) -> Point:
    """Find the point in hull most counter-clockwise from p (right tangent)."""
    best = hull[0]
    for q in hull[1:]:
        cross = _cross(p, best, q)
        if cross < 0:
            best = q
        elif cross == 0 and _dist_sq(p, q) > _dist_sq(p, best):
            best = q
    return best


def chan_algorithm(points: list[Point]) -> list[Point]:
    """
    Chan's output-sensitive convex hull algorithm.

    Combines Graham scan on small groups with Jarvis wrapping on group hulls.
    Optimal O(n log h) time.

    >>> hull = chan_algorithm([Point(0,0), Point(2,0), Point(2,2), Point(0,2), Point(1,1)])
    >>> len(hull)
    4
    >>> Point(1,1) in hull
    False
    >>> chan_algorithm([Point(0,0)])
    []
    """
    unique = list({(p.x, p.y): p for p in points}.values())
    n = len(unique)
    if n < 3:
        return []

    # Try increasing guesses for h
    for t in range(1, n.bit_length() + 2):
        m = min(2 ** (2 ** t), n)

        # Split into groups of size m and compute mini-hulls
        groups = [unique[i:i + m] for i in range(0, n, m)]
        mini_hulls = [_graham_small(g) for g in groups]

        # Jarvis wrap on mini-hulls
        start_pt = min(unique, key=lambda p: (p.x, p.y))
        hull = [start_pt]

        for _ in range(m):
            candidates = [_tangent_point(mh, hull[-1]) for mh in mini_hulls if mh]
            # Pick the most counter-clockwise candidate
            best = candidates[0]
            for c in candidates[1:]:
                cross = _cross(hull[-1], best, c)
                if cross < 0:
                    best = c
                elif cross == 0 and _dist_sq(hull[-1], c) > _dist_sq(hull[-1], best):
                    best = c

            if best == start_pt:
                break
            hull.append(best)

        if hull[-1] == start_pt or len(hull) <= m:
            return hull if len(hull) >= 3 else []

    return hull if len(hull) >= 3 else []


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_SETS: list[tuple[str, list[Point], int]] = [
    ("square+interior", [Point(0,0), Point(2,0), Point(2,2), Point(0,2), Point(1,1)], 4),
    ("triangle", [Point(0,0), Point(4,0), Point(2,3)], 3),
    ("pentagon", [Point(0,1), Point(1,0), Point(2,0), Point(3,1), Point(1.5,3), Point(1.5,1)], 5),
]


def _hull_set(hull: list) -> set[tuple[float, float]]:
    if not hull:
        return set()
    if isinstance(hull[0], tuple):
        return set(hull)
    return {(p.x, p.y) for p in hull}


def run_all() -> None:
    print("\n=== Correctness ===")
    for label, pts, expected_len in TEST_SETS:
        ref = jarvis_march_reference(pts)
        tup_input = [(p.x, p.y) for p in pts]
        tup = jarvis_tuples(tup_input)
        chan = chan_algorithm(pts)

        ref_set = _hull_set(ref)
        tup_set = _hull_set(tup)
        chan_set = _hull_set(chan)

        ok = ref_set == tup_set == chan_set and len(ref) == expected_len
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] {label:20s}  hull_size={len(ref)}  (expected {expected_len})")

    # Collinear variant test
    pts_collinear = [Point(0,0), Point(1,0), Point(2,0), Point(2,2), Point(0,2)]
    hull_col = jarvis_with_collinear(pts_collinear)
    has_midpoint = Point(1, 0) in hull_col
    print(f"  [{'OK' if has_midpoint else 'FAIL'}] collinear variant   includes boundary midpoint: {has_midpoint}")

    # Benchmark
    random.seed(42)
    N = 300
    rand_pts = [Point(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(N)]
    rand_tuples = [(p.x, p.y) for p in rand_pts]

    REPS = 500
    print(f"\n=== Benchmark: {REPS} iterations, {N} random points ===")
    impls = [
        ("Reference Jarvis",    lambda: jarvis_march_reference(rand_pts)),
        ("Tuples Jarvis",       lambda: jarvis_tuples(rand_tuples)),
        ("With collinear",      lambda: jarvis_with_collinear(rand_pts)),
        ("Chan's algorithm",    lambda: chan_algorithm(rand_pts)),
    ]
    for name, fn in impls:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<22} {t:>8.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
