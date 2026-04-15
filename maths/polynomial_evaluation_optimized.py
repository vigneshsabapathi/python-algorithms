"""
Polynomial evaluation variants + benchmark.

1. naive         - sum(c * x**i) -- O(n^2) exponentiation cost
2. horner        - Horner's rule, O(n)
3. pow_accum     - accumulate x^i multiplicatively, O(n)
4. numpy_polyval - numpy.polyval (descending order), O(n) vectorized
"""
from __future__ import annotations

import time
from typing import Sequence


def naive(coeffs: Sequence[float], x: float) -> float:
    return sum(c * x**i for i, c in enumerate(coeffs))


def horner(coeffs: Sequence[float], x: float) -> float:
    r = 0
    for c in reversed(coeffs):
        r = r * x + c
    return r


def pow_accum(coeffs: Sequence[float], x: float) -> float:
    r = 0
    xp = 1
    for c in coeffs:
        r += c * xp
        xp *= x
    return r


def numpy_polyval(coeffs: Sequence[float], x: float) -> float:
    try:
        import numpy as np
    except ImportError:
        return horner(coeffs, x)
    return float(np.polyval(list(reversed(coeffs)), x))


def benchmark() -> None:
    import random

    rng = random.Random(0)
    sizes = [10, 100, 1000]
    print(f"{'fn':<16}{'size':>6}{'ms':>12}")
    for size in sizes:
        coeffs = [rng.random() for _ in range(size)]
        for fn in (naive, horner, pow_accum, numpy_polyval):
            t = time.perf_counter()
            for _ in range(1000):
                fn(coeffs, 1.0001)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<16}{size:>6}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
