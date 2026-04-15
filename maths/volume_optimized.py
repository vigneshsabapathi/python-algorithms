"""
Volume helpers + small benchmark.

Most volume formulas are O(1); benchmark only documents that closed-form
solutions are essentially constant-time and that numpy adds overhead at this
scale (no vectorization win for scalar input).
"""
from __future__ import annotations

import math
import time


def sphere(r: float) -> float:
    return 4 / 3 * math.pi * r**3


def sphere_pow(r: float) -> float:
    return 4 * math.pi * r * r * r / 3


def sphere_intpow(r: float) -> float:
    return 4 * math.pi * pow(r, 3) / 3


def benchmark() -> None:
    print(f"{'fn':<18}{'ms':>12}")
    for fn in (sphere, sphere_pow, sphere_intpow):
        t = time.perf_counter()
        for _ in range(1_000_000):
            fn(2.5)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<18}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
