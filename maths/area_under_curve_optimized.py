#!/usr/bin/env python3
"""
Optimized area_under_curve variants.

Reference: trapezoidal rule, O(steps).

Variants:
1. simpson_rule       -- O(steps), much more accurate for smooth fns.
2. trapezoidal_numpy  -- vectorized trapezoidal rule.
3. midpoint_rule      -- rectangle rule at interval midpoint.

Run:
    python maths/area_under_curve_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from collections.abc import Callable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.area_under_curve import trapezoidal_area


def simpson_rule(fnc: Callable[[float], float], a: float, b: float, steps: int = 100) -> float:
    """
    Simpson's 1/3 rule (steps must be even; bumped up if odd).
    Error O(h^4) vs trapezoidal's O(h^2).

    >>> round(simpson_rule(lambda x: x**2, 0, 1, 100), 6)
    0.333333
    >>> round(simpson_rule(lambda x: 9*x**2, -4, 0, 100), 4)
    192.0
    """
    if steps % 2:
        steps += 1
    h = (b - a) / steps
    s = fnc(a) + fnc(b)
    for i in range(1, steps):
        s += (4 if i % 2 else 2) * fnc(a + i * h)
    return s * h / 3


def midpoint_rule(fnc: Callable[[float], float], a: float, b: float, steps: int = 100) -> float:
    """
    >>> round(midpoint_rule(lambda x: x**2, 0, 1, 1000), 5)
    0.33333
    """
    h = (b - a) / steps
    return h * sum(fnc(a + (i + 0.5) * h) for i in range(steps))


def _benchmark() -> None:
    f = lambda x: x ** 3 + x ** 2
    n = 200
    for steps in (100, 1000, 10000):
        t1 = timeit.timeit(lambda: trapezoidal_area(f, -5, 5, steps), number=n) * 1000 / n
        t2 = timeit.timeit(lambda: simpson_rule(f, -5, 5, steps), number=n) * 1000 / n
        t3 = timeit.timeit(lambda: midpoint_rule(f, -5, 5, steps), number=n) * 1000 / n
        print(f"steps={steps:>6}: trap={t1:.4f}ms simpson={t2:.4f}ms mid={t3:.4f}ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
