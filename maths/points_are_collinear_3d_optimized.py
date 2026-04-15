"""
Collinearity of 3 points in 3D: multiple approaches + benchmark.

1. cross_product     - zero cross product of (b-a), (c-a)
2. rank_check        - rank of [b-a; c-a] <= 1 via proportional coords
3. volume_tetra      - 6*volume of tetrahedron formed (for 4 points) / degenerate
4. area_triangle     - magnitude of cross product = 2*area, compare to 0
"""
from __future__ import annotations

import math
import time


def cross_product(a, b, c, tol=1e-9):
    abv = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    acv = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    cx = abv[1] * acv[2] - abv[2] * acv[1]
    cy = abv[2] * acv[0] - abv[0] * acv[2]
    cz = abv[0] * acv[1] - abv[1] * acv[0]
    return abs(cx) <= tol and abs(cy) <= tol and abs(cz) <= tol


def area_triangle(a, b, c, tol=1e-9):
    abv = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    acv = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    cx = abv[1] * acv[2] - abv[2] * acv[1]
    cy = abv[2] * acv[0] - abv[0] * acv[2]
    cz = abv[0] * acv[1] - abv[1] * acv[0]
    return math.sqrt(cx * cx + cy * cy + cz * cz) <= tol


def rank_check(a, b, c, tol=1e-9):
    v1 = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    v2 = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    # find nonzero component of v1
    # check v2 = k * v1
    k = None
    for i in range(3):
        if abs(v1[i]) > tol:
            k = v2[i] / v1[i]
            break
    if k is None:
        # v1 is zero vector -> a == b, always collinear with c
        return True
    for i in range(3):
        if abs(v2[i] - k * v1[i]) > tol:
            return False
    return True


def benchmark() -> None:
    cases = [
        ((0, 0, 0), (1, 1, 1), (2, 2, 2), True),
        ((0, 0, 0), (1, 0, 0), (0, 1, 0), False),
        ((1, 2, 3), (4, 5, 6), (7, 8, 9), True),
    ]
    funcs = [cross_product, area_triangle, rank_check]
    print(f"{'fn':<16}{'case':>6}{'result':>8}{'ms':>12}")
    for fn in funcs:
        for i, (a, b, c, _) in enumerate(cases):
            t = time.perf_counter()
            for _ in range(100000):
                r = fn(a, b, c)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<16}{i:>6}{str(r):>8}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
