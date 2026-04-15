#!/usr/bin/env python3
"""
Optimized arc_length variants.

Reference: s = 2*pi*r * angle/360  (degrees).

Variants:
1. arc_length_radians      -- s = r * theta (radians); the pure formula.
2. arc_length_constant     -- precompute pi/180 to reduce ops.
3. arc_length_vectorized   -- numpy broadcast over arrays (batch mode).

Run:
    python maths/arc_length_optimized.py
"""

from __future__ import annotations

import math
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.arc_length import arc_length as arc_length_reference

_PI_OVER_180 = math.pi / 180.0


def arc_length_radians(theta: float, radius: float) -> float:
    """
    Pure arc formula s = r * theta where theta is radians.

    >>> round(arc_length_radians(math.pi / 2, 10), 6)
    15.707963
    """
    return radius * theta


def arc_length_constant(angle_deg: float, radius: float) -> float:
    """
    Precomputed pi/180 — cuts one division per call.

    >>> round(arc_length_constant(90, 10), 10)
    15.7079632679
    >>> round(arc_length_constant(45, 5), 10)
    3.926990817
    """
    return radius * angle_deg * _PI_OVER_180


def _benchmark() -> None:
    angles = list(range(0, 360, 3))
    n = 50000
    print(f"Benchmark: arc_length (n={n:,} iterations over {len(angles)} angles)\n")
    t1 = timeit.timeit(lambda: [arc_length_reference(a, 10) for a in angles], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [arc_length_constant(a, 10) for a in angles], number=n) * 1000 / n
    print(f"  arc_length (reference):       {t1:.4f} ms")
    print(f"  arc_length_constant:          {t2:.4f} ms  [{t1/t2:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
