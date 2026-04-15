"""
Hypotenuse computation variants + benchmark.

1. naive_sqrt    - sqrt(a*a + b*b)
2. math_hypot    - math.hypot (avoids overflow/underflow)
3. manual_scale  - scale by max(|a|, |b|) to avoid overflow
"""
from __future__ import annotations

import math
import time


def naive_sqrt(a: float, b: float) -> float:
    return math.sqrt(a * a + b * b)


def math_hypot(a: float, b: float) -> float:
    return math.hypot(a, b)


def manual_scale(a: float, b: float) -> float:
    a, b = abs(a), abs(b)
    if a < b:
        a, b = b, a
    if a == 0:
        return 0.0
    r = b / a
    return a * math.sqrt(1 + r * r)


def benchmark() -> None:
    cases = [(3, 4), (5e150, 12e150), (1e-200, 1e-200)]
    print(f"{'fn':<14}{'inputs':>30}{'result':>18}{'ms':>12}")
    for fn in (naive_sqrt, math_hypot, manual_scale):
        for a, b in cases:
            t = time.perf_counter()
            for _ in range(100000):
                try:
                    r = fn(a, b)
                except OverflowError:
                    r = float("inf")
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<14}{str((a, b)):>30}{r:>18.4g}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
