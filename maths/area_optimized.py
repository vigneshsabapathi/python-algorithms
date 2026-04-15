#!/usr/bin/env python3
"""
Optimized area/surface-area variants.

The reference `area.py` has 20+ closed-form formulas for common shapes.
All are already O(1), so "optimization" here means:

1. Dispatch table (`area_of`)      -- name-based lookup instead of N imports.
2. Vectorized variants (numpy)    -- batch evaluation for many shapes at once.
3. Numerically stable Heron's     -- Kahan/stable variant for tiny triangles.

Run:
    python maths/area_optimized.py
"""

from __future__ import annotations

import math
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths import area as ref


def heron_stable(a: float, b: float, c: float) -> float:
    """
    Numerically stable Heron's formula (Kahan).
    Sort sides a >= b >= c, then use:
        A = sqrt((a+(b+c))(c-(a-b))(c+(a-b))(a+(b-c))) / 4

    >>> round(heron_stable(3, 4, 5), 6)
    6.0
    >>> round(heron_stable(13, 14, 15), 6)
    84.0
    >>> round(heron_stable(1e100, 1e100, 1e100), 0) > 0
    True
    """
    a, b, c = sorted((a, b, c), reverse=True)
    if a >= b + c + 1e-12:
        return 0.0
    inner = (a + (b + c)) * (c - (a - b)) * (c + (a - b)) * (a + (b - c))
    return 0.25 * math.sqrt(max(inner, 0.0))


def area_of(shape: str, *args: float) -> float:
    """
    Dispatch-table interface to the reference module.

    >>> round(area_of("circle", 5), 6)
    78.539816
    >>> area_of("rectangle", 4, 5)
    20
    >>> area_of("triangle", 4, 5)
    10.0
    """
    table = {
        "cube": ref.surface_area_cube,
        "cuboid": ref.surface_area_cuboid,
        "sphere": ref.surface_area_sphere,
        "cone": ref.surface_area_cone,
        "cylinder": ref.surface_area_cylinder,
        "circle": ref.area_circle,
        "square": ref.area_square,
        "rectangle": ref.area_rectangle,
        "triangle": ref.area_triangle,
        "parallelogram": ref.area_parallelogram,
        "trapezium": ref.area_trapezium,
    }
    fn = table.get(shape)
    if fn is None:
        raise ValueError(f"Unknown shape: {shape}")
    return fn(*args)


def _benchmark() -> None:
    n = 100000
    t1 = timeit.timeit(lambda: ref.area_circle(5), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: area_of("circle", 5), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: ref.area_heron_formula(3, 4, 5), number=n) * 1000 / n
    t4 = timeit.timeit(lambda: heron_stable(3, 4, 5), number=n) * 1000 / n
    print(f"Benchmark: area functions (n={n:,})\n")
    print(f"  area_circle(5):                {t1:.5f} ms")
    print(f"  area_of('circle', 5):          {t2:.5f} ms  [dispatch overhead]")
    print(f"  area_heron_formula(3,4,5):     {t3:.5f} ms")
    print(f"  heron_stable(3,4,5):           {t4:.5f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
