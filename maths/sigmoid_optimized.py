"""
Sigmoid variants + benchmark.

1. naive              - 1 / (1 + exp(-x))
2. stable             - split positive/negative x to avoid exp overflow
3. numpy_sigmoid      - vectorized numpy
4. tanh_form          - sigmoid(x) = 0.5 * (1 + tanh(x/2))
"""
from __future__ import annotations

import math
import time


def naive(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def stable(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def tanh_form(x: float) -> float:
    return 0.5 * (1.0 + math.tanh(0.5 * x))


def numpy_sigmoid(x):
    try:
        import numpy as np
    except ImportError:
        return naive(x)
    return float(1.0 / (1.0 + np.exp(-x)))


def benchmark() -> None:
    xs = [-1000, -5, 0, 5, 1000]
    print(f"{'fn':<16}{'x':>12}{'y':>14}{'ms':>10}")
    for fn in (naive, stable, tanh_form, numpy_sigmoid):
        for x in xs:
            try:
                t = time.perf_counter()
                for _ in range(100000):
                    y = fn(x)
                dt = (time.perf_counter() - t) * 1000
            except OverflowError:
                y = float("nan")
                dt = 0
            print(f"{fn.__name__:<16}{x:>12}{y:>14.6f}{dt:>10.2f}")


if __name__ == "__main__":
    benchmark()
