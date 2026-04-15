"""
Harmonic-sum variants + benchmark.

1. forward_loop    - 1/1 + 1/2 + ...
2. reverse_loop    - sum from smallest to largest term (better precision)
3. asymptotic      - ln(n) + gamma + corrections (O(1))
4. fractions_exact - exact rational sum for small n
"""
from __future__ import annotations

import math
import time
from fractions import Fraction


def forward_loop(n: int) -> float:
    s = 0.0
    for k in range(1, n + 1):
        s += 1.0 / k
    return s


def reverse_loop(n: int) -> float:
    s = 0.0
    for k in range(n, 0, -1):
        s += 1.0 / k
    return s


def asymptotic(n: int) -> float:
    GAMMA = 0.5772156649015329
    return math.log(n) + GAMMA + 1.0 / (2 * n) - 1.0 / (12 * n * n)


def fractions_exact(n: int) -> Fraction:
    s = Fraction(0)
    for k in range(1, n + 1):
        s += Fraction(1, k)
    return s


def benchmark() -> None:
    print(f"{'fn':<18}{'n':>10}{'value':>20}{'ms':>12}")
    for n in (10, 1_000, 100_000):
        for fn in (forward_loop, reverse_loop, asymptotic):
            t = time.perf_counter()
            v = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<18}{n:>10}{v:>20.10f}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
