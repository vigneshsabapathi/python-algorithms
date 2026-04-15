"""
Degrees-to-radians + benchmark.

1. scalar_mul   - degrees * pi / 180
2. math_radians - math.radians (C implementation)
3. reciprocal   - degrees * (pi / 180)  precompute constant
"""
from __future__ import annotations

import math
import time

_FACTOR = math.pi / 180


def scalar_mul(d: float) -> float:
    return d * math.pi / 180


def math_radians(d: float) -> float:
    return math.radians(d)


def reciprocal(d: float) -> float:
    return d * _FACTOR


def benchmark() -> None:
    values = [0, 30, 90, 180, 360, -180]
    print(f"{'fn':<16}{'ms':>12}")
    for fn in (scalar_mul, math_radians, reciprocal):
        t = time.perf_counter()
        for _ in range(1_000_000):
            for v in values:
                fn(v)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<16}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
