"""
tanh variants + benchmark.

1. naive          - (e^x - e^-x) / (e^x + e^-x), unstable for large |x|
2. stable_pos     - branch by sign of x to avoid overflow
3. math_tanh      - math.tanh (libm)
4. sigmoid_form   - tanh(x) = 2 sigmoid(2x) - 1
"""
from __future__ import annotations

import math
import time


def naive(x: float) -> float:
    e_pos, e_neg = math.exp(x), math.exp(-x)
    return (e_pos - e_neg) / (e_pos + e_neg)


def stable_pos(x: float) -> float:
    if x >= 0:
        e = math.exp(-2 * x)
        return (1 - e) / (1 + e)
    e = math.exp(2 * x)
    return (e - 1) / (e + 1)


def math_tanh(x: float) -> float:
    return math.tanh(x)


def sigmoid_form(x: float) -> float:
    sig = 1.0 / (1.0 + math.exp(-2 * x)) if x >= 0 else math.exp(2 * x) / (1.0 + math.exp(2 * x))
    return 2 * sig - 1


def benchmark() -> None:
    xs = [-500, -1, 0, 1, 500]
    print(f"{'fn':<14}{'x':>10}{'y':>14}{'ms':>10}")
    for fn in (naive, stable_pos, math_tanh, sigmoid_form):
        for x in xs:
            try:
                t = time.perf_counter()
                for _ in range(10000):
                    y = fn(x)
                dt = (time.perf_counter() - t) * 1000
            except OverflowError:
                y = float("nan")
                dt = 0
            print(f"{fn.__name__:<14}{x:>10}{y:>14.6f}{dt:>10.3f}")


if __name__ == "__main__":
    benchmark()
