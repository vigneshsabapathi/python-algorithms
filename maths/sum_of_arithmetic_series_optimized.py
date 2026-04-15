"""
Arithmetic-series sum variants + benchmark.

1. formula         - n/2 * (2a + (n-1)d)        O(1)
2. loop            - explicit summation         O(n)
3. range_sum       - sum(range(...))            O(n) (but C-fast)
4. numpy_vector    - numpy.arange().sum()       O(n) vectorized
"""
from __future__ import annotations

import time


def formula(a: float, d: float, n: int) -> float:
    return n / 2 * (2 * a + (n - 1) * d)


def loop(a: float, d: float, n: int) -> float:
    s = 0.0
    for k in range(n):
        s += a + k * d
    return s


def range_sum(a: int, d: int, n: int) -> int:
    if d == 0:
        return a * n
    return sum(range(a, a + n * d, d))


def numpy_vector(a, d, n):
    try:
        import numpy as np
    except ImportError:
        return loop(a, d, n)
    return float(np.arange(a, a + n * d, d, dtype=float).sum()) if d else a * n


def benchmark() -> None:
    print(f"{'fn':<14}{'n':>10}{'result':>16}{'ms':>12}")
    for n in (1_000, 100_000, 1_000_000):
        for fn in (formula, loop, range_sum, numpy_vector):
            t = time.perf_counter()
            r = fn(1, 2, n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<14}{n:>10}{r:>16.1f}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
