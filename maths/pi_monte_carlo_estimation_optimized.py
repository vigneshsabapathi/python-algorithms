"""
Monte Carlo pi estimation variants + benchmark.

1. python_loop   - pure Python loop
2. vectorized    - numpy vectorized (if available)
3. math_based    - estimator using low-discrepancy (Halton) sequence
"""
from __future__ import annotations

import math
import random
import time


def python_loop(n: int, seed: int = 42) -> float:
    rng = random.Random(seed)
    inside = 0
    for _ in range(n):
        x, y = rng.random(), rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n


def vectorized(n: int, seed: int = 42) -> float:
    try:
        import numpy as np
    except ImportError:
        return python_loop(n, seed)
    rng = np.random.default_rng(seed)
    x = rng.random(n)
    y = rng.random(n)
    return 4.0 * float(np.sum(x * x + y * y <= 1.0)) / n


def _halton(i: int, base: int) -> float:
    f, r = 1.0, 0.0
    while i > 0:
        f /= base
        r += f * (i % base)
        i //= base
    return r


def halton_qmc(n: int, seed: int = 42) -> float:
    inside = 0
    for i in range(1, n + 1):
        x = _halton(i, 2)
        y = _halton(i, 3)
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n


def benchmark() -> None:
    print(f"{'fn':<14}{'n':>10}{'estimate':>14}{'err':>12}{'ms':>10}")
    for fn in (python_loop, vectorized, halton_qmc):
        for n in (10_000, 100_000, 1_000_000):
            t = time.perf_counter()
            e = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<14}{n:>10}{e:>14.6f}{abs(e - math.pi):>12.6f}{dt:>10.2f}")


if __name__ == "__main__":
    benchmark()
