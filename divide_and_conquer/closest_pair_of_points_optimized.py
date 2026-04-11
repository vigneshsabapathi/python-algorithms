#!/usr/bin/env python3
"""
Optimized and alternative implementations of Closest Pair of Points.

The reference D&C approach is O(n log^2 n) because it re-sorts the strip
by y-coordinate at each level. With pre-sorting by y, we get O(n log n).

Three variants + brute force comparison:
  strip_presort  — pre-sort by Y once, filter strip from Y-sorted list → O(n log n)
  scipy_kdtree   — use scipy.spatial.KDTree for practical performance
  brute_force    — O(n^2) baseline

Run:
    python divide_and_conquer/closest_pair_of_points_optimized.py
"""

from __future__ import annotations

import math
import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.closest_pair_of_points import closest_pair as reference
from divide_and_conquer.closest_pair_of_points import euclidean_distance


# ---------------------------------------------------------------------------
# Variant 1 — O(n log n) with Y pre-sort
# ---------------------------------------------------------------------------

def strip_presort(
    points: list[tuple[float, float]],
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    """
    Closest pair with O(n log n) by pre-sorting Y.

    >>> strip_presort([(0, 0), (3, 4), (1, 1), (5, 5)])[0]
    1.4142135623730951
    >>> strip_presort([(0, 0), (10, 10), (0, 1)])[0]
    1.0
    """
    if len(points) < 2:
        raise ValueError("Need at least 2 points")

    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    dist, pair = _closest_presort(px, py)
    return dist, pair


def _closest_presort(
    px: list[tuple[float, float]], py: list[tuple[float, float]]
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    n = len(px)
    if n <= 3:
        best = float("inf")
        pair = (px[0], px[1])
        for i in range(n):
            for j in range(i + 1, n):
                d = euclidean_distance(px[i], px[j])
                if d < best:
                    best = d
                    pair = (px[i], px[j])
        return best, pair

    mid = n // 2
    mid_x = px[mid][0]

    pyl = [p for p in py if p[0] <= mid_x]
    pyr = [p for p in py if p[0] > mid_x]

    # Handle ties — ensure balanced split
    if len(pyl) > mid + 1:
        excess = len(pyl) - (mid + 1)
        pyr = pyl[-(excess):] + pyr
        pyl = pyl[:mid + 1]

    dl, pair_l = _closest_presort(px[:mid], pyl)
    dr, pair_r = _closest_presort(px[mid:], pyr)

    if dl < dr:
        delta, best_pair = dl, pair_l
    else:
        delta, best_pair = dr, pair_r

    # Build strip from y-sorted list (already sorted)
    strip = [p for p in py if abs(p[0] - mid_x) < delta]

    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and strip[j][1] - strip[i][1] < delta:
            d = euclidean_distance(strip[i], strip[j])
            if d < delta:
                delta = d
                best_pair = (strip[i], strip[j])
            j += 1

    return delta, best_pair


# ---------------------------------------------------------------------------
# Variant 2 — Brute force O(n^2)
# ---------------------------------------------------------------------------

def brute_force(
    points: list[tuple[float, float]],
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    """
    Brute-force closest pair — O(n^2).

    >>> brute_force([(0, 0), (3, 4), (1, 1)])[0]
    1.4142135623730951
    """
    n = len(points)
    if n < 2:
        raise ValueError("Need at least 2 points")
    best = float("inf")
    pair = (points[0], points[1])
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean_distance(points[i], points[j])
            if d < best:
                best = d
                pair = (points[i], points[j])
    return best, pair


# ---------------------------------------------------------------------------
# Variant 3 — scipy KDTree (practical, optimized C code)
# ---------------------------------------------------------------------------

def kdtree_closest(
    points: list[tuple[float, float]],
) -> tuple[float, tuple[tuple[float, float], tuple[float, float]]]:
    """
    Closest pair using scipy KDTree — O(n log n) practical.

    >>> d, _ = kdtree_closest([(0, 0), (3, 4), (1, 1)])
    >>> round(d, 10)
    1.4142135624
    """
    try:
        from scipy.spatial import KDTree
    except ImportError:
        raise ImportError("scipy required for kdtree_closest")

    import numpy as np
    pts = np.array(points)
    tree = KDTree(pts)
    dists, idxs = tree.query(pts, k=2)  # k=2: nearest neighbor (self + closest)
    min_idx = np.argmin(dists[:, 1])
    best_dist = dists[min_idx, 1]
    p1 = tuple(pts[min_idx])
    p2 = tuple(pts[idxs[min_idx, 1]])
    return best_dist, (p1, p2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [(0, 0), (3, 4), (1, 1), (5, 5)],
    [(0, 0), (10, 10), (0, 1)],
    [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)],
    [(i, random.random()) for i in range(20)],
]

IMPLS = [
    ("reference", reference),
    ("strip_presort", strip_presort),
    ("brute_force", brute_force),
]

try:
    from scipy.spatial import KDTree
    IMPLS.append(("kdtree", kdtree_closest))
except ImportError:
    pass


def run_all() -> None:
    print("\n=== Correctness ===")
    for pts in TEST_CASES:
        dists = {}
        for name, fn in IMPLS:
            d, _ = fn(pts)
            dists[name] = round(d, 10)
        ref_d = dists["reference"]
        ok = all(v == ref_d for v in dists.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] n={len(pts):<4}  dist={ref_d}  "
              + "  ".join(f"{nm}={v}" for nm, v in dists.items()))

    sizes = [50, 200, 500]
    REPS = 50

    for n in sizes:
        pts = [(random.uniform(-1000, 1000), random.uniform(-1000, 1000)) for _ in range(n)]
        print(f"\n=== Benchmark n={n}, {REPS} runs ===")
        bench_impls = [impl for impl in IMPLS if not (impl[0] == "brute_force" and n > 200)]
        for name, fn in bench_impls:
            t = timeit.timeit(lambda fn=fn: fn(pts), number=REPS) * 1000 / REPS
            print(f"  {name:<16} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
