"""
Geometric-series sum variants + benchmark.

1. formula          - closed form, O(log n) due to r**n
2. loop_accumulate  - iterative, O(n)
3. pow_builtin      - use pow(r, n) explicitly
4. infinite         - a / (1 - r) when |r| < 1 (limit of n -> inf)
"""
from __future__ import annotations

import time


def formula(a, r, n):
    if r == 1:
        return a * n
    return a * (1 - r**n) / (1 - r)


def loop_accumulate(a, r, n):
    s = 0.0
    term = a
    for _ in range(n):
        s += term
        term *= r
    return s


def pow_builtin(a, r, n):
    if r == 1:
        return a * n
    return a * (1 - pow(r, n)) / (1 - r)


def infinite(a, r):
    if abs(r) >= 1:
        raise ValueError("|r| must be < 1 for convergence")
    return a / (1 - r)


def benchmark() -> None:
    print(f"{'fn':<18}{'n':>10}{'result':>24}{'ms':>12}")
    for n in (10, 100, 10_000):
        for fn in (formula, loop_accumulate, pow_builtin):
            t = time.perf_counter()
            for _ in range(10000):
                r = fn(1, 1.0001, n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<18}{n:>10}{r:>24.6f}{dt:>12.3f}")
    print(f"infinite(1, 0.5) = {infinite(1, 0.5)}")


if __name__ == "__main__":
    benchmark()
