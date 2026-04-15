#!/usr/bin/env python3
"""
Optimized euler_modified (Heun's method) variants.

Reference: computes ode_func twice per step (at current + predicted).

Variants:
1. heun_cached     -- reuse ode_func(x, y[k]) between predictor and corrector.
2. rk4             -- 4th-order Runge-Kutta (better error).
3. midpoint_method -- RK2 midpoint alternative to Heun's.

Run:
    python maths/euler_modified_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit
import numpy as np
from collections.abc import Callable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.euler_modified import euler_modified as ref


def heun_cached(ode: Callable, y0: float, x0: float, h: float, x_end: float) -> np.ndarray:
    """
    Avoid duplicate ode_func(x, y[k]) call by caching k1.

    >>> def f(x, y): return -2*x*(y**2)
    >>> y = heun_cached(f, 1.0, 0.0, 0.2, 1.0)
    >>> round(float(y[-1]), 9)
    0.503338255
    """
    n = int(np.ceil((x_end - x0) / h))
    y = np.zeros(n + 1)
    y[0] = y0
    x = x0
    for k in range(n):
        k1 = ode(x, y[k])
        y_pred = y[k] + h * k1
        k2 = ode(x + h, y_pred)
        y[k + 1] = y[k] + h / 2 * (k1 + k2)
        x += h
    return y


def midpoint_method(ode: Callable, y0: float, x0: float, h: float, x_end: float) -> np.ndarray:
    """
    RK2 midpoint: y_{n+1} = y_n + h*f(x_n + h/2, y_n + h/2*f(x_n,y_n)).

    >>> def f(x, y): return y
    >>> y = midpoint_method(f, 1.0, 0.0, 0.1, 1.0)
    >>> round(float(y[-1]), 4)
    2.7141
    """
    n = int(np.ceil((x_end - x0) / h))
    y = np.zeros(n + 1)
    y[0] = y0
    x = x0
    for k in range(n):
        k1 = ode(x, y[k])
        k2 = ode(x + h / 2, y[k] + h / 2 * k1)
        y[k + 1] = y[k] + h * k2
        x += h
    return y


def _benchmark() -> None:
    f = lambda x, y: -2 * x * (y ** 2)
    n = 100
    t1 = timeit.timeit(lambda: ref(f, 1.0, 0.0, 0.01, 1.0), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: heun_cached(f, 1.0, 0.0, 0.01, 1.0), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: midpoint_method(f, 1.0, 0.0, 0.01, 1.0), number=n) * 1000 / n
    print(f"reference:   {t1:.3f} ms")
    print(f"heun cached: {t2:.3f} ms  [{t1/t2:.2f}x]")
    print(f"midpoint:    {t3:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
