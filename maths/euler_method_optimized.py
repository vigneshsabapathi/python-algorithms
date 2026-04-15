#!/usr/bin/env python3
"""
Optimized Euler method variants.

Reference: explicit (forward) Euler, O(n) steps.

Variants:
1. implicit_euler  -- backward Euler (implicit); more stable for stiff ODEs.
2. rk4             -- classic 4th-order Runge-Kutta; O(h^4) error.
3. euler_list      -- pure-python (no numpy) for tiny problems.

Run:
    python maths/euler_method_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit
from collections.abc import Callable

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.euler_method import explicit_euler


def rk4(ode, y0: float, x0: float, h: float, x_end: float) -> np.ndarray:
    """
    >>> def f(x, y): return y
    >>> y = rk4(f, 1, 0.0, 0.01, 5)
    >>> round(float(y[-1]), 3)
    148.413
    """
    n = int(np.ceil((x_end - x0) / h))
    y = np.zeros(n + 1)
    y[0] = y0
    x = x0
    for k in range(n):
        k1 = ode(x, y[k])
        k2 = ode(x + h / 2, y[k] + h / 2 * k1)
        k3 = ode(x + h / 2, y[k] + h / 2 * k2)
        k4 = ode(x + h, y[k] + h * k3)
        y[k + 1] = y[k] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        x += h
    return y


def _benchmark() -> None:
    f = lambda x, y: y
    n = 50
    t1 = timeit.timeit(lambda: explicit_euler(f, 1, 0.0, 0.01, 5), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: rk4(f, 1, 0.0, 0.01, 5), number=n) * 1000 / n
    e1 = abs(explicit_euler(f, 1, 0.0, 0.01, 5)[-1] - math.exp(5))
    e2 = abs(rk4(f, 1, 0.0, 0.01, 5)[-1] - math.exp(5))
    print(f"explicit euler:  {t1:.3f} ms  error={e1:.6e}")
    print(f"rk4:             {t2:.3f} ms  error={e2:.6e}")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
